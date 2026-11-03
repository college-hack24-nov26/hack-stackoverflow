# AVAQ -AI visual assistance and querying 

# AVAQ – AI Visual Assistant

AVAQ is an AI-powered visual assistant that helps users understand their surroundings through a webcam and natural-language voice interaction.

Users can press and hold the Spacebar, ask a question about their surroundings, and release it. AVAQ processes the voice input, analyzes the current camera frame using a Vision-Language Model, and provides a text and spoken response.

## Features

* **Real-Time Camera:** Continuously displays webcam footage.
* **Push-to-Talk:** Hold Spacebar to record a question.
* **Speech Recognition:** Converts voice input into text using Faster Whisper.
* **Visual Understanding:** Uses Qwen3-VL to understand camera images and answer questions.
* **Natural Language Responses:** Generates contextual answers based on the user's question and current visual surroundings.
* **Text-to-Speech:** Speaks generated answers using pyttsx3.
* **Interactive Interface:** Simple webcam interface with keyboard controls.

## Project Architecture

```text
AVAQ
│
├── Webcam
│     │
│     └── Current Camera Frame
│
├── Spacebar Push-to-Talk
│     │
│     └── Microphone Recording
│
├── Faster Whisper
│     │
│     └── Speech-to-Text
│
├── Qwen3-VL
│     │
│     ├── Camera Image
│     └── Transcribed Question
│
├── AI Response
│     │
│     ├── Display Text
│     └── Text-to-Speech
│
└── AVAQ Response
```

## Technologies Used

| Technology     | Purpose                            |
| -------------- | ---------------------------------- |
| Python         | Core application development       |
| OpenCV         | Webcam access and image processing |
| Faster Whisper | Speech recognition                 |
| Qwen3-VL       | Vision-language understanding      |
| Ollama         | Local AI model execution           |
| pyttsx3        | Text-to-Speech                     |
| SoundDevice    | Microphone recording               |
| NumPy          | Audio processing                   |
| Keyboard       | Push-to-talk controls              |

## Project Structure

```text
hack-stackoverflow/
│
├── models/
│   └── yolo26n.pt
│
├── modules/
│   ├── __init__.py
│   ├── camera.py
│   ├── audio.py
│   ├── speech_recognition.py
│   ├── vision_ai.py
│   └── tts.py
│
├── test files/
│   └── test_tts.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

* Python 3.12
* Webcam
* Microphone
* Speakers or headphones
* Ollama
* Qwen3-VL model
* Windows operating system

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/hack-stackoverflow.git
cd hack-stackoverflow
```

### 2. Create Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Install Ollama

Download Ollama:

https://ollama.com/

### 5. Download Qwen3-VL

```powershell
ollama pull qwen3-vl:2b
```

Verify:

```powershell
ollama list
```

## Running AVAQ

Start the application:

```powershell
python main.py
```

### Interaction

1. AVAQ initializes the camera, microphone, speech recognition, and vision model.
2. The webcam displays a live camera feed.
3. Press and hold **SPACEBAR**.
4. Ask a question about your surroundings.
5. Release **SPACEBAR**.
6. AVAQ transcribes your question.
7. The current camera frame and transcribed question are sent to Qwen3-VL.
8. Qwen generates a natural-language response.
9. AVAQ displays and speaks the response.

### Example

**User:**

"What do you see in front of me?"

**AVAQ:**

"I can see two people standing in the room. There is also a table and a chair."

## Controls

| Key              | Action                                  |
| ---------------- | --------------------------------------- |
| SPACEBAR         | Hold to record a question               |
| Release SPACEBAR | Stop recording and process the question |
| ESC              | Exit AVAQ                               |

## AI Processing Pipeline

```text
Voice Input
    ↓
Faster Whisper
    ↓
Transcribed Question
    ↓
Camera Image + Question
    ↓
Qwen3-VL
    ↓
Natural Language Answer
    ↓
pyttsx3
    ↓
Spoken Response
```

## Future Improvements

* Natural neural voices such as Sarah.
* Improved speech recognition accuracy.
* Faster visual response generation.
* Continuous object detection using YOLO26.
* Object-aware assistive navigation.
* Visual assistance for people with visual impairments.
* Offline voice interaction.
* Improved user interface.
* Multilingual interaction.

## Project Goal

AVAQ aims to make visual information more accessible through conversational artificial intelligence, enabling users to ask questions about their surroundings and receive understandable responses.

## License

This project is intended for educational and hackathon purposes.
