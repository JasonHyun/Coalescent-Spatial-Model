#!/usr/bin/env python3
"""
Standalone script to regenerate distribution plots from spatial mapping results JSON.
This allows regenerating plots without re-running the entire spatial mapping workflow.
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

def regenerate_distribution_plots(json_file, output_dir=None):
    """
    Regenerate distribution plots from spatial mapping results JSON.
    
    Args:
        json_file: Path to spatial_mapping_results.json
        output_dir: Directory to save plots (defaults to same directory as JSON)
    """
    # Load results
    with open(json_file, 'r') as f:
        results = json.load(f)
    
    # Extract successful results
    successful_results = [r for r in results if r.get('status') == 'success']
    
    if len(successful_results) == 0:
        print("❌ No successful results found in JSON file.")
        return
    
    # Extract metrics
    morans_i_values = []
    alpha_values = []
    beta_values = []
    
    for r in successful_results:
        metrics = r.get('spatial_metrics', {})
        if 'morans_i' in metrics:
            morans_i_values.append(metrics['morans_i'])
        if 'within_lineage_spread_alpha' in metrics:
            alpha_values.append(metrics['within_lineage_spread_alpha'])
        if 'founder_separation_beta' in metrics:
            beta_values.append(metrics['founder_separation_beta'])
    
    if len(alpha_values) == 0:
        print("❌ No alpha values found in results.")
        return
    
    # Determine output directory
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(json_file))
    
    print(f"📊 Regenerating distribution plots from {len(successful_results)} successful results...")
    print(f"   • Moran's I values: {len(morans_i_values)}")
    print(f"   • Alpha values: {len(alpha_values)}")
    print(f"   • Beta values: {len(beta_values)}")
    
    # Create 3-panel plot: alpha, beta, and Moran's I
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Alpha distribution
    axes[0].hist(alpha_values, bins=30, color='blue', alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Within-lineage Spread (α)', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].set_title('Distribution of Within-lineage Spread (α)', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # Beta distribution
    if len(beta_values) > 0:
        axes[1].hist(beta_values, bins=50, color='red', alpha=0.7, edgecolor='black')
        axes[1].axvline(np.mean(beta_values), color='blue', linestyle='--', linewidth=2, 
                      label=f'Mean: {np.mean(beta_values):.4f}')
        axes[1].axvline(np.median(beta_values), color='green', linestyle='--', linewidth=2, 
                      label=f'Median: {np.median(beta_values):.4f}')
        axes[1].set_xlabel('Founder Separation (β)', fontsize=12)
        axes[1].set_ylabel('Frequency', fontsize=12)
        axes[1].set_title('Distribution of Founder Separation (β)', fontsize=14, fontweight='bold')
        # Set x-axis to show most of the data (up to 0.2 covers ~99% of values)
        if np.percentile(beta_values, 95) < 0.2:
            axes[1].set_xlim(left=0, right=max(0.2, np.percentile(beta_values, 99)))
            axes[1].text(0.98, 0.95, f'Note: {sum(1 for b in beta_values if b >= 0.2)} values >= 0.2 (max={max(beta_values):.3f})', 
                       transform=axes[1].transAxes, fontsize=9, verticalalignment='top',
                       horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
    
    # Moran's I distribution
    if len(morans_i_values) > 0:
        axes[2].hist(morans_i_values, bins=30, color='purple', alpha=0.7, edgecolor='black')
        axes[2].set_xlabel("Moran's I", fontsize=12)
        axes[2].set_ylabel('Frequency', fontsize=12)
        axes[2].set_title("Distribution of Moran's I", fontsize=14, fontweight='bold')
        axes[2].grid(True, alpha=0.3)
    else:
        axes[2].text(0.5, 0.5, 'No Moran\'s I data available', 
                    ha='center', va='center', transform=axes[2].transAxes, fontsize=12)
        axes[2].set_title("Distribution of Moran's I", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    dist_plot_path = os.path.join(output_dir, "spatial_metrics_distributions.png")
    plt.savefig(dist_plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Distribution plots saved to: {dist_plot_path}")
    
    # Print summary statistics
    print("\n📊 Summary Statistics:")
    if len(morans_i_values) > 0:
        print(f"   Moran's I:")
        print(f"     Mean: {np.mean(morans_i_values):.4f}")
        print(f"     Median: {np.median(morans_i_values):.4f}")
        print(f"     Std Dev: {np.std(morans_i_values):.4f}")
        print(f"     Range: {np.min(morans_i_values):.4f} - {np.max(morans_i_values):.4f}")
    print(f"   Alpha:")
    print(f"     Mean: {np.mean(alpha_values):.4f}")
    print(f"     Median: {np.median(alpha_values):.4f}")
    print(f"     Std Dev: {np.std(alpha_values):.4f}")
    print(f"     Range: {np.min(alpha_values):.4f} - {np.max(alpha_values):.4f}")
    if len(beta_values) > 0:
        print(f"   Beta:")
        print(f"     Mean: {np.mean(beta_values):.4f}")
        print(f"     Median: {np.median(beta_values):.4f}")
        print(f"     Std Dev: {np.std(beta_values):.4f}")
        print(f"     Range: {np.min(beta_values):.4f} - {np.max(beta_values):.4f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: regenerate_distribution_plots.py <spatial_mapping_results.json> [output_directory]")
        print("\nExample:")
        print("  python regenerate_distribution_plots.py results/spatial_mapping/spatial_mapping_results.json")
        print("  python regenerate_distribution_plots.py results/spatial_mapping/spatial_mapping_results.json results/spatial_mapping")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(json_file):
        print(f"❌ Error: JSON file not found: {json_file}")
        sys.exit(1)
    
    regenerate_distribution_plots(json_file, output_dir)



