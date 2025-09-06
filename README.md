# Virtual Keyboard

A customizable virtual keyboard built with Kivy, supporting multiple languages (English, Persian, Arabic, and Numbers) and themes (light/dark).

## Features
- Multi-language support (English, Persian, Arabic, Numbers)
- Light and dark themes with transparent backgrounds
- Glow effect on buttons for a modern look
- Smooth animations for opening/closing
- Customizable font and layout
- Responsive design for different screen sizes

## Installation
1. Install Python 3.8+.
2. Install Kivy: `pip install kivy`.
3. Download `Vazir.ttf` from [Vazir Font](https://github.com/rastikerdar/vazir-font/releases) and place it in the `fonts` directory.
4. Run the application: `python virtual_keyboard.py`.

## Usage
```bash
cd path/to/virtual-keyboard
python virtual_keyboard.py
```
Click the "Open Virtual Keyboard" button to display the keyboard.

## Requirements
- Kivy>=2.0.0
- Python>=3.8
- Vazir.ttf font (optional, falls back to Arial if not found)

## Directory Structure
```
virtual-keyboard/
├── fonts/
│   └── Vazir.ttf
├── virtual_keyboard.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
```

## Troubleshooting
If Persian text appears as squares:
- Ensure `Vazir.ttf` is in the `fonts` directory.
- Check console logs for font loading messages.
- Download a fresh copy of `Vazir.ttf` from [Vazir Font](https://github.com/rastikerdar/vazir-font/releases).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## GitHub Repository
https://github.com/aboutbehnam