# SCARCITY TRAP - COMPLETE PRODUCTION WORKFLOW
## From Generated Images to YouTube Upload

---

## PHASE 1: IMAGE ORGANIZATION (30-45 minutes)

### Step 1.1: Locate Generated Images
```
Location: C:\claude\multi-channel-content-engine\imageto video
Count: 75 PNG files
Status: ✓ Complete
```

### Step 1.2: Organize Into Folder Structure
**Option A: Automated (Python Script)**
```bash
python3 organize_images.py
```
- Source: `C:\claude\multi-channel-content-engine\imageto video`
- Destination: `/tmp/scarcity-trap-production/scenes/`
- Creates: 10 scene folders + 6 category folders per scene
- Time: 5-10 minutes

**Option B: Manual Organization**
- Follow structure in `ASSET_MAPPING.md`
- Move files to scene/category folders
- Time: 20-30 minutes

### Step 1.3: Verify Organization
```bash
ls -R scenes/ | less
# Should show:
# Scene-01-Definition/
#   ├── characters/
#   ├── backgrounds/
#   ├── objects/
#   ├── data-viz/
#   ├── motion-effects/
#   └── text/
```

---

## PHASE 2: AFTER EFFECTS PROJECT SETUP (1-2 hours)

### Step 2.1: Create New After Effects Project
1. Open After Effects
2. File → New → New Project
3. Save as: `Scarcity_Trap_Master.aep`
4. Set project settings:
   - Color Depth: 8-bit
   - Linear Color Space
   - Working Color Space: sRGB

### Step 2.2: Automate Composition Creation
**Method 1: Run ExtendScript (Easiest)**
```
In After Effects:
File → Scripts → Run Script File
Select: SETUP_COMPOSITIONS.jsx
```
This automatically creates:
- ✓ Master composition (14:00)
- ✓ 10 scene compositions
- ✓ Folder structure
- ⏱️ Duration: 2-3 minutes

**Method 2: Manual Creation**
- See `SCARCITY_TRAP_PROJECT_SETUP.md` for detailed steps
- ⏱️ Duration: 45-60 minutes

### Step 2.3: Configure Project Settings
```
Composition Settings (All Compositions):
├─ Resolution: 1920 x 1080
├─ Frame Rate: 23.976 fps
├─ Duration: [Scene-specific]
├─ Background: White (255, 255, 255)
└─ Pixel Aspect: Square
```

---

## PHASE 3: IMAGE IMPORT & ASSET ASSEMBLY (2-3 hours)

### Step 3.1: Import All Images
1. File → Import → Multiple Files
2. Select all 75 PNG files
3. Check: "Import as Composition" OFF
4. Set footage interpretation:
   - Alpha Channel: Straight (Unmatted)
   - Frame Rate: 23.976 fps

### Step 3.2: Organize Footage
```
Project Panel Structure:
├─ SCENE 01
│  ├─ BG - Workspace
│  ├─ CHAR - Neutral Sitting
│  ├─ OBJ - Lightbulb
│  ├─ OBJ - Checkmark
│  ├─ TEXT - SCARCITY
│  └─ FX - Radial Motion Lines
├─ SCENE 02
│  └─ [Similar structure]
├─ SCENE 03-10
└─ REUSABLE_ASSETS
   ├─ Characters
   ├─ Icons
   ├─ Data Viz Elements
   └─ Color Palette
```

### Step 3.3: Import Into Scene Compositions
**For Each Scene (10 total):**

1. Open Scene 01 composition
2. Import: BG layer (locked)
3. Import: Character layer
4. Import: Object layers (layered by Z-depth)
5. Import: Data visualization layers
6. Import: Text layers
7. Import: Motion effect layers
8. Arrange layer order (see Layer Stack in SETUP.md)
9. Set scale to fit (typically 100%)
10. Repeat for Scenes 2-10

**Time Per Scene:** 15-20 minutes
**Total Time:** 2.5-3 hours

---

## PHASE 4: ANIMATION & TIMING (4-6 hours)

### Step 4.1: Set Master Duration Markers
In Master Composition:
```
Markers:
├─ Scene 1: 0:00
├─ Scene 2: 1:15
├─ Scene 3: 2:45
├─ Scene 4: 4:20
├─ Scene 5: 6:00
├─ Scene 6: 7:30
├─ Scene 7: 9:00
├─ Scene 8: 10:30
├─ Scene 9: 12:00
└─ Scene 10: 13:15
```

### Step 4.2: Animate Each Scene (Scene Template)

**Basic Animation Pattern:**
```
Timeline:
├─ BG Layer: [Locked, entire duration]
├─ Character: [Entrance fade 0-10f, hold, exit fade 10f before end]
├─ Objects: [Staggered entrances 10-30f apart]
├─ Data Viz: [Animated reveals, 0.5-1.0s duration]
├─ Text: [Fade in 10f, hold, fade out 10f]
└─ Motion FX: [Entrance 20f, hold varied, exit 15-20f]
```

**Keyframe Rules:**
- Character entrance: Fade + position (0.5s)
- Object appearance: Offset by 15-30 frames
- Text timing: Sync with voiceover
- Motion effects: Subtle, non-distracting
- Eye blinks: Every 30-40 frames
- Hand gestures: 3-5 frame transitions

**Example: Scene 1 Animation (1:15)**
```
0:00 - 0:10   | Character fades in + positions
0:05 - 0:30   | Background fully visible
0:10 - 0:20   | Eyes blink animation
0:15 - 1:00   | Hand moves to chin (slow 45f transition)
0:20 - 1:10   | Text "SCARCITY" fades in and holds
0:40 - 1:00   | Lightbulb icon appears and pulses
1:10 - 1:15   | Text and character fade out
```

**Time Per Scene:** 30-45 minutes × 10 = 5-7.5 hours
**Efficiency Tip:** Create Scene 1 as template, copy to others, modify per requirements

### Step 4.3: Add Emphasis Effects (30 minutes total)

Optional effects to enhance key moments:
- Glow effect on icons (5% opacity)
- Slight scale pulse on important objects (98%-102%)
- Motion blur on hand gestures (5-10% intensity)
- Fast box blur on background (2-3px, when needed)

**DO NOT:** Add excessive effects - maintain clean, minimalist aesthetic

### Step 4.4: Preview & Timing Check (1 hour)

For each scene:
1. RAM Preview at quarter resolution
2. Verify timing matches script
3. Check for jerky or unnatural movements
4. Adjust keyframes as needed
5. Test full 14:00 playback

---

## PHASE 5: AUDIO INTEGRATION (1.5-2 hours)

### Step 5.1: Import Voiceover
1. File → Import → Audio
2. Select: `voiceover_scarcity_trap_14_00.wav` (provided)
3. Drag to Master comp
4. Lock audio layer (prevent accidental movement)

**Sync Points:**
- 0:00: Voiceover begins
- 14:00: Voiceover ends
- Use audio waveform visual guide to sync text/animation

### Step 5.2: Import Background Music
1. File → Import → Audio
2. Select: Background music track
3. Drag to Master comp below voiceover
4. Set volume: -12dB (let voiceover dominate)
5. Add fade in (0-5sec) and fade out (13:55-14:00)

### Step 5.3: Add Sound Effects (Optional)
- Scene transitions: Subtle whoosh (0.2s)
- Data viz reveals: Gentle tick sound (optional)
- Character stress: Heartbeat (Scene 3, optional)
- Positive ending: Uplifting chord (Scene 10, optional)

### Step 5.4: Mix Audio Levels
```
Audio Levels (Master):
├─ Voiceover: 0dB (reference)
├─ Music: -12dB to -18dB
└─ Effects: -6dB to -12dB
```

Use After Effects audio mixer:
- Window → Audio Mixer
- Adjust levels per track
- Export test mix at -0.5dB peak

---

## PHASE 6: COLOR GRADING & EFFECTS (1-1.5 hours)

### Step 6.1: Apply Global Color Correction

For each scene or master composition:

1. Add Adjustment Layer above all content
2. Apply Effects (in order):
   - Levels (increase contrast)
   - Curves (warm up shadows)
   - Color Balance (add warmth)
   - Saturation (optional, +5-10%)

**Recommended Levels:**
```
Shadows: 15
Midtones: 1.0
Highlights: 245
```

### Step 6.2: Optional LUT Application

If using professional color grading:
1. Effect → Utility → 3D LUT
2. Load provided LUT file (if available)
3. Set blend mode: Linear Dodge (optional)

### Step 6.3: Scene-Specific Tweaks

- **Scene 1-3:** Slightly warm (color temp +500K)
- **Scene 4-6:** Neutral warm
- **Scene 7-9:** Slightly cool (introduce sage green tint)
- **Scene 10:** Warm + bright (hopeful feeling)

### Step 6.4: Verify Color Consistency
- Full 14:00 playback
- Check no jarring transitions
- Verify colors match character design (ochre, burnt sienna, sage green)

---

## PHASE 7: RENDERING & EXPORT (1.5-2 hours)

### Step 7.1: Pre-Render Check
1. Preview Settings:
   - Resolution: Quarter (for speed)
   - Frame Rate: 23.976 fps
2. RAM Preview entire 14:00
3. Address any lagging or playback issues
4. Make final timing adjustments

### Step 7.2: Export Master File (ProRes HQ)

1. Composition → Add to Render Queue
2. Render Settings:
   - Best (full resolution)
   - Format: ProRes 422 HQ
3. Output Module:
   - File Type: QuickTime
   - Video Codec: ProRes 422 HQ
   - Color Depth: 8-bit
   - Frame Rate: 23.976 fps
4. Output File: `Scarcity_Trap_MASTER_ProRes.mov`
5. Start Render

**Render Time:** 45-90 minutes (depends on hardware)

### Step 7.3: Create YouTube Delivery File

1. Composition → Add to Render Queue (same as master)
2. Output Module:
   - File Type: MPEG-4
   - Video Codec: H.264
   - Bitrate: 10 Mbps
   - Frame Rate: 23.976 fps
   - Audio: AAC 128kbps stereo
3. Output File: `Scarcity_Trap_YouTube.mp4`
4. Start Render

**Render Time:** 20-30 minutes

### Step 7.4: Quality Check
```
ProRes Master:
├─ Check file integrity: ffprobe Scarcity_Trap_MASTER_ProRes.mov
├─ Verify duration: 14:00.000
├─ Inspect color profile: Linear/correct
├─ Audio sync: Voiceover perfectly synced

YouTube MP4:
├─ Duration: 14:00
├─ Resolution: 1920x1080
├─ Bitrate: ~10 Mbps
├─ Audio: Stereo 128kbps
└─ No compression artifacts
```

---

## PHASE 8: YOUTUBE UPLOAD & DELIVERY (30 minutes)

### Step 8.1: Prepare YouTube Metadata

**Video Title:**
```
Psychology of Decision Making: The Scarcity Trap
```

**Description:**
```
When resources feel limited, our decision-making ability 
shrinks. In this animated explainer, we explore how scarcity 
affects cognition, leading to poor choices and negative 
consequences.

Watch "The Decision Fatigue Trap" next:
[Link to related video]

---

Key Topics:
• Scarcity Mindset
• Cognitive Bandwidth
• Decision Fatigue
• Behavioral Economics

Research by: Mullainathan & Shafir
Animation: [Your Name]

Resources:
---

Chapters:
0:00 - Introduction
1:15 - Limited Resources
2:45 - Decision Bandwidth
4:20 - The Trap
6:00 - Cognitive Capacity
7:30 - Quality of Life
9:00 - Scarcity Mindset
10:30 - Poor Decisions
12:00 - Consequences
13:15 - Path Forward
```

**Tags:**
```
decision making, scarcity, cognitive bias, behavioral economics, 
psychology, animation, educational, explainer video, mental health
```

**Thumbnail:** Create custom 1280x720 PNG

### Step 8.2: Upload to YouTube

1. YouTube Studio → Create → Upload Video
2. Select file: `Scarcity_Trap_YouTube.mp4`
3. Fill in metadata (title, description, tags)
4. Set thumbnail
5. Check: "Not Made for Kids" (educational content)
6. Visibility: Unlisted (review) → Public (publish)
7. Add to playlist: "Behavioral Economics Series"
8. Publish

### Step 8.3: Post-Upload Quality Check

1. Wait 10 minutes for processing
2. View in full 1080p quality
3. Verify color grading
4. Confirm audio sync
5. Check chapter markers appear correctly
6. Share on social media

---

## PHASE 9: OPTIMIZATION & ARCHIVAL (1 hour)

### Step 9.1: Create Backup Archive
```bash
tar -czf Scarcity_Trap_PRODUCTION.tar.gz \
  Scarcity_Trap_Master.aep \
  Scarcity_Trap_MASTER_ProRes.mov \
  Scarcity_Trap_YouTube.mp4 \
  assets/ \
  scenes/ \
  audio/
```

### Step 9.2: Document Process
- Create production notes: `PRODUCTION_NOTES.md`
- Record total time spent per phase
- Note any challenges or workarounds
- Document settings used for future projects

### Step 9.3: Organize Assets
```
Archive Structure:
├─ FINAL_DELIVERABLES/
│  ├─ Scarcity_Trap_MASTER_ProRes.mov (master)
│  ├─ Scarcity_Trap_YouTube.mp4 (delivery)
│  └─ Thumbnail_1280x720.png
├─ SOURCE_FILES/
│  ├─ Scarcity_Trap_Master.aep
│  ├─ 75_Generated_Images/
│  └─ Audio_Tracks/
└─ DOCUMENTATION/
   ├─ PRODUCTION_NOTES.md
   ├─ ASSET_MAPPING.md
   └─ WORKFLOW_CHECKLIST.md
```

---

## COMPLETE TIMELINE

```
Phase 1: Image Organization ............ 0.5 - 0.75 hours
Phase 2: AE Project Setup .............. 1.0 - 2.0 hours
Phase 3: Image Import & Assembly ....... 2.0 - 3.0 hours
Phase 4: Animation & Timing ............ 4.0 - 6.0 hours
Phase 5: Audio Integration ............. 1.5 - 2.0 hours
Phase 6: Color Grading ................. 1.0 - 1.5 hours
Phase 7: Rendering & Export ............ 1.5 - 2.0 hours
Phase 8: YouTube Upload ................ 0.5 hours
Phase 9: Optimization & Archival ....... 1.0 hours
                                        ───────────────
TOTAL PRODUCTION TIME .................. 13 - 20 hours
```

**Fast-Track Option:** Skip detailed animation per scene (use simpler timing) = 8-12 hours total

---

## CRITICAL SUCCESS FACTORS

✓ All 75 images organized before AE work
✓ Compositions created with correct timings (±0 frames)
✓ Audio imported and locked (prevent sync drift)
✓ Consistent animation patterns per scene
✓ Color grading applied uniformly
✓ Final export tested at full quality before upload

---

## TROUBLESHOOTING REFERENCE

| Problem | Solution | Time |
|---------|----------|------|
| Missing images in AE | Verify import location, re-link in Project Settings | 5-10 min |
| Audio out of sync | Manually adjust audio layer in time, re-preview | 5 min |
| Slow playback | Reduce preview resolution, close unused panels | 2 min |
| Rendering fails | Check for missing footage, resolve all warnings | 10-15 min |
| Colors look wrong | Verify color depth (8-bit), apply levels correction | 5 min |
| Text appears blurry | Use sharp rasterization, verify font is installed | 5 min |

---

**Status:** ✓ Ready for Production
**Last Updated:** 2026-09-11
**Next Action:** Begin Phase 1 (Image Organization)
