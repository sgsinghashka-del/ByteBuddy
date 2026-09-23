# ByteBuddy

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-1.28-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img alt="Hugging Face" src="https://img.shields.io/badge/HuggingFace-Inference-FFD21F?style=for-the-badge&logo=huggingface&logoColor=black" />
  <img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" />
</p>

<p align="center">
  <img src="docs/screenshots/bytebuddy-dashboard.png" alt="ByteBuddy app dashboard" width="1100" />
</p>

ByteBuddy is a local-first AI assistant for fast experimentation, idea generation, and product prototyping using open-source language models from Hugging Face.

Built for founders, builders, and teams who want a clean AI workspace without the overhead of a heavy platform.

## Why ByteBuddy?

- Modern, startup-ready interface
- Local-first workflow with secure token handling
- Open-source model switching for experimentation
- Lightweight setup and fast iteration
- Built for prompt testing and product ideation

## Features

- ⚡ Fast AI chat experience
- 🤖 Switch between multiple Hugging Face models
- 🔧 Tune temperature, top-p, and output length
- 🧠 Great for prompt testing and iteration
- 🔒 Keep your workflow private and local
- 🎨 Light-mode product aesthetic for polished demos

## Quick start

```bash
git clone https://github.com/sgsinghashka-del/ByteBuddy.git
cd ByteBuddy
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## Environment

Create a `.env` file in the project root:

```env
HF_TOKEN=your_huggingface_token_here
```

## Screenshots

These screenshots are intended to reflect the real app experience rather than static mockups.

```bash
streamlit run app.py
python capture_screenshots.py
```

Generated files:

- `docs/screenshots/bytebuddy-dashboard.png`
- `docs/screenshots/bytebuddy-chat.png`

## Project structure

```text
ByteBuddy/
├── app.py
├── config.py
├── utils.py
├── requirements.txt
├── capture_screenshots.py
├── .env.example
├── README.md
├── docs/
│   └── screenshots/
│       ├── bytebuddy-dashboard.png
│       └── bytebuddy-chat.png
└── .gitignore
```

## Supported models

- Mistral-7B-Instruct-v0.2
- Llama-2-7b-chat-hf
- Zephyr-7b-beta
- Falcon-7b-instruct

## License

MIT
