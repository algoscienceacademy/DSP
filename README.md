# Digital Signal Processing (DSP) Learning Suite

A comprehensive suite of interactive DSP applications designed for different skill levels. This project provides hands-on experience with digital signal processing concepts through visual and interactive tools.

## Project Structure

```
aliasF/
├── Beginner/
│   ├── signalgui1.py
│   └── README.md
├── Intermediate/
│   ├── signalgui2.py
│   └── README.md
├── Expert/
│   ├── main.py
│   └── README.md
└── README.md
```

## Overview

This project offers three levels of DSP applications:
- **Beginner**: Basic signal sampling and quantization
- **Intermediate**: Advanced signal processing with FFT analysis
- **Expert**: Comprehensive DSP workbench with real-time analysis

## Requirements

- Python 3.8+
- PySide6
- NumPy
- Matplotlib
- SciPy
- Pandas (Expert level only)

## Installation

```bash
pip install PySide6 numpy matplotlib scipy pandas
```

## Quick Start

1. Clone the repository
2. Navigate to desired difficulty level
3. Run the corresponding Python file:
```bash
python signalgui1.py  # For beginner
python signalgui2.py  # For intermediate
python main.py        # For expert
```

# Project Setup Guide

## Virtual Environment Setup

1. Install Python 3.8 or higher if not already installed
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

## Required Packages

Install the following packages after activating your virtual environment:

```bash
pip install -r requirements.txt
```

Essential packages include:
- pip>=21.0.0
- setuptools>=45.0.0
- wheel>=0.37.0
- pytest>=6.0.0
- black>=22.0.0  # for code formatting
- flake8>=3.9.0  # for linting
- mypy>=0.910    # for type checking
- python-dotenv>=0.19.0  # for environment variables

## Features

### Common Features
- Interactive signal generation
- Real-time visualization
- Sampling and quantization
- Aliasing demonstration

### Level-specific Features
- **Beginner**: Basic DSP concepts
- **Intermediate**: FFT analysis, noise simulation
- **Expert**: Advanced filtering, PCM encoding, eye diagrams

## Contributing

Feel free to submit issues and enhancement requests.

## License

MIT License
