from flask import Flask, render_template, request, jsonify
import json
import os
from openai import OpenAI

app = Flask(__name__)

# Load ad specs from JSON
with open('adspecs.json', encoding='utf-8') as f:
    adspecs = json.load(f)

# Synonyms for technical fields (Norwegian)
keyword_map = {
    "filtype": ["filtype", "format", "filformat", "videoformat"],
    "kodek": ["kodek", "codec", "koding"],
    "audiolevel": ["audiolevel", "lydnivå", "loudness", "lufs", "lkfs", "lyd"],
    "dimensjoner": ["dimensjoner", "oppløsning", "størrelse", "piksler", "hd", "1080p", "720p"],
    "aspect_ratio": ["aspect ratio", "sideforhold", "forhold", "16:9", "9:16"],
    "framerate": ["framerate", "bilderate", "fps", "bilder per sekund"],
    "maks_storrelse": ["maks størrelse", "maksimal størrelse", "filstørrelse", "størrelse", "max size", "megabyte", "mb", "stor"],
    "filmlengde": ["filmlengde", "lengde", "varighet", "hvor lang", "sekunder", "minutter", "video være", "hvor lenge"],
    "safezones": ["safezone", "safe zone", "safe zones", "safezones", "sikker sone", "sikre soner", "margin", "marginer"]
}

# Initialize OpenAI client (will use API key from environment variable)
client = None
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except Exception as e:
    print(f"OpenAI initialization failed: {e}")

# Helper: Compose system prompt from JSON
def build_system_prompt(adspecs):
    specs = adspecs.get("technical_specs", {})
    normative = adspecs.get("normative_info", {})
    costar = adspecs.get("chatbot_guidelines", {}).get("costar", {})
    
    specs_text = "\n".join([
        f"- {key.replace('_', ' ').capitalize()}: {value.get('value', '')} ({value.get('explanation', '')})"
        for key, value in specs.items() if isinstance(value, dict)
    ])
    
    advantages = "\n".join([f"- {a}" for a in normative.get("advantages", [])])
    best_practices = "\n".join([f"- {b}" for b in normative.get("best_practices", [])])
    product_desc = normative.get("product_description", "")
    
    costar_text = "\n".join([f"{k.capitalize()}: {v}" for k, v in costar.items()])
    
    return f"""Du er Norgespecs™ Assistenten.

TEKNISKE SPESIFIKASJONER:
{specs_text}

NORMATIV INFO:
Fordeler:
{advantages}
Beste praksis:
{best_practices}
Produktbeskrivelse: {product_desc}

CHATBOT-REGLER (COSTAR):
{costar_text}

Svar alltid på norsk. Vær hjelpsom, tydelig og profesjonell. Gi konkrete, tekniske og normative svar basert på dataene over. Hvis du ikke vet svaret, si ifra og henvis til offisielle spesifikasjoner."""

SYSTEM_PROMPT = build_system_prompt(adspecs)

# Fallback bot: dynamic matching from JSON

def get_fallback_response(user_message, adspecs):
    user_message = user_message.lower()
    specs = adspecs.get("technical_specs", {})
    for key, synonyms in keyword_map.items():
        if any(syn in user_message for syn in synonyms):
            if key in specs:
                value = specs[key].get("value", "")
                explanation = specs[key].get("explanation", "")
                if value and explanation:
                    return f"{value} — {explanation}"
                elif value:
                    return value
    return "Beklager, jeg forstår ikke spørsmålet ditt. Prøv å spørre om filstørrelse, format, kodek, audiolevel, dimensjoner, aspect ratio, framerate, filmlengde eller safe zone."

# GPT-4 bot: always up-to-date with JSON

def get_gpt4_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=350,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"GPT-4 API error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'response': 'Vennligst skriv inn et spørsmål.'})
    # Try GPT-4 first if available
    if client:
        gpt_response = get_gpt4_response(user_message)
        if gpt_response:
            return jsonify({
                'response': gpt_response,
                'powered_by': 'GPT-4'
            })
    # Fallback to dynamic bot
    simple_response = get_fallback_response(user_message, adspecs)
    return jsonify({
        'response': simple_response,
        'powered_by': 'Simple Bot'
    })

if __name__ == '__main__':
    app.run(debug=True) 