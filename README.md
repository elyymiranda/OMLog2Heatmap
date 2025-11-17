# OpenMolcas Configuration Weight Analyzer

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![OpenMolcas](https://img.shields.io/badge/OpenMolcas-compatible-green.svg)](https://www.molcas.org/)

![Example: configuration_heatmap_root1_thres0.3](https://github.com/user-attachments/assets/358765d5-9f06-455a-b106-aaaa69b8dc32)

**A specialized Python tool for quantifying and visualizing electronic configuration weights from OpenMolcas calculations, with particular focus on analyzing static correlation effects across different molecular geometries.**

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Parameters](#parameters)
- [Output Files](#output-files)
- [Customization](#customization)
- [Example Workflow](#example-workflow)
- [Citation](#citation)
- [License](#license)

---

## Introduction

This tool automates the extraction and visualization of CI (Configuration Interaction) coefficients and weights from OpenMolcas log files. It is particularly useful for:

- **Comparing electronic structures** between different molecular geometries
- **Analyzing static correlation effects** in multi-configurational calculations
- **Identifying dominant configurations** in CASSCF/RASSCF wavefunctions
- **Visualizing configuration changes** across potential energy surfaces

The tool generates publication-quality heatmaps that make it easy to identify which electronic configurations are important for each electronic state and how they vary between geometries.

---

## Features

- **Automatic parsing**: Extracts CI coefficients and weights from OpenMolcas log files
- **Publication-quality heatmaps**: Generates professional visualizations comparing configurations between geometries
- **Multi-root support**: Automatically detects and processes all roots from input files
- **LaTeX labels**: Customizable configuration labels using LaTeX notation for professional figures
- **Energy analysis**: Calculates and displays energy differences between geometries
- **Flexible filtering**: Adjustable threshold for coefficient filtering to focus on dominant configurations
- **Easy customization**: Simple dictionary-based configuration for labels and geometry names

---

## Requirements

- **Python 3.6+**
- Required Python packages:
  - `pandas` - Data manipulation and analysis
  - `seaborn` - Statistical data visualization
  - `matplotlib` - Plotting library

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/elyymiranda/OMLog2Heatmap.git
cd OMLog2Heatmap
```

2. **Install dependencies:**
```bash
pip install pandas seaborn matplotlib
```

3. **Make the script executable (optional):**
```bash
chmod +x OM2Log2Heatmap.py
```

---

## Usage

Basic usage with default threshold (0.2):
```bash
python OM2Log2Heatmap.py geo1=non_planar.log geo2=planar.log
```

Custom threshold:
```bash
python OM2Log2Heatmap.py geo1=non_planar.log geo2=planar.log thres=0.15
```

---

## Parameters

| Parameter | Description                                        | Default | Required |
|-----------|----------------------------------------------------|---------|----------|
| `geo1`    | First geometry OpenMolcas log file                | -       | Yes      |
| `geo2`    | Second geometry OpenMolcas log file               | -       | Yes      |
| `thres`   | Minimum absolute CI coefficient value to include  | 0.2     | No       |

**Notes:**
- Log files must be from OpenMolcas CASSCF/RASSCF calculations
- Both files should have the same active space for meaningful comparisons
- Lower threshold values include more configurations but may clutter visualizations
- Higher threshold values focus on the most important configurations

---

## Output Files

For each root detected, the script generates two files:

1. **Text file**: `config_weights_root{N}_thres{X}.txt`
   - Contains raw configuration weights data
   - Tabular format with configuration strings and weights for each geometry
   - Includes energy differences

2. **Heatmap**: `configuration_heatmap_root{N}_thres{X}.png`
   - Visual representation of configuration weights
   - Color-coded for easy identification of dominant configurations
   - Includes geometry labels and energy differences

Where:
- `{N}` = root number (1, 2, 3, ...)
- `{X}` = threshold value used (e.g., 0.2, 0.15)

---

## Customization

The script can be easily customized by editing the configuration dictionaries:

### Configuration Labels

Use LaTeX notation for professional-looking labels:

```python
CONFIG_LABELS = {
    '2222222u000000': r'$\pi_1^*$',
    '222222200u0000': r'$\pi_3^*$',
    '22222220u00000': r'$\pi_2^*$',
    # Add more configurations as needed
}
```

### Geometry Names

Customize how geometries appear in the output:

```python
GEOMETRY_NAMES = {
    'planar': 'p-NDP',
    'non-planar': 'NDP',
    'optimized': 'Opt',
    'twisted': 'Twisted'
}
```

---

## Example Workflow

### Step 1: Run OpenMolcas Calculations

Perform CASSCF/RASSCF calculations for your geometries of interest and save the log files.

### Step 2: Run the Analyzer

```bash
python OM2Log2Heatmap.py geo1=geometry1.log geo2=geometry2.log thres=0.15
```

### Step 3: Examine Output

- Check the `.txt` files for numerical data
- Review the `.png` heatmaps for visual analysis
- Identify dominant configurations and their variations between geometries

### Step 4: Customize (Optional)

Edit the script to add custom labels for your specific configurations and geometry names.

---

## Citation

If you use this tool in your research, please cite this repository:

```bibtex
@software{omlog2heatmap,
  author = {Miranda, Ely},
  title = {OpenMolcas Configuration Weight Analyzer},
  year = {2025},
  url = {https://github.com/elyymiranda/OMLog2Heatmap}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

## Acknowledgments

This tool was developed for analyzing multi-configurational wavefunctions in the context of photochemistry and excited state dynamics research.
