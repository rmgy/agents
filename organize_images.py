#!/usr/bin/env python3
"""
SCARCITY TRAP - IMAGE ORGANIZATION SCRIPT
Organizes generated images into scene-based folder structure
"""

import os
import shutil
import sys
from pathlib import Path

# Configuration
SOURCE_DIR = input("Enter source directory with generated images (or press Enter for current): ").strip()
if not SOURCE_DIR:
    SOURCE_DIR = "."

DEST_BASE = "/tmp/scarcity-trap-production/scenes"  # Change this path as needed

# Asset mapping: prompt number -> (scene, category)
ASSET_MAP = {
    # Scene 1: Definition
    1: ("Scene-01-Definition", "characters"),
    11: ("Scene-01-Definition", "characters"),
    19: ("Scene-01-Definition", "backgrounds"),
    30: ("Scene-01-Definition", "objects"),
    32: ("Scene-01-Definition", "objects"),
    55: ("Scene-01-Definition", "text"),
    61: ("Scene-01-Definition", "text"),
    63: ("Scene-01-Definition", "motion-effects"),

    # Scene 2: Limited Resources
    2: ("Scene-02-Limited-Resources", "characters"),
    12: ("Scene-02-Limited-Resources", "characters"),
    20: ("Scene-02-Limited-Resources", "backgrounds"),
    27: ("Scene-02-Limited-Resources", "objects"),  # 3x copies
    28: ("Scene-02-Limited-Resources", "objects"),
    39: ("Scene-02-Limited-Resources", "data-viz"),
    56: ("Scene-02-Limited-Resources", "text"),
    64: ("Scene-02-Limited-Resources", "motion-effects"),

    # Scene 3: Decision Bandwidth
    3: ("Scene-03-Decision-Bandwidth", "characters"),
    29: ("Scene-03-Decision-Bandwidth", "objects"),
    32: ("Scene-03-Decision-Bandwidth", "objects"),  # Reuse
    33: ("Scene-03-Decision-Bandwidth", "objects"),
    40: ("Scene-03-Decision-Bandwidth", "data-viz"),
    43: ("Scene-03-Decision-Bandwidth", "data-viz"),
    57: ("Scene-03-Decision-Bandwidth", "text"),
    60: ("Scene-03-Decision-Bandwidth", "text"),
    65: ("Scene-03-Decision-Bandwidth", "motion-effects"),
    66: ("Scene-03-Decision-Bandwidth", "motion-effects"),
    48: ("Scene-03-Decision-Bandwidth", "objects"),
    25: ("Scene-03-Decision-Bandwidth", "backgrounds"),

    # Scene 4: Poor Trap
    4: ("Scene-04-Poor-Trap", "characters"),
    22: ("Scene-04-Poor-Trap", "backgrounds"),
    26: ("Scene-04-Poor-Trap", "objects"),
    35: ("Scene-04-Poor-Trap", "objects"),  # 2x copies
    31: ("Scene-04-Poor-Trap", "objects"),
    41: ("Scene-04-Poor-Trap", "data-viz"),
    44: ("Scene-04-Poor-Trap", "data-viz"),
    68: ("Scene-04-Poor-Trap", "motion-effects"),
    67: ("Scene-04-Poor-Trap", "motion-effects"),
    58: ("Scene-04-Poor-Trap", "text"),

    # Scene 5: Cognitive Capacity
    5: ("Scene-05-Cognitive-Capacity", "characters"),
    13: ("Scene-05-Cognitive-Capacity", "characters"),
    19: ("Scene-05-Cognitive-Capacity", "backgrounds"),  # Reuse
    39: ("Scene-05-Cognitive-Capacity", "data-viz"),  # Reuse
    42: ("Scene-05-Cognitive-Capacity", "data-viz"),
    45: ("Scene-05-Cognitive-Capacity", "data-viz"),
    36: ("Scene-05-Cognitive-Capacity", "objects"),
    33: ("Scene-05-Cognitive-Capacity", "objects"),  # Reuse
    60: ("Scene-05-Cognitive-Capacity", "text"),  # Reuse
    65: ("Scene-05-Cognitive-Capacity", "motion-effects"),  # Reuse

    # Scene 6: Quality of Life
    6: ("Scene-06-Quality-of-Life", "characters"),
    47: ("Scene-06-Quality-of-Life", "objects"),
    48: ("Scene-06-Quality-of-Life", "objects"),  # Reuse
    49: ("Scene-06-Quality-of-Life", "objects"),
    50: ("Scene-06-Quality-of-Life", "objects"),
    51: ("Scene-06-Quality-of-Life", "objects"),
    35: ("Scene-06-Quality-of-Life", "objects"),  # Reuse
    38: ("Scene-06-Quality-of-Life", "objects"),
    21: ("Scene-06-Quality-of-Life", "backgrounds"),
    64: ("Scene-06-Quality-of-Life", "motion-effects"),  # Reuse
    59: ("Scene-06-Quality-of-Life", "text"),

    # Scene 7: Scarcity Mindset
    7: ("Scene-07-Scarcity-Mindset", "characters"),
    15: ("Scene-07-Scarcity-Mindset", "characters"),
    26: ("Scene-07-Scarcity-Mindset", "backgrounds"),
    19: ("Scene-07-Scarcity-Mindset", "backgrounds"),  # Reuse
    34: ("Scene-07-Scarcity-Mindset", "objects"),
    37: ("Scene-07-Scarcity-Mindset", "objects"),
    66: ("Scene-07-Scarcity-Mindset", "motion-effects"),  # Reuse
    63: ("Scene-07-Scarcity-Mindset", "motion-effects"),  # Reuse
    57: ("Scene-07-Scarcity-Mindset", "text"),  # Reuse
    46: ("Scene-07-Scarcity-Mindset", "data-viz"),

    # Scene 8: Poor Decisions
    8: ("Scene-08-Poor-Decisions", "characters"),
    31: ("Scene-08-Poor-Decisions", "objects"),  # Reuse
    32: ("Scene-08-Poor-Decisions", "objects"),  # Reuse
    33: ("Scene-08-Poor-Decisions", "objects"),  # Reuse
    34: ("Scene-08-Poor-Decisions", "objects"),  # Reuse
    41: ("Scene-08-Poor-Decisions", "data-viz"),  # Reuse
    39: ("Scene-08-Poor-Decisions", "data-viz"),  # Reuse
    25: ("Scene-08-Poor-Decisions", "backgrounds"),  # Reuse
    68: ("Scene-08-Poor-Decisions", "motion-effects"),  # Reuse
    56: ("Scene-08-Poor-Decisions", "text"),  # Reuse
    60: ("Scene-08-Poor-Decisions", "text"),  # Reuse

    # Scene 9: Consequences
    9: ("Scene-09-Consequences", "characters"),
    23: ("Scene-09-Consequences", "backgrounds"),
    33: ("Scene-09-Consequences", "objects"),  # Reuse
    36: ("Scene-09-Consequences", "objects"),  # Reuse (2x)
    37: ("Scene-09-Consequences", "objects"),  # Reuse
    63: ("Scene-09-Consequences", "motion-effects"),  # Reuse
    65: ("Scene-09-Consequences", "motion-effects"),  # Reuse
    67: ("Scene-09-Consequences", "motion-effects"),  # Reuse
    40: ("Scene-09-Consequences", "data-viz"),
    42: ("Scene-09-Consequences", "data-viz"),  # Reuse
    58: ("Scene-09-Consequences", "text"),  # Reuse
    69: ("Scene-09-Consequences", "objects"),

    # Scene 10: Path Forward
    10: ("Scene-10-Path-Forward", "characters"),
    24: ("Scene-10-Path-Forward", "backgrounds"),
    29: ("Scene-10-Path-Forward", "objects"),  # Reuse
    36: ("Scene-10-Path-Forward", "objects"),  # Reuse
    46: ("Scene-10-Path-Forward", "data-viz"),  # Reuse
    68: ("Scene-10-Path-Forward", "motion-effects"),  # Reuse
    67: ("Scene-10-Path-Forward", "motion-effects"),  # Reuse
    50: ("Scene-10-Path-Forward", "objects"),  # Reuse
    62: ("Scene-10-Path-Forward", "text"),

    # Reusable assets
    69: ("assets/color-palette", "palettes"),
    70: ("assets/color-palette", "palettes"),
    71: ("assets/characters/details", "details"),
    72: ("assets/characters/details", "details"),
    73: ("assets/characters/details", "details"),
    74: ("assets/characters/details", "details"),
    75: ("assets/characters/details", "details"),
}

def organize_images():
    """Move generated images to proper scene folders"""

    source_path = Path(SOURCE_DIR)

    if not source_path.exists():
        print(f"❌ Source directory not found: {SOURCE_DIR}")
        return False

    # Get all PNG files
    image_files = list(source_path.glob("*.png")) + list(source_path.glob("*.jpg"))

    if not image_files:
        print(f"⚠️  No image files found in {SOURCE_DIR}")
        return False

    print(f"\n📁 Found {len(image_files)} image files")
    print(f"📍 Destination base: {DEST_BASE}\n")

    organized_count = 0
    skipped_count = 0

    for image_file in sorted(image_files):
        # Extract prompt number from filename
        # Expected format: Prompt-XX-... or similar
        filename = image_file.name

        try:
            # Try to extract prompt number
            if filename.startswith("Prompt-"):
                prompt_num = int(filename.split("-")[1])
            else:
                # Try alternative naming
                parts = filename.replace(".png", "").replace(".jpg", "").split("-")
                if parts[0].isdigit():
                    prompt_num = int(parts[0])
                else:
                    print(f"⚠️  Skipping {filename} - cannot parse prompt number")
                    skipped_count += 1
                    continue

            # Get scene and category from mapping
            if prompt_num not in ASSET_MAP:
                print(f"⚠️  Skipping Prompt-{prompt_num} - not in mapping")
                skipped_count += 1
                continue

            scene, category = ASSET_MAP[prompt_num]
            dest_dir = Path(DEST_BASE) / scene / category

            # Create destination directory
            dest_dir.mkdir(parents=True, exist_ok=True)

            # Copy file
            dest_file = dest_dir / filename
            shutil.copy2(image_file, dest_file)

            print(f"✓ {filename:60} → {scene}/{category}/")
            organized_count += 1

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            skipped_count += 1

    print(f"\n✅ Organized: {organized_count} files")
    print(f"⚠️  Skipped: {skipped_count} files")
    print(f"📁 Destination: {DEST_BASE}")

    return True

def generate_summary():
    """Generate summary of organized assets"""

    summary_file = Path(DEST_BASE).parent / "ORGANIZATION_SUMMARY.txt"

    with open(summary_file, 'w') as f:
        f.write("SCARCITY TRAP - IMAGE ORGANIZATION SUMMARY\n")
        f.write("=" * 60 + "\n\n")

        # Count files per scene
        scenes_dir = Path(DEST_BASE)
        for scene_dir in sorted(scenes_dir.glob("Scene-*")):
            total_files = len(list(scene_dir.rglob("*.*")))
            f.write(f"{scene_dir.name}: {total_files} files\n")

            # List categories
            for category_dir in sorted(scene_dir.iterdir()):
                if category_dir.is_dir():
                    cat_files = len(list(category_dir.glob("*.*")))
                    f.write(f"  └─ {category_dir.name}: {cat_files} files\n")

    print(f"\n📝 Summary saved to: {summary_file}")

if __name__ == "__main__":
    if organize_images():
        generate_summary()
        print("\n✨ Organization complete! Ready for After Effects import.")
    else:
        sys.exit(1)
