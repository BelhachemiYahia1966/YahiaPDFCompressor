# YahiaPDFCompressor
![image alt](https://github.com/BelhachemiYahia1966/YahiaPDFCompressor/blob/950e8839d385085148adbd658fdeb2c866574efa/Yahblubre.jpg)
PDF compressor with a GUI Interface
# Yahia PDF Compressor

A graphical PDF compression tool that reduces PDF file sizes using Ghostscript with customizable compression levels.


![image alt](https://github.com/BelhachemiYahia1966/YahiaPDFCompressor/blob/f1e603d926fdfc14824745fe361a84108cc9c5b9/YahiaPDFCompressorimg.png)




## Features

- Intuitive GUI for easy PDF compression
- Multiple compression levels (Minimum to Maximum)
- Displays compression results including size reduction
- Cross-platform support (Windows, macOS, Linux)
- Option to open compressed file after completion

## Requirements

- Python 3.6 or higher
- Ghostscript (must be installed separately)
- Python packages listed in dependencies

## Installation

### 1. Install Python
If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/)

### 2. Install Ghostscript
The application requires Ghostscript to work (DON'T FORGET TO ADD bin FOLDER AFTER INSTALLATION TO YOUR PATH VARIABLES ):

- **Windows**: Download from [Ghostscript website](https://www.ghostscript.com/)
- **macOS**: `brew install ghostscript`
- **Linux (Debian/Ubuntu)**: `sudo apt install ghostscript`

### 3. Install Python Dependencies
Run the following command to install required Python packages:

```bash
pip install pillow tk
