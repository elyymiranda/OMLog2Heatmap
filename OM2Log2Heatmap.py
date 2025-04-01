#!/usr/bin/env python3
"""
Script to analyze and visualize configuration weights from OpenMolcas log files.
Creates heatmaps comparing weights between two geometries for each root.
"""

import re
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Configuration to label mapping library - add new patterns here as needed
CONFIG_LABELS = {
    '2222222u000000': r'$\pi_1^*$',
    '222222200u0000': r'$\pi_3^*$',
    '22222220u00000': r'$\pi_2^*$',
    '22222u22000000': r'$\pi\pi_2^*$+$\pi_2^*$',
    '222222200000u0': r'$\pi_4^*$',
    '2222222000u000': r'$\sigma_{NO}^*$',
    '22222220000u00': r'$\sigma_{{CCl}_1}^*$',
    '2222222000000u': r'$\sigma_{{CCl}_2}^*$',
    # Add more mappings as needed
}

# Font settings for publication quality figures
plt.rcParams.update({
    'font.size': 12,            # Base font size
    'axes.titlesize': 14,       # Title font size
    'axes.labelsize': 12,       # Axis label font size
    'xtick.labelsize': 11,      # X-axis tick label size
    'ytick.labelsize': 11,      # Y-axis tick label size
    'legend.fontsize': 10,      # Legend font size
    'figure.titlesize': 14      # Figure title size
})

# Geometry name mapping - update if using different systems
GEOMETRY_NAMES = {
    'planar': 'p-NDP',
    'non-planar': 'NDP'
}

def detect_num_roots(log_file):
    """Detect the number of roots from the log file by searching for 'ciroot' line."""
    with open(log_file, 'r') as f:
        for line in f:
            if 'ciroot' in line.lower():
                try:
                    # Extract first number from line like "ciroot = 7 7 1"
                    num_roots = int(line.split()[2])
                    print(f"Detected {num_roots} roots in {log_file}")
                    return num_roots
                except (IndexError, ValueError):
                    print("Warning: Could not parse ciroot line, defaulting to 7 roots")
                    return 7
    print("Warning: No ciroot found in log file, defaulting to 7 roots")
    return  # Default if not found

def parse_ras_weights(log_file, threshold=0.2):
    """Parse configuration weights and energies from OpenMolcas log file for all roots"""
    num_roots = detect_num_roots(log_file)
    roots = {i: {'configs': {}, 'energy': None} for i in range(1, num_roots+1)}
    current_root = 0
    config_count = 0
    in_config_section = False
    
    with open(log_file, 'r') as f:
        for line in f:
            # Detect new root section and extract energy
            if "printout of CI-coefficients larger than" in line:
                current_root = int(line.split()[-1])
                in_config_section = True
                config_count = 0
                # The energy line comes right after the root declaration
                next_line = next(f)
                if "energy=" in next_line:
                    try:
                        energy = float(next_line.split()[1])
                        roots[current_root]['energy'] = energy
                    except (IndexError, ValueError):
                        print(f"  Could not parse energy for root {current_root}")
                print(f"\nFound coefficients for root {current_root}")
                continue
                
            # Parse configuration lines - more robust pattern
            if in_config_section and current_root > 0:
                # Skip lines that don't match the expected configuration pattern
                if not re.match(r'^\s*\d+\s+[\dud\*]+\s+[-\d.]+\s+[\d.]+', line.strip()):
                    continue
                    
                # Strict pattern matching for configurations
                match = re.match(r'^\s*(\d+)\s+([\dud\*]+)\s+([-\d.]+)\s+([\d.]+)', line.strip())
                if match:
                    conf_num = match.group(1)
                    conf = match.group(2)
                    # Additional validation - configuration strings should be exactly 14 characters
                    if len(conf) != 14:
                        continue
                    try:
                        coeff = float(match.group(3))
                        weight = float(match.group(4)) * 100  # Convert to percentage
                        if abs(coeff) >= threshold:  # Filter by coefficient threshold
                            roots[current_root]['configs'][conf] = weight
                            config_count += 1
                            print(f"  Config {config_count}: {conf} = {coeff:.3f} (weight={weight:.1f}%)")
                    except ValueError:
                        continue
                # Detect end of configuration section
                elif "Natural orbitals and occupation numbers" in line:
                    in_config_section = False
                elif "----" in line or "====" in line:
                    in_config_section = False
    
    return roots

def map_config_to_label(config):
    """
    Convert configuration string to pretty label using the library.
    
    Args:
        config: Configuration string from log file
    
    Returns:
        Pretty label if found in CONFIG_LABELS, otherwise original string
    """
    return CONFIG_LABELS.get(config, config)

def main():
    """
    Main function to parse arguments, process log files, and generate plots.
    """
    # Parse command line arguments in format key=value
    args = {}
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            args[key] = value
    
    # Check required arguments
    if 'geo1' not in args or 'geo2' not in args:
        print("Usage: python3 map3.py geo1=file1.log geo2=file2.log [thres=0.2]")
        sys.exit(1)
    
    # Get threshold value (default = 0.2)
    threshold = float(args.get('thres', 0.2))
    print(f"\nUsing coefficient threshold: {threshold}")
    
    # Get input files
    nonplanar_log = Path(args['geo1'])
    planar_log = Path(args['geo2'])

    # Validate input files exist
    for f in [nonplanar_log, planar_log]:
        if not f.exists():
            print(f"Error: File not found - {f}")
            sys.exit(1)

    # Parse data for both geometries
    print("\n=== PARSING LOG FILES ===")
    planar_roots = parse_ras_weights(planar_log, threshold)
    nonplanar_roots = parse_ras_weights(nonplanar_log, threshold)

    # Determine number of roots from parsed data
    num_roots = max(
        max(planar_roots.keys()) if planar_roots else 0,
        max(nonplanar_roots.keys()) if nonplanar_roots else 0
    )
    print(f"\nProcessing {num_roots} roots")

    # Create combined DataFrame and plots for each root
    for root in range(1, num_roots + 1):
        print(f"\n=== PROCESSING ROOT {root} ===")
        
        # Get configurations for this root
        planar_configs = planar_roots.get(root, {}).get('configs', {})
        nonplanar_configs = nonplanar_roots.get(root, {}).get('configs', {})
        all_confs = set(planar_configs.keys()).union(set(nonplanar_configs.keys()))
        
        if not all_confs:
            print(f"No configurations found for root {root} with |coefficient| >= {threshold}")
            continue
            
        # Create data table with pretty labels
        data = []
        for conf in all_confs:
            data.append({
                "Configuration": map_config_to_label(conf),
                f"{GEOMETRY_NAMES['planar']} (%)": planar_configs.get(conf, 0.0),
                f"{GEOMETRY_NAMES['non-planar']} (%)": nonplanar_configs.get(conf, 0.0)
            })

        print(f"\nSample data for root {root}:")
        print(data[:3])  # Print first 3 configurations
        
        try:
            df = pd.DataFrame(data)
            if "Configuration" not in df.columns:
                raise ValueError("'Configuration' column missing in DataFrame")
                
            df = df.set_index("Configuration")
            print(f"\nDataFrame for root {root}:")
            print(df.head())
            
            # Save to text file with energy information
            output_txt = f"config_weights_root{root}_thres{threshold}.txt"
            with open(output_txt, 'w') as f:
                # Write threshold information
                f.write(f"Coefficient threshold: |c| >= {threshold}\n")
                f.write(f"{GEOMETRY_NAMES['planar']} Energy (Hartree): {planar_roots.get(root, {}).get('energy', 'N/A')}\n")
                f.write(f"{GEOMETRY_NAMES['non-planar']} Energy (Hartree): {nonplanar_roots.get(root, {}).get('energy', 'N/A')}\n")
                planar_energy = planar_roots.get(root, {}).get('energy')
                nonplanar_energy = nonplanar_roots.get(root, {}).get('energy')
                if planar_energy and nonplanar_energy:
                    energy_diff = (nonplanar_energy - planar_energy) * 27.2114  # Convert to eV
                    f.write(f"Energy Difference (eV): {energy_diff:.4f}\n")
                f.write("\n")
                # Write configuration data
                df.to_csv(f, sep='\t', float_format="%.1f")
            
            print(f"Saved parsed data to: {output_txt}")

            # Generate heatmap if we have data
            if len(df) > 0:
                # Create figure with adjusted size
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Create heatmap with larger fonts
                sns.heatmap(
                    df,
                    cmap="YlOrRd",
                    annot=True,
                    fmt=".1f",
                    vmin=0,
                    vmax=100,
                    linewidths=0.5,
                    cbar_kws={'label': 'Weight (%)'},
                    ax=ax,
                    annot_kws={"size": 11}  # Larger annotation font
                )

                # Adjust font sizes
                ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)  # Larger y-axis labels
                ax.set_xticklabels(ax.get_xticklabels(), fontsize=12)  # Larger x-axis labels
                cbar = ax.collections[0].colorbar
                cbar.ax.tick_params(labelsize=11)
                cbar.ax.set_ylabel('Weight (%)', fontsize=12)

                # Adjust title and labels
                plt.title(f"Configuration Weight Comparison - Root {root}\n(|c| ≥ {threshold})",
                         pad=15, fontsize=14)
                plt.ylabel("Configuration", fontsize=12)
                plt.xlabel("")

                # Adjust layout to make more compact
                plt.tight_layout(pad=1.5)

                output_png = f"configuration_heatmap_root{root}_thres{threshold}.png"
                plt.savefig(output_png, dpi=300, bbox_inches='tight')
                print(f"Saved heatmap to: {output_png}")
                plt.close()
                
        except Exception as e:
            print(f"\nERROR processing root {root}: {str(e)}")
            continue

if __name__ == "__main__":
    main()
