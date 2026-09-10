# FLASED

FLASED is a desktop flashcard app built for active recall. It uses Python, PySide6, SQLite, and Google Gemini to turn your notes into flashcards and help you review them.

## Features

* Generate flashcards from your notes using Gemini
* First-letter mnemonic codes for easier recall
* Adaptive review system with **Again**, **Hard**, and **Easy**
* Organize cards into Subjects and Modules
* Search, edit, add, and delete cards
* Track Gemini API usage and quota
* Dark-themed PySide6 desktop interface
* Build as a standalone Windows `.exe`

## Tech Stack

* Python
* PySide6
* Google Gemini API
* Pydantic
* SQLite
* PyInstaller

## Setup

```bash
git clone https://github.com/6sceed/Flased
cd flased
pip install PySide6 google-genai pydantic
python app.py
```

Add your Gemini API key through the app or set `GEMINI_API_KEY` as an environment variable.

## Keyboard Shortcuts

| Key     | Action        |
| ------- | ------------- |
| `Space` | Reveal answer |
| `1`     | Again         |
| `2`     | Hard          |
| `3`     | Easy          |
| `Esc`   | Exit session  |

## Build

```bash
python -m PyInstaller FLASED.spec
```

The executable will be created in `dist/FLASED.exe`.

## Images
![Dashboard](https://github.com/6sceed/Flased/blob/main/flased/build/FLASED/images/7.png?raw=true)

![Review](https://github.com/6sceed/Flased/blob/main/flased/build/FLASED/images/3.png?raw=true)

![Flashcard Browser](https://github.com/6sceed/Flased/blob/main/flased/build/FLASED/images/4.png?raw=true)

![Completed Session](https://github.com/6sceed/Flased/blob/main/flased/build/FLASED/images/1.png?raw=true)
