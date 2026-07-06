#!/usr/bin/env python3
"""
Transcriere audio → text folosind OpenAI Whisper (local)
Suporta: MP3, WAV, M4A, FLAC, etc.
"""

import whisper
import os
import json
from pathlib import Path
from datetime import datetime

def transcribe_audio(audio_file, model="base", language="ro"):
    """
    Transcriere audio în română
    
    Args:
        audio_file (str): Path la fișierul audio
        model (str): Model Whisper: tiny, base, small, medium, large
        language (str): Cod limbă (ro = română)
    
    Returns:
        dict: Transcriere și metadate
    """
    
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Fișierul audio nu există: {audio_file}")
    
    print(f"📥 Încarcă modelul Whisper ({model})...")
    model_obj = whisper.load_model(model)
    
    print(f"🔄 Transcriere în curs: {audio_file}")
    result = model_obj.transcribe(audio_file, language=language, verbose=False)
    
    return {
        "text": result["text"],
        "language": result["language"],
        "segments": result["segments"],
        "duration": result.get("duration", "N/A"),
        "file": audio_file,
        "timestamp": datetime.now().isoformat()
    }

def save_transcription(transcription, output_dir="output"):
    """Salvează transcriere în text și JSON"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Extrage nume fișier original
    base_name = Path(transcription["file"]).stem
    
    # Salvează text brut
    text_file = os.path.join(output_dir, f"{base_name}_transcription.txt")
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(transcription["text"])
    
    # Salvează JSON complet
    json_file = os.path.join(output_dir, f"{base_name}_transcription.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(transcription, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Transcriere salvată:")
    print(f"   📄 {text_file}")
    print(f"   📋 {json_file}")
    
    return text_file, json_file

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Utilizare: python transcriber.py <audio_file> [model]")
        print("\nModele disponibile: tiny, base, small, medium, large")
        print("Exemplu: python transcriber.py meeting.mp3 base")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    try:
        transcription = transcribe_audio(audio_file, model=model)
        text_file, json_file = save_transcription(transcription)
        print(f"\n📝 Text transcriere:\n{transcription['text'][:200]}...")
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
