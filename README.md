# Norgespecs™

Norgespecs™ er bransjestandarden for videoannonse-spesifikasjoner i Norge, brukt og anbefalt av ledende mediehus og organisasjoner.

## Funksjoner

- Interaktiv chatbot for spørsmål om tekniske spesifikasjoner
- Detaljerte spesifikasjoner for videoannonser
- Responsivt design
- GPT-4 integrasjon for avanserte svar
- Fallback til enkel bot når GPT-4 ikke er tilgjengelig

## Tekniske Spesifikasjoner

Applikasjonen inneholder detaljerte spesifikasjoner for:
- Filtyper (.mp4/VAST)
- Kodek (H264)
- Audiolevel (-23 LUFS)
- Dimensjoner (1080p/720p)
- Aspect ratio (16:9/9:16)
- Framerate (25fps)
- Safe zones
- Maksimal filstørrelse

## Installasjon

1. Klon repositoriet:
```bash
git clone [repository-url]
cd norgespecs
```

2. Opprett og aktiver et virtuelt miljø:
```bash
python -m venv venv
source venv/bin/activate  # På Windows: venv\Scripts\activate
```

3. Installer avhengigheter:
```bash
pip install -r requirements.txt
```

4. Sett opp miljøvariabler:
```bash
# Opprett en .env fil og legg til:
OPENAI_API_KEY=din_api_nøkkel_her
```

5. Start applikasjonen:
```bash
python app.py
```

## Miljøkrav

- Python 3.8 eller nyere
- Flask
- OpenAI Python package (for GPT-4 integrasjon)
- Se requirements.txt for fullstendig liste

## Lisens

Copyright © 2024 Norgespecs™. Alle rettigheter reservert. 