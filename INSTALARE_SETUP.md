# 🎙️ Sistem Local de Transcriere și Minute Ședințe

Transcriere audio → Text + Generare minute automate (100% local, fără API keys)

---

## 📋 Prerequisite

- **Python 3.9+**
- **FFmpeg** (pentru procesare audio)
- **CUDA** (opțional - pentru accelerare GPU pe Whisper)

---

## 🚀 Instalare Rapidă

### 1️⃣ Instalează dependențele Python
```bash
pip install -r requirements.txt
```

### 2️⃣ Instalează FFmpeg

**Windows (cu Chocolatey):**
```bash
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### 3️⃣ Instalează Ollama (pentru minute automate)

Descarcă de la: https://ollama.ai

Apoi în terminal:
```bash
ollama pull mistral
ollama serve
```

> **Rulează `ollama serve` în alt terminal înainte de a genera minute!**

---

## 💻 Utilizare

### Opțiunea 1: Pipeline Complet (Audio → Transcriere → Minute)

```bash
python pipeline.py meeting.mp3
```

**Cu modele specifice:**
```bash
python pipeline.py meeting.mp3 base mistral
```

### Opțiunea 2: Doar Transcriere

```bash
python transcriber.py meeting.mp3
```

**Modele Whisper:**
- `tiny` - cel mai rapid (~1GB RAM)
- `base` - bun compromis (recommended) (~2GB)
- `small` - mai acurat (~2.5GB)
- `medium` - foarte acurat (~5GB)
- `large` - cea mai bună calitate (~10GB)

### Opțiunea 3: Doar Generare Minute

```bash
python minutes_generator.py output/meeting_transcription.txt mistral
```

---

## 📁 Structura Ieșirilor

```
output/
├── meeting_transcription.txt      # Text transcriere brut
├── meeting_transcription.json     # Transcriere + metadate
└── meeting_minutes.txt            # Minute generate
```

---

## ⚙️ Configurare Avansată

### Folosi alt model Ollama

```bash
# Descarcă model
ollama pull llama2

# Generează minute cu llama2
python minutes_generator.py output/meeting_transcription.txt llama2
```

**Modele disponibile:**
- `mistral` - rapid, bun pentru română
- `llama2` - puternic, mai lent
- `neural-chat` - optimizat conversații
- `dolphin-mixtral` - foarte bun

### Accelerare cu GPU (CUDA)

**Windows/Linux cu NVIDIA:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

> Whisper va detecta automat și folosi GPU-ul

---

## 🔧 Troubleshooting

### ❌ "FFmpeg not found"
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### ❌ "Ollama connection refused"
Deschide alt terminal și rulează:
```bash
ollama serve
```

### ❌ Transcriere foarte lentă
- Foloseşte model mai mic: `tiny` sau `base`
- Activează GPU cu PyTorch CUDA
- Scurtează fișierul audio

### ❌ Minute slabe/incomplete
- Încearcă alt model: `ollama pull llama2`
- Crește temperatura în `minutes_generator.py` la 0.5
- Transcriere mai scurtă (< 5 minute)

---

## 📊 Performanță Estimată

| Model | Viteză | Calitate | RAM | Timp |
|-------|--------|----------|-----|------|
| tiny | ⚡⚡⚡ | ⭐ | 1GB | ~1 min/10 min audio |
| base | ⚡⚡ | ⭐⭐⭐ | 2GB | ~5 min/10 min audio |
| small | ⚡ | ⭐⭐⭐⭐ | 2.5GB | ~15 min/10 min audio |
| large | ❌ | ⭐⭐⭐⭐⭐ | 10GB | ~60 min/10 min audio |

---

## 📝 Format Minute Generate

```
MINUTE ȘEDINȚEI
Generat: 2025-06-06 14:30:00
==================================================

1. DATA ȘI LOCUL ȘEDINȚEI
   - Data: ...
   - Locul: ...

2. PARTICIPANȚI
   - Prezent: ...
   - Absent: ...

3. ORDINEA DE ZI
   - Punct 1: ...
   - Punct 2: ...

4. DISCUȚII PE PUNCTE
   [Detalii discuții]

5. DECIZII ADOPTATE
   - Decizie 1: ...
   - Decizie 2: ...

6. SARCINI ȘI RESPONSABILI
   - Sarcina 1: ...
   - Responsabil: ...
   - Termen: ...

7. TERMENE
   - Termen 1: ...
```

---

## 🎯 Exemple

### Transcriere Meeting Zoom
```bash
# 1. Descarcă recording-ul
# 2. Conversie la MP3 (optional)
# 3. Rulează:
python pipeline.py zoom_recording.mp3
```

### Ședință rapidă (< 15 min)
```bash
python pipeline.py meeting.wav tiny
```

### Ședință lungă (> 30 min)
```bash
python pipeline.py meeting.mp3 small
```

---

## 📚 Resurse Suplimentare

- [Whisper Documentation](https://github.com/openai/whisper)
- [Ollama Models](https://ollama.ai/library)
- [FFmpeg Guide](https://ffmpeg.org/download.html)

---

## 💡 Tips & Tricks

1. **Transcriere mai exactă**: Redă audio mai clar cu `tiny` model de 2 ori decât `base` o dată
2. **Minute mai bune**: Transcriere scurtă (< 3000 cuvinte) = minute mai clarificate
3. **Salvează template**: Editează `prompt_minute.txt` cu instrucțiuni custom
4. **Batch processing**: Creează script care aplică pipeline la mai multe fișiere

---

## ⚖️ Licență
Open Source - Folosește liber!

## 🤝 Contribuții
Issues și pull requests bineveniți!
