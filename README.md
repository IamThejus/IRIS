
# IRIS — Infra-Red Based Intelligent System

An AI-powered local-first smart home assistant capable of controlling real-world appliances using infrared communication, voice interaction, and realtime interfaces.

---

## Overview

IRIS (Infra-Red Based Intelligent System) is an advanced smart home ecosystem that combines:

- Embedded Systems
- Infrared Automation
- Voice AI
- Local Speech Processing
- Realtime Web Technologies
- Mobile Application Development

The project integrates custom-built hardware with a modern AI software stack to create a futuristic assistant capable of controlling appliances such as:

- Air Conditioners
- Smart Fans
- TVs
- Other IR-Based Devices

using:

- Voice Commands
- Mobile Controls
- Web Interfaces
- AI-Assisted Conversations

IRIS is inspired by futuristic assistants like JARVIS while focusing heavily on:

- Local-first Architecture
- Privacy
- Low Latency
- Embedded Intelligence
- Realtime Control
- Modularity

---

# Features

## AI Voice Assistant

- Wake-word activation using Porcupine
- Speech-to-text using Faster Whisper
- AI conversational responses
- Natural voice output using Piper TTS

---

## Smart Appliance Control

Supports:

- AC Control
- Fan Control
- IR-Based Appliance Automation

Capabilities include:

- Power Control
- Temperature Control
- Fan Speed Adjustment
- Mode Switching
- Boost Mode

---

## Infrared Automation System

Custom IR hardware layer built using:

- Raspberry Pi Pico 2W
- TSOP1738 IR Receiver
- IR LED Transmitter
- 2N2222 Transistor Amplification Circuit

Supports:

- IR Signal Learning
- IR Signal Transmission
- Universal Remote Style Control

---

## Realtime Web Interface

Built using:

- FastAPI
- WebSockets
- HTML/CSS/JavaScript

Features:

- Live Assistant States
- Animated AI Orb
- Conversation Logs
- Realtime Synchronization

---

## Flutter Mobile Application

The Android mobile application is built using Flutter.

Features:

- Device Dashboard
- Smart Remote Interfaces
- AC Controller UI
- Fan Controller UI
- Appliance Status Monitoring

IRIS is the successor of the earlier project **Remote X**, evolving from a smart IR remote system into a complete AI-powered smart home ecosystem.

---

# System Architecture

```text
                ┌─────────────────────┐
                │     User Voice      │
                └─────────┬───────────┘
                          │
                          ▼
               ┌─────────────────────┐
               │ Wake Word Detection │
               │     Porcupine       │
               └─────────┬───────────┘
                          │
                          ▼
               ┌─────────────────────┐
               │ Speech Recognition  │
               │   Faster Whisper    │
               └─────────┬───────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
   ┌────────────────┐         ┌────────────────┐
   │ IoT Commands   │         │ AI Conversation│
   └──────┬─────────┘         └──────┬─────────┘
          │                           │
          ▼                           ▼
 ┌──────────────────┐       ┌──────────────────┐
 │ IR Transmission  │       │ Groq LLM Engine  │
 └────────┬─────────┘       └────────┬─────────┘
          │                           │
          ▼                           ▼
 ┌──────────────────┐       ┌──────────────────┐
 │ Appliance Control│       │ Piper Voice TTS  │
 └──────────────────┘       └──────────────────┘
````

---

# Hardware Components

## Main Controller

* Raspberry Pi Pico 2W

---

## IR Receiver

### TSOP1738 IR Receiver Module

Used for:

* Reading Remote Signals
* Capturing IR Protocols
* Learning Appliance Commands

---

## IR Transmitter

* IR LED
* 2N2222 Transistor Driver Circuit

Used for:

* High-Power IR Transmission
* Appliance Communication
* Remote Emulation

---

## Additional Components

* Breadboard
* Jumper Wires
* Li-ion Battery Input
* USB Power Supply

---

# Software Stack

| Layer               | Technology           |
| ------------------- | -------------------- |
| Backend             | Python + FastAPI     |
| AI Engine           | Groq LLM             |
| Speech Recognition  | Faster Whisper       |
| Wake Word           | Porcupine            |
| Voice Output        | Piper TTS            |
| Frontend            | HTML/CSS/JavaScript  |
| Mobile App          | Flutter              |
| Communication       | WebSocket + HTTP     |
| Embedded Controller | Raspberry Pi Pico 2W |

---

# Folder Structure

```text
IRIS/
│
├── main.py
├── ai_engine.py
├── api_calls.py
├── settings.py
├── voice.py
├── iris_system_prompt.py
│
├── web_ui/
│   └── index.html
│
├── hardware/
│   ├── IR Receiver Setup
│   ├── IR Blaster Setup
│   └── Circuit Diagrams
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/IamThejus/IRIS.git
cd IRIS
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Porcupine

Add:

* Porcupine Access Key
* Wake Word Model

inside:

```python
settings.py
```

---

## Configure Groq API

```python
GROQ_API_KEY = "YOUR_API_KEY"
```

---

## Run IRIS

```bash
python main.py
```

---

# Web Interface

After startup:

```text
http://localhost:8000
```

---

# Mobile Application

The Flutter application provides:

* Smart Home Dashboard
* Appliance Management
* Realtime Remote Control
* Device Monitoring

---

# Current Capabilities

## Supported Devices

* LG AC
* Atomberg Smart Fan

---

## Supported Commands

### Fan

* Turn On/Off Fan
* Increase Speed
* Decrease Speed
* Boost Mode

### AC

* Turn On/Off AC
* Increase Temperature
* Decrease Temperature
* Change Modes

---

# Future Roadmap

## Planned Features

* Full Offline LLM Integration
* MQTT Support
* Device Discovery
* Automation Engine
* Room-Based Intelligence
* IR Learning Mode
* Multi-Device Synchronization
* Sensor Integration
* Computer Vision
* Home Assistant Integration

---

# Project Vision

IRIS aims to become a fully local-first intelligent smart home ecosystem capable of understanding, automating, and interacting with real-world environments naturally.

The project focuses on:

* Privacy
* Low Latency
* Offline Capability
* Embedded AI
* Universal Appliance Compatibility

---

# Inspiration

Inspired by:

* JARVIS
* Smart Home Ecosystems
* Edge AI Systems
* Local-First Computing

---

# Creators

Built by:

* Thejus Asokan

---

# License

MIT License

