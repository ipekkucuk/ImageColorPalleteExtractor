# 🎨 ImageColorPaletteExtractor

ImageColorPaletteExtractor is a simple and effective Python tool that extracts the **most dominant colors** from a given image (JPEG or PNG). It uses **KMeans clustering** to identify key colors, while automatically filtering out **grayscale**, **too dark**, and **too light** pixels to ensure a clean and useful color palette. 

## 🧩 Features

- Accepts `.jpg` and `.png` image files
- User-defined number of dominant colors (**between 3 and 9**)
- Filters out:
  - Grayscale tones
  - Extremely dark or light pixels
- Detects if grayscale tones dominate the result and retries with stricter filters
- Displays:
  - Color palette as a horizontal visual bar (using Matplotlib)
  - HEX color codes in the terminal

## 📷 Example
🎨 Enter the name of the image (e.g sample.jpg): 2.jpg
How many colors do you want? (Enter a number between 3 and 9): 5

Top dominant colors (HEX):

1. #b26372
2. #633935
3. #7c495d
4. #3c2412
5. #da8083


Visual palette:

[Example Palette](https://imgur.com/a/7EuaJXc) 

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.x
- Libraries:
  - Pillow
  - numpy
  - matplotlib
  - scikit-learn

### 📦 Installation

Install required libraries via pip:
pip install pillow numpy matplotlib scikit-learn

