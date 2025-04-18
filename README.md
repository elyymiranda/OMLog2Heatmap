# OpenMolcas Configuration Weight Analyzer

![Exemple: configuration_heatmap_root1_thres0 3](https://github.com/user-attachments/assets/358765d5-9f06-455a-b106-aaaa69b8dc32)

**A specialized Python tool for quantifying and visualizing electronic configuration weights from OpenMolcas calculations, with particular focus on analyzing static correlation effects across different molecular geometries.**

## Features

- Parses CI coefficients and weights from OpenMolcas log files
- Generates publication-quality heatmaps comparing configurations between geometries
- Automatically detects number of roots from input files
- Customizable configuration labels using LaTeX notation
- Calculates and displays energy differences between geometries
- Flexible threshold for coefficient filtering

## Requirements

- Python 3.6+
- Required packages:
  - pandas
  - seaborn
  - matplotlib

Install dependencies with:
```bash
pip install pandas seaborn matplotlib
```

## Usage

```bash
python OMLOG2Heatmap.py geo1=non_planar.log geo2=planar.log [thres=0.2]
```

## Parameters

| Parameter | Description                                   | Default |
|-----------|-----------------------------------------------|---------|
| `geo1`    | First geometry log file (required)            | -       |
| `geo2`    | Second geometry log file (required)           | -       |
| `thres`   | Minimum absolute CI coefficient value to include | 0.2    |

## Output Files

For each root, the script generates:

- config_weights_root{N}_thres{X}.txt - Text file with raw data
- configuration_heatmap_root{N}_thres{X}.png - Visualization heatmap

Where:

- {N} = root number (1-7 or as detected)
- {X} = threshold value used

## Customization

Edit in script:
```python
CONFIG_LABELS = {
    '2222222u000000': r'$\pi_1^*$',
    '222222200u0000': r'$\pi_3^*$'
}

GEOMETRY_NAMES = {
    'planar': 'p-NDP',
    'non-planar': 'NDP'
}
```
