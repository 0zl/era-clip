# EraClip

<img align="right" src="images/0.png" width="200" style="margin: 0 0 20px 20px;">

A **simple clipboard translator** for Era games. Just copy text and get instant English translations via DeepL - *no more suffering through moonrunes while dating Reimu!*

**[Download Latest Release](https://github.com/0zl/era-clip/releases/latest/download/EraClip.exe)**

## Features

- Real-time clipboard monitoring & translation
- Language detection (JP/CN/KR)
- High-quality DeepL translations
- Smart caching to reduce API calls
- Always-on-top with transparency options
- Clean UI that doesn't butcher CJK text
- Works with all Era games *(just enable Copy to Clipboard!)*
- Bugs. More bugs.

*Built with love for `/hgg/` and `/egg/`. Feel free to contribute or whatever.*

## Why Though?

Other Era game translators are too complex for my taste. I just wanted something dead simple and quick *(and probably shittier version)*. Plus, I needed an excuse to learn Python.

## How To Use

1. Get your **DeepL API Key** first:
   - Sign up at [DeepL API Free](https://www.deepl.com/pro-api)
   - Copy your Authentication Key

2. Run the compiled version:
   - Download the latest release
   - Run `EraClip.exe`
   - Paste your DeepL API Key in Settings tab
   - Enable Copy to Clipboard in your Era game
   - Start translator.

3. Run from source:
   ```bash
   git clone https://github.com/0zl/era-clip
   cd era-clip
   pip install -r requirements.txt
   python main.py
   ```

## Why this is detected as a Virus?!

**TL;DR.** False-Positive.

Windows Defender and friends might get mad and become *Tsundere* to this tool. Here's why:
- It uses goofy Windows API calls to monitor your clipboard
- It create *ghost window* runs in the background like a sus program to capture clipboard event
- It's compiled with Nuitka. *(PyInstaller alternative)*
- It reads/writes files on your system for config and caching translations

If you're paranoid:
1. Check the source code (it's all here!)
2. Build it yourself
3. Run via Python instead of using compiled binary
4. Or just use something else.

I don't know how to workaround this, it's open source, feels free to improve the software.
