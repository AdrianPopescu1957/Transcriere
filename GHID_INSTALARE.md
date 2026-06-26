# Ghid Simplu: Transcriere și Minute Ședințe

## Scop
Pe PC un flux minimal care:
1. Transcrie audio în limba română (ședință, discuție, interviu)
2. Generează minute structurate
3. Procesare locală, fără Internet
4. Generează minute structurate folosind Ollama

---

## Procedura în Varianta simplă: Whisper.cpp + Ollama

### 1. Instalezi Whisper.cpp

#### (a) Clonează repo-ul oficial Whisper.cpp:
```bash
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
```

#### (b) Compilează proiectul (pe Linux/macOS/Windows cu WSL):
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

#### (c) Descarcă modelul Whisper în limba română
Exemplu cu modelul "small" pentru echilibru între performanță și calitate:
```bash
./main -m models/ggml-small.bin -f audio.wav
```
Modele pre-antrenate: disponibile în repo oficial sau pe pagina oficială Whisper.cpp.

---

### 2. Instalezi Ollama + un model bun la rezumare (Mistral sau Phi-3)

#### (A) Clonează repo-ul Ollama:
```bash
git clone https://github.com/ollama/ollama.git
cd ollama
```

#### (B) Instaleaza mediul necesar

**Pentru Windows:**
- Instalează **Go** de pe https://go.dev/dl/ și asigură-te că apare în variabila de mediu `PATH`
- Instalează **CMake** de pe https://cmake.org/download/ și adaugă-l în `PATH`
- Instalează **Visual Studio Build Tools** de pe https://visualstudio.microsoft.com/downloads/
  - Selectează componenta „Desktop development with C++"
  - Deschide „Developer Command Prompt for VS"

**Pentru Linux/macOS:**
- Instalează Go, CMake și compilatorul C/C++ conform instrucțiunilor specifice

#### (C) Compilează și instaleaza Ollama:
```bash
make
sudo make install
```

#### (D) Descarcă și instaleaza modelul Mistral (sau Phi-2):
Conform instrucțiunilor din repo Ollama (modele preantrenate disponibile în repo sau pagina oficială).

---

## Fișier template: prompt_minute.txt

Salvează-l în directorul proiectului:

```
Transcrierea completă a unei ședințe în limba română se generează minutele ședinței cu următoarea structură:

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
```

---

## Flux de lucru recomandat

1. **Obții audio**: ședință/discuție în fișier `.wav`
2. **Transcriere** cu Whisper.cpp:
   ```bash
   ./whisper.cpp/main -m models/ggml-small.bin -f ședință.wav > transcriere.txt
   ```
3. **Generare minute** cu Ollama + prompt din `prompt_minute.txt`:
   - Trimite textul transcris + prompt la modelul local Mistral
   - Obții minutele structurate

---

## Notă
Procesare 100% locală, nu sunt necesare conturi online sau chei API.
