#!/usr/bin/env python3
"""
Generare minute din transcriere folosind Ollama (local, fără API keys)
Necesită: ollama pull mistral (sau alt model)
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "mistral"  # Schimbă cu alt model dacă vrei: llama2, neural-chat, etc.

def load_prompt():
    """Încarcă prompt din prompt_minute.txt"""
    if os.path.exists("prompt_minute.txt"):
        with open("prompt_minute.txt", "r", encoding="utf-8") as f:
            return f.read()
    else:
        # Fallback dacă fișierul nu există
        return """Transcrierea completă a unei ședințe în limba română se generează minutele ședinței cu următoarea structură:

1. Data și locul ședinței
2. Participanți
3. Ordinea de zi
4. Discuții pe puncte
5. Decizii adoptate
6. Sarcini și responsabili
7. Termene

INSTRUCȚIUNI:
- Nu inventa informații care nu apar în transcriere
- Fii concis, tehnic și neutru
- La final, oferă un sumar de maximum 5 rânduri
"""

def check_ollama_running():
    """Verifică dacă Ollama rulează"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def generate_minutes(transcription_text, model=DEFAULT_MODEL):
    """
    Generează minute din transcriere
    
    Args:
        transcription_text (str): Textul transcrierit
        model (str): Modelul Ollama de folosit
    
    Returns:
        str: Minutele generate
    """
    
    if not check_ollama_running():
        raise ConnectionError(
            f"❌ Ollama nu rulează pe {OLLAMA_URL}\n"
            "Instalează și pornește: ollama pull mistral && ollama serve"
        )
    
    prompt_template = load_prompt()
    prompt = f"{prompt_template}\n\nTRANSCRIERE:\n{transcription_text}\n\nMINUTE ȘEDINȚEI:"
    
    print(f"🤖 Generare minute cu modelul {model}...")
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3,  # Răspunsuri mai deterministe
            },
            timeout=300  # Timeout mare pentru modele mari
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama eroare: {response.text}")
        
        result = response.json()
        return result.get("response", "")
    
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            f"Nu se poate conecta la Ollama pe {OLLAMA_URL}\n"
            "Pornim: ollama serve"
        )

def load_transcription(file_path):
    """Încarcă transcriere din fișier"""
    if file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("text", "")
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

def save_minutes(minutes_text, output_dir="output", base_name="meeting"):
    """Salvează minute generate"""
    os.makedirs(output_dir, exist_ok=True)
    
    minutes_file = os.path.join(output_dir, f"{base_name}_minutes.txt")
    with open(minutes_file, "w", encoding="utf-8") as f:
        f.write(f"MINUTE ȘEDINȚEI\n")
        f.write(f"Generat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(minutes_text)
    
    print(f"✅ Minute salvate: {minutes_file}")
    return minutes_file

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Utilizare: python minutes_generator.py <transcription_file> [model]")
        print("\nExemplu: python minutes_generator.py output/meeting_transcription.txt mistral")
        print("\nModele disponibile (după: ollama pull <model>):")
        print("  - mistral (recomandat - rapid și bun)")
        print("  - llama2")
        print("  - neural-chat")
        print("  - dolphin-mixtral")
        sys.exit(1)
    
    transcription_file = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL
    
    try:
        if not os.path.exists(transcription_file):
            raise FileNotFoundError(f"Fișier nu găsit: {transcription_file}")
        
        print(f"📖 Încarcă transcriere: {transcription_file}")
        transcription_text = load_transcription(transcription_file)
        
        minutes = generate_minutes(transcription_text, model=model)
        
        base_name = Path(transcription_file).stem.replace("_transcription", "")
        minutes_file = save_minutes(minutes, base_name=base_name)
        
        print(f"\n📋 Minute generate:\n")
        print(minutes)
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
