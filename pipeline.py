#!/usr/bin/env python3
"""
Pipeline complet: Audio → Transcriere → Minute
Execută ambii pași: transcriere + generare minute
"""

import sys
import os
from pathlib import Path
from transcriber import transcribe_audio, save_transcription
from minutes_generator import generate_minutes, save_minutes, check_ollama_running

def main():
    if len(sys.argv) < 2:
        print("PIPELINE: Audio → Transcriere → Minute")
        print("\nUtilizare: python pipeline.py <audio_file> [whisper_model] [ollama_model]")
        print("\nExemplu:")
        print("  python pipeline.py meeting.mp3")
        print("  python pipeline.py meeting.mp3 base mistral")
        print("\nModele Whisper: tiny, base, small, medium, large")
        print("Modele Ollama: mistral, llama2, neural-chat, dolphin-mixtral")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    whisper_model = sys.argv[2] if len(sys.argv) > 2 else "base"
    ollama_model = sys.argv[3] if len(sys.argv) > 3 else "mistral"
    
    try:
        # PASUL 1: Transcriere
        print("\n" + "="*50)
        print("PASUL 1: TRANSCRIERE AUDIO")
        print("="*50)
        
        transcription = transcribe_audio(audio_file, model=whisper_model)
        text_file, json_file = save_transcription(transcription)
        
        # PASUL 2: Generare minute
        print("\n" + "="*50)
        print("PASUL 2: GENERARE MINUTE")
        print("="*50)
        
        if not check_ollama_running():
            print("\n⚠️  Ollama nu rulează. Doar transcriere completă.")
            print("Pentru minute, pornește Ollama:")
            print("  ollama pull mistral")
            print("  ollama serve")
            sys.exit(0)
        
        minutes = generate_minutes(transcription["text"], model=ollama_model)
        base_name = Path(audio_file).stem
        minutes_file = save_minutes(minutes, base_name=base_name)
        
        print("\n" + "="*50)
        print("✅ PIPELINE COMPLET")
        print("="*50)
        print(f"📄 Transcriere: {text_file}")
        print(f"📋 Minute: {minutes_file}")
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
