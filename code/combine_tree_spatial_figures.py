#!/usr/bin/env python3
"""
Combine coalescent tree and spatial mapping figures side-by-side for presentation.
This script reads existing PNG files and creates combined visualizations.
"""

import os
import glob
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def combine_tree_spatial_figures(presentation_dir):
    """
    Combine coalescent tree and spatial mapping figures side-by-side.
    
    Args:
        presentation_dir: Path to the presentation directory
    """
    presentation_path = Path(presentation_dir)
    coalescent_dir = presentation_path / "coalescent_trees"
    spatial_dir = presentation_path / "spatial_mapping"
    output_dir = presentation_path / "combined_figures"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Find all coalescent tree images
    coalescent_images = sorted(glob.glob(str(coalescent_dir / "coalescent_tree_*.png")))
    
    if not coalescent_images:
        print("No coalescent tree images found!")
        return
    
    print(f"Found {len(coalescent_images)} coalescent tree images")
    
    for coalescent_path in coalescent_images:
        # Extract patient UUID from filename
        filename = Path(coalescent_path).name
        uuid = filename.replace("coalescent_tree_", "").replace(".png", "")
        
        # Find corresponding spatial mapping image
        spatial_path = spatial_dir / f"spatial_mapping_{uuid}.png"
        
        if not spatial_path.exists():
            print(f"Warning: No spatial mapping found for {uuid}")
            continue
        
        print(f"Processing patient {uuid}...")
        
        # Load images
        try:
            tree_img = mpimg.imread(coalescent_path)
            spatial_img = mpimg.imread(str(spatial_path))
        except Exception as e:
            print(f"Error loading images for {uuid}: {e}")
            continue
        
        # Create side-by-side figure
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        
        # Display coalescent tree on the left
        axes[0].imshow(tree_img)
        axes[0].axis('off')
        
        # Display spatial mapping on the right
        axes[1].imshow(spatial_img)
        axes[1].axis('off')
        
        # Add patient UUID as overall title
        fig.suptitle(f'Patient: {uuid}', fontsize=14, y=0.98, fontweight='bold')
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for suptitle
        
        # Save combined figure
        output_path = output_dir / f"combined_{uuid}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"  ✓ Saved: {output_path}")
    
    print(f"\n✅ Combined figures saved to: {output_dir}")
    print(f"   Total combined figures: {len(glob.glob(str(output_dir / 'combined_*.png')))}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        presentation_dir = sys.argv[1]
    else:
        # Default to presentation directory in results
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        presentation_dir = project_root / "results" / "presentation"
    
    combine_tree_spatial_figures(presentation_dir)

