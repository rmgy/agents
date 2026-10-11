# Meaning Channel Hybrid Hero Video Production SOP

**Version 2.0 — Hybrid I2V + FFmpeg Pipeline**  
**Niche:** Educational/Psychological YouTube Shorts (9:16 vertical, 115 seconds, 4-act narrative)  
**Last updated:** 2026-10-11

---

## OVERVIEW

This SOP standardizes production of Meaning Channel episodes using a **hybrid AI video pipeline**: 4 image-to-video (I2V) hero clips (10 s each) + 15 FFmpeg limited-motion still clips (3–8 s each) = 115 seconds of finished video.

**Core principle: Audio locks time.** Script → VO → measure → finalize asset list.

**Key metrics:**
- 115 s per episode
- 4 heroes (I2V) = 40 s true animation (34.8%)
- 15 stills (FFmpeg) = 75 s limited motion (65.2%)
- 14 unique images (with reuse tricks)
- 4 narrative acts
- Cost: ~$88–120 production (images + I2V) + VO + music

---

## PART 1: PRE-PRODUCTION

### 1.1 Story Brief & Script Draft

**Input:** Episode concept, title, thematic anchor.

**Deliverable:** 
- 1-paragraph story summary
- 4-act beat breakdown
- Draft script (~350–400 words @ 130 WPM)

**Process:**

Use this Claude prompt:

```
[MEANING_CHANNEL_STORY_BRIEF]

Episode Title: [TITLE]
Thematic anchor (psychology / neuroscience / symbolism / history): [ANCHOR]
Target viewer: 18–40, education-seeking, spiritually curious
Short summary of the concept: [SUMMARY]

Task: Generate a 4-act narrative outline + draft script for a 115-second Meaning Channel episode.

Output format:
# [TITLE]

## Story Structure
- **Act 1 (Experience, 0–30 s):** [beat summary, emotional arc]
- **Act 2 (Science/Story, 30–60 s):** [neuroscience, history, or logic]
- **Act 3 (Symbolism, 60–90 s):** [cultural, spiritual, or pattern meaning]
- **Act 4 (Reflection, 90–115 s):** [personal integration, takeaway]

## Draft Script (21 blocks, ~130 WPM, 1:55 total)
[VO_BLOCK_1] Act 1 — opening, hook, establish emotion
[VO_BLOCK_2] ...
[VO_BLOCK_21] Act 4 — closing, reflection, call to action

## Visual Beats (preliminary)
- Act 1: [highest-motion beat / hook visual]
- Act 2: [science revelation visual]
- Act 3: [symbolic climax visual]
- Act 4: [payoff / integration visual]
```

---

### 1.2 VO Talent & Recording Setup

**Decision:** Record live VO (more authentic) or use high-quality TTS (faster, consistent).

**Live VO:**
- Voice actor specs: warm, contemplative, 125–135 WPM, clear diction.
- Recording: studio or treated room, USB mic, 48 kHz / 16-bit WAV.
- Direction: intimate, like a friend sharing a revelation. Pace is measured. Pauses before revelations (0.4–0.6 s).

**TTS Option:**
- Service: Google Cloud TTS (Wavenet voices) or ElevenLabs (natural timbre).
- Voice selection: Amber or Liam (contemplative, adult).
- Settings: pitch −5%, speed 0.95× (slow it to ~130 WPM).

**Output:** VO script with block markers and estimated durations.

---

### 1.3 Beat-to-Shot Mapping & VO Lock

**Input:** Draft script (21 VO blocks), recorded or TTS audio.

**Process:**

1. **Measure VO duration per block:**
   ```bash
   ffprobe -select_streams a:0 -show_entries frame=pkt_duration_time \
     -of csv=p=0 vo_block_01.wav | awk '{sum+=$1} END {print sum}'
   ```

2. **Run the smart hero count formula:**
   ```
   TOTAL = 115 s (measured or set)
   FULL_SEGMENTS = FLOOR(115 / 30) = 3
   REMAINING = 115 - (3 * 30) = 25 s
   
   If REMAINING >= 15 s OR (10 s <= REMAINING < 15 s AND contains payoff):
     HEROES = FULL_SEGMENTS + 1 = 4
   Otherwise:
     HEROES = FULL_SEGMENTS = 3
   
   STILLS = CEILING((TOTAL - HEROES * 10) / 5)
   IMAGES_BASE = HEROES + STILLS
   IMAGES_REUSE = IMAGES_BASE - (keyframe_bookends + harvested_frames)
   ```
   
   For 115 s: **4 heroes, 15 stills, 14 images (with reuse).**

3. **Assign hero beats** (using the scoring rubric, below).

4. **Retime shots to VO:**
   ```python
   # For each VO block, calculate final shot duration
   def retime_block(vo_duration_sec, block_type="still", hero_max_vo=6.5):
       if block_type == "hero":
           if vo_duration_sec > hero_max_vo:
               return ("WARN", f"Hero VO {vo_duration_sec}s > {hero_max_vo}s, trim script")
           return ("HERO", 10)  # Fixed hero duration
       else:  # still
           shot_dur = vo_duration_sec + 0.35  # Padding
           if shot_dur < 3:
               return ("MERGE", f"< 3s, merge with adjacent block")
           elif shot_dur > 8:
               return ("SPLIT", f"Split into 2 stills, +1 image")
           else:
               return ("STILL", round(shot_dur, 2))
   ```

5. **Finalize timeline:**
   - Total duration must sum exactly to 115 s.
   - No shot < 3 s.
   - Stills ≤ 8 s.
   - Hero VO ≤ 6.5 s.

**Deliverable:** `timeline.json` (see schema, §10).

---

## PART 2: ASSET PLANNING

### 2.1 Hero Beat Selection

**Goal:** Place 4 heroes to maximize story impact while respecting spacing rules.

**Scoring rubric** (beat type, motion necessity, narrative role):

```
BEAT_WEIGHTS = {
    "hook": 5,              # Opening, must engage
    "revelation": 5,        # New science or insight
    "climax": 5,            # Emotional / narrative peak
    "transformation": 4,    # Visible change in subject
    "payoff": 4,            # CTA or resolution
    "action": 4,            # Motion, no still can sell it
    "chapter_open": 3,      # Act boundary
    "emotional_peak": 3,    # Deeper feeling moment
    "setup": 1,             # Context, exposition
    "explain": 0,           # Data, diagram (stills only)
    "transition": 0,        # Connection between acts
}

def score_beat(beat_dict):
    # beat_dict: {time_sec, beat_type, motion_necessary_0_2, 
    #             thumbnail_promise_0_1, retention_risk_0_2, i2v_risk_0_2}
    return (3 * BEAT_WEIGHTS.get(beat_dict["beat_type"], 0)
            + 2 * beat_dict.get("motion_necessary", 0)
            + 2 * beat_dict.get("thumbnail_promise", 0)
            + beat_dict.get("retention_risk", 0)
            - 2 * beat_dict.get("i2v_risk", 0))
```

**Spacing rules:**
- Minimum gap: 15 s (heroes too close cancel each other).
- Maximum gap: 45 s (first 2 min), 60 s (after).
- Hook hero: mandatory at 0–10 s.
- Payoff hero: mandatory in last 30 s if REMAINING >= 15 s.

**Algorithm** (pseudocode):

```
beats = [all story beats from timeline, scored]
heroes_to_place = 4

# Greedy placement with gap enforcement
selected_heroes = [beats[0]] if beats[0]["time"] < 10 and beats[0]["beat_type"] == "hook"
for b in sorted(beats, key=score_beat, reverse=True):
    if len(selected_heroes) >= heroes_to_place:
        break
    if b not in selected_heroes:
        gap_check = all(abs(b["time"] - h["time"]) >= 15 for h in selected_heroes)
        if gap_check:
            selected_heroes.append(b)

# Repair: fill any gap > max_gap by swapping lower-scored heroes
def repair_gaps(selected, max_gap=45):
    for i in range(len(selected) - 1):
        if selected[i+1]["time"] - selected[i]["time"] > max_gap:
            candidates = [b for b in beats 
                         if selected[i]["time"] < b["time"] < selected[i+1]["time"]
                         and all(abs(b["time"] - h["time"]) >= 15 for h in selected)]
            if candidates:
                swap_out = min((h for h in selected[:-1] if h["beat_type"] != "hook"), 
                              key=score_beat)
                selected.remove(swap_out)
                selected.append(max(candidates, key=score_beat))
    return sorted(selected, key=lambda b: b["time"])
```

**Meaning Channel template (locked):**
- **H1 @ 0–10 s:** Experience act, disorientation / sensory hook.
- **H2 @ 30–40 s:** Science act, revelation / mechanism visible.
- **H3 @ 60–70 s:** Symbolism act, climax / pattern emergence.
- **H4 @ 90–100 s:** Reflection act, payoff / integration.

**Deliverable:** Hero placement map (times, beat descriptions, why each is a motion peak).

---

### 2.2 Image & I2V Prompt Generation

**Input:** Timeline with 4 heroes + 15 stills, VO scripts, color palette (4 hex codes).

**Process:**

#### A. Hero I2V Prompts

Use this Claude prompt template:

```
[HERO_I2V_PROMPT_GENERATOR]

Episode: [TITLE]
Color Palette: Primary: [HEX1], Accent: [HEX2], Highlight: [HEX3], Shadow: [HEX4]
Narrative: [ACT_NAME] — [beat description]
VO line: "[VO_TEXT]" (duration: [VO_DUR]s)

Task: Generate a concise image-to-video prompt for a 10-second I2V clip.

Requirements:
- Subject: [specific entity or scene]
- Action: [single, clear motion or transformation]
- Camera move: [pull back / zoom / rotate / pan, if any]
- Lighting: describe using the color palette hex codes
- Style: storybook illustration, soft focus, cinematic
- Duration: 10 s, trim head to 0.5–2 s so frame 1 is mid-action
- Peak motion: should land at [PEAK_TIME]s (where "[REVEAL_WORD]" is spoken)

Output:
## H[#]: [BEAT_NAME]
**Image:** [subject, scene, composition, 1–2 sentences]
**Action:** [motion, transformation, 1–2 sentences]
**Camera:** [move, direction, 1 sentence]
**Lighting:** [color references using the palette, 1 sentence]
**Duration:** 10 s; trim head [X]s so peak lands @ [PEAK_TIME]s
**Motion style:** [ethereal / dynamic / hypnotic / meditative]
**Prompt for I2V (Runway / Adobe):**
"[Runnable I2V prompt string: subject, action, camera, lighting, palette, duration, style]"
```

**Example output:**

```
## H1: Overlapping Realities
**Image:** A café interior shown twice, perfectly aligned. The present moment in 
sharp detail (#e8e8e8 silverware, #0a0e27 walls), a ghostly translucent copy behind 
it in (#4a1a6f) plum tint. A figure's face in foreground, eyes widening.

**Action:** The two spaces subtly shift apart, creating disorientation. Then realign. 
The motion is slow, dreamlike, uncanny.

**Camera:** Slow 3-frame-per-second pullback, 10 s total. Creates sensation of distance 
while maintaining the overlap.

**Lighting:** Even deep midnight (#0a0e27) base. Present moment: silver (#e8e8e8) 
highlights on objects, rim light on face. Ghost moment: plum (#4a1a6f) color cast, 
lower saturation.

**Duration:** 10 s; trim head 0.5 s (so first motion frame shows shift already starting). 
Peak motion (widest gap between spaces) should land at 4–5 s, where the hook VO 
"*without knowing it*" is spoken.

**Motion style:** Ethereal, otherworldly, disorienting.

**Prompt for I2V:**
"A café interior shown twice, overlapping. One sharp and silver-lit, one ghostly and 
plum-tinted. They subtly shift apart and realign. Camera slowly pulls back. Figure's 
face in foreground, eyes widening. Storybook illustration style, ethereal, slow motion, 
deep midnight and silver color palette. 10 seconds, mid-action on frame 1."
```

**Repeat for H2, H3, H4.**

Deliverable: 4 hero prompts, each with copy-paste I2V string.

---

#### B. Still-Image Prompts

Use this template:

```
[STILL_IMAGE_PROMPT_GENERATOR]

Episode: [TITLE]
Color Palette: [HEX1], [HEX2], [HEX3], [HEX4]
Timeline context: Act [#], beat [name], VO block [S##]
VO text: "[VO_TEXT]" (duration: [VO_DUR]s, shot duration: [SHOT_DUR]s)
Narrative role: [establish / reveal / transition / resolve]

Task: Generate a still-image prompt for a 3–8 second zoompan clip.

Requirements:
- Composition: [framing, rule of thirds, focus point]
- Subject: [what the camera should see, 1–2 nouns]
- Lighting: [key, fill, back, mood; use color palette]
- Style: storybook illustration, soft focus, cinematic
- FFmpeg move: [push_in / pan / punch_in / pull_out / hold] + [direction, intensity]
- Keyword (if applicable): [word that gets a punch or motion emphasis]

Output:
## S[##]: [BEAT_NAME]
**Image:** [subject and composition, 1–2 sentences]
**Lighting:** [key light, fill, mood; reference palette, 1 sentence]
**Style:** storybook illustration, [specific mood]
**Duration:** [SHOT_DUR]s
**FFmpeg move:** [movement], intensity [0–1], direction [left/right/up/down]
**Keyword sync:** [if punch, the word and its timestamp in the VO block]
**Prompt for image gen (Midjourney / Flux):**
"[Subject], [composition], [lighting], [color palette reference], [style], storybook."
```

**Example:**

```
## S01: Entering Café
**Image:** A person pushing through a café door. Warm interior light spills through. 
Disorientation visible in their body language. Tables, silverware, ambient warmth.

**Lighting:** Warm golden backlight from door, soft fill on figure. Deep midnight 
shadows in café interior. Silver accents on glass and metal. Mood: familiar yet eerie.

**Style:** Storybook illustration, soft focus, intimate.

**Duration:** 5 s

**FFmpeg move:** push_in, intensity 0.08, direction toward figure's face. Ramp over 0.5 s, 
hold for 4.5 s. Creates anticipation for H1.

**Keyword sync:** None (ambient establishing shot).

**Prompt for image gen:**
"Person entering a café, warm golden backlight, cozy interior, disorientation in 
expression, storybook illustration, deep midnight and silver color palette, soft 
focus, intimate mood."
```

**Repeat for S02–S15.**

Deliverable: 15 still prompts + camera move specs.

---

### 2.3 Reuse Map

**Locked reuse tricks** (save 2–3 images without harming continuity):

1. **Keyframe bookend:** The still *before* a hero is the hero's starting keyframe (shot slow push_in). The hero animates out of it. Saves 1 image per hero, but limits this to 1–2 per episode (usually H1 and H2).

2. **Last-frame harvest:** Extract the hero's final frame as the following still's keyframe. Upscale if soft. Free image, perfect continuity cut.

**Template:**

```json
{
  "reuse_tricks": {
    "keyframe_bookends": [
      {
        "hero": "H1",
        "hero_beat": "Overlapping Realities",
        "still_before": "S02",
        "still_beat": "Eyes Widening",
        "benefit": "S02 slow push_in builds anticipation; H1 animates out of same keyframe"
      }
    ],
    "harvested_frames": [
      {
        "hero": "H1",
        "harvest_source": "H1.mp4 last frame (~10 s mark)",
        "still_after": "S04",
        "still_beat": "Settling Confusion",
        "process": "ffmpeg -sseof -0.1 -i H1.mp4 -frames:v 1 -update 1 s04_keyframe.png; upscale if soft"
      },
      {
        "hero": "H2",
        "harvest_source": "H2.mp4 final frame",
        "still_after": "S08"
      },
      {
        "hero": "H3",
        "harvest_source": "H3.mp4 final frame",
        "still_after": "S12"
      }
    ]
  },
  "images_to_generate": 14,
  "breakdown": "4 heroes + 15 stills - 1 keyframe_bookend (S02) - 3 harvests = 14"
}
```

**Deliverable:** Reuse map with ffmpeg harvest commands.

---

## PART 3: ASSET GENERATION

### 3.1 Batch Image Generation

**Tool:** Midjourney (fast mode) or Flux.

**Process:**

1. **Prepare batch file** (`images.txt`):
   ```
   # H1 Keyframe (overlapping realities)
   A café interior shown twice, overlapping...
   
   # S01 (entering café)
   Person entering a café, warm golden backlight...
   
   # S03 (memory fragments)
   Surreal floating memory snippets...
   
   [... 14 prompts total]
   ```

2. **Submit to Midjourney:**
   - Use `/imagine` for each prompt OR upload batch.
   - Aspect ratio: `--ar 9:16` (ensure vertical orientation).
   - Quality: `--q 2` (fast, cost-effective for storyboard style).
   - Style: Add to each prompt: `storybook illustration, soft focus, [color palette]`.

3. **Monitor & upscale:**
   - Download each generation.
   - Upscale to 1080×1920 px (9:16 vertical).
   - Check color accuracy: blacks = #0a0e27, highlights = #e8e8e8.

4. **Quality check:**
   - Are all images consistent in style (storybook)?
   - Do colors match the palette?
   - Are compositions clear and cinematic?

**Cost:** 14 images @ $2–3 each = $28–42 (Midjourney fast).

**Deliverable:** 14 high-res still PNG files (1080×1920 px, 72 DPI).

---

### 3.2 I2V Generation

**Tool:** Runway Gen-3 or Adobe Firefly (Motion).

**Process:**

1. **Prepare I2V batch:**
   - 4 hero keyframes (from image batch, or generated separately).
   - 4 I2V prompts (from §2.2A).
   - Motion parameters: duration 10 s, resolution 1080×1920, 30 FPS.

2. **Submit jobs:**
   ```bash
   # Example: Runway API (if available)
   runway_api_call(
     keyframe="H1_keyframe.png",
     prompt="A café interior shown twice, overlapping...",
     duration=10,
     fps=30,
     resolution="1080x1920"
   )
   ```

3. **Monitor generation:**
   - I2V typically takes 10–15 min per clip.
   - If parallel API: all 4 @ once = ~15 min total.
   - If sequential: ~60 min total.

4. **QA checks:**
   - Frame 1 is mid-action (not ramping in slowly). If ramp is slow (0.5–2 s), trim.
   - Peak motion lands at expected second (e.g., H1 peak @ 4–5 s).
   - No jitter or artifacts.
   - Color accuracy: palette preserved.
   - Resolution: steady 1080×1920, 30 FPS.

5. **Prepare for assembly:**
   - Convert to H.264 MP4 if needed.
   - Trim head if ramp-in is slow: `ffmpeg -i H1.mp4 -ss 0.5 -c copy H1_trimmed.mp4`.
   - Confirm duration: `ffprobe -v error -show_entries format=duration -of csv=p=0 H1.mp4`.

**Cost:** 4 I2V clips @ $15 each = $60 (Runway standard).

**Deliverable:** H1.mp4, H2.mp4, H3.mp4, H4.mp4 (10 s each, 1080×1920, 30 FPS, trimmed heads).

---

### 3.3 FFmpeg Still Rendering (Zoompan)

**Tool:** FFmpeg with `zoompan` filter (free, CPU-rendered).

**Process:**

For each still (S01–S15), render the specified camera move:

```bash
# S01: push_in, intensity 0.08, 5 seconds
ffmpeg -i s01.png \
  -vf "scale=1080:1920,zoompan=z='min(zoom+0.0008,1.08)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:fps=30" \
  -frames:v 150 s01_pushIn.mp4

# S02: pan left, 5 seconds
ffmpeg -i s02.png \
  -vf "scale=1080:1920,zoompan=z='1':x='(iw/30)*t':y='(ih-ih/zoom)/2':d=1:fps=30" \
  -frames:v 150 s02_panLeft.mp4

# S03: punch_in (jump), intensity 0.2, 5 seconds
ffmpeg -i s03.png \
  -vf "scale=1080:1920,zoompan=z='if(t<1,1,1.2)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:fps=30" \
  -frames:v 150 s03_punchIn.mp4

# S15: dissolve, 5 seconds (fade to white)
ffmpeg -i s15.png \
  -vf "scale=1080:1920,fade=out:st=4:d=1" \
  -frames:v 150 s15_dissolve.mp4
```

**Movement presets** (copy-paste):

```
# Push_in, intensity 0.06 (gentle)
zoompan=z='min(zoom+0.0006,1.06)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:fps=30

# Push_in, intensity 0.10 (strong)
zoompan=z='min(zoom+0.001,1.10)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:fps=30

# Pan left
zoompan=z='1':x='(iw/30)*t':y='(ih-ih/zoom)/2':d=1:fps=30

# Pan right
zoompan=z='1':x='(iw/30)*(5-t)':y='(ih-ih/zoom)/2':d=1:fps=30

# Punch_in (instant jump), intensity 1.2
zoompan=z='if(t<0.5,1,1.2)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:fps=30

# Pull_out, intensity 0.05 (very gentle)
zoompan=z='max(zoom-0.0005,0.95)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:fps=30

# Hold (no motion, slight pulse)
scale=1080:1920
```

**Batch script** (`render_stills.sh`):

```bash
#!/bin/bash
declare -A MOVES=(
  [s01]="push_in,0.08"
  [s02]="pan,left"
  [s03]="punch_in,1.2"
  [s04]="pull_out,0.05"
  [s05]="push_in,0.06"
  # ... etc for s06–s15
)

for still in "${!MOVES[@]}"; do
  IFS=',' read -r move intensity <<< "${MOVES[$still]}"
  echo "Rendering $still with $move..."
  # [ffmpeg command for this still]
done
```

**Cost:** Free (CPU rendering, ~1 min per clip on modern hardware).

**Deliverable:** S01.mp4–S15.mp4 (each 3–8 s, 1080×1920, 30 FPS, camera move applied).

---

## PART 4: AUDIO DESIGN

### 4.1 VO Finalization

**Input:** VO blocks (recorded or TTS), measured durations.

**Process:**

1. **Normalize audio:**
   ```bash
   ffmpeg-normalize vo_blocks/*.wav -o vo_normalized/ -l -20 LUFS
   ```

2. **Apply gentle EQ** (warmth + clarity):
   - Boost 200–400 Hz (warmth, presence).
   - Slight dip at 2–3 kHz (reduce harshness).
   - Boost 8–12 kHz (clarity, presence).

3. **Gate & compress:**
   - Gate threshold: −35 dB (remove room noise).
   - Compressor ratio: 2:1, knee: soft, make-up gain: +2 dB.

4. **Export per block:**
   ```bash
   ffmpeg -i vo_block_01.wav -af "highpass=100,lowpass=12000,compand=0.5|0.5,10|10,-inf,-35/-35,-35,-35,0,-inf" \
     vo_01_processed.wav
   ```

**Deliverable:** 21 processed VO files, normalized to −20 LUFS.

---

### 4.2 Soundscape & Music Bed

**Approach:** Contemplative, supportive, never competes with VO.

**Elements:**

1. **Ambient pad** (60–90 min duration):
   - Tone: Ethereal, subtle, matches episode mood (e.g., neural hum for Science acts, cosmic drone for Symbolism acts).
   - Instrumentation: Pad synth, bowed strings, warm reverb.
   - Loudness: −18 LUFS when solo, ducks to −24 LUFS under VO.

2. **SFX library:**
   - Soft impacts on punch_in keywords (e.g., "recognition" → subtle 1 kHz click).
   - Transition tones between acts (soft whoosh or bell).
   - Hero breathing gap SFX: music swell + soft underscore.

3. **Music structure:**
   - Acts 1–2: Minimal, sparse, contemplative.
   - Act 3 (climax): Gradual build, emotional arc.
   - Act 4: Resolution, settling into clarity.

**Tools:**
- Ambient: Splice (download royalty-free), or compose in Logic Pro / Ableton.
- SFX: Freesound.org (CC-licensed), or generate via AI (Adobe SoundDraw).
- Mixing: Reaper, Audacity, or Adobe Audition.

**Deliverable:** 
- `audio_bed.wav` (115 s, −18 LUFS)
- SFX library (`sfx_punches.wav`, `sfx_transitions.wav`, `sfx_hero_breaths.wav`)

---

## PART 5: ASSEMBLY & POST-PRODUCTION

### 5.1 Timeline Assembly

**Tool:** Adobe Premiere Pro, DaVinci Resolve, or Final Cut Pro.

**Process:**

1. **Create new sequence:**
   - Format: 1080×1920 px, 9:16 vertical.
   - Frame rate: 30 FPS.
   - Audio: Stereo, 48 kHz.

2. **Import & arrange on timeline:**
   - Sequence order: H1 → S01 → S02 → S03 → S04 → H2 → S05 → ... → S15.
   - Confirm durations match timeline.json exactly.

3. **Sync VO to timeline:**
   - Lay each VO block on audio track, aligned to its shot's start time.
   - Apply J-cut where appropriate (VO leads picture by 0.2–0.3 s for transitions).
   - Check sync: keyword punches should land ±0.1 s of marked timestamp.

4. **Arrange music bed & SFX:**
   - Layer 1: VO (lead).
   - Layer 2: Music bed (support, ducked).
   - Layer 3: SFX (impacts on punches, transitions).

5. **Color grade:**
   - Apply LUT or manual grade to unify palette across all stills + heroes.
   - Ensure blacks are true #0a0e27 (RGB 10, 14, 39).
   - Highlights clip to #e8e8e8 (RGB 232, 232, 232).
   - Plum (#4a1a6f) and slate (#5a6e8f) accents visible but not overblown.

6. **Overlays (optional):**
   - On-screen text for key concepts (e.g., "Pattern Recognition", "Eternal Return").
   - Fade in @ first VO mention, fade out @ 2–3 s later.
   - Font: sans-serif, light weight, high contrast (white on dark background).
   - Placement: lower third or center, clear of important visuals.

**Deliverable:** Assembled timeline (sequence file + linked media).

---

### 5.2 Audio Mixing & Ducking

**Process:**

1. **Ducking:** Music ducks when VO is present.
   ```
   # Scenario: Music at −18 LUFS, VO at −20 LUFS
   # Under VO: music → −26 LUFS (−8 dB reduction)
   # Hero breathing gap (0.5–1 s silence): music swells to −14 LUFS
   ```

2. **SFX layering:**
   - Punch-in keyword: SFX click at −30 LUFS (subtle), attack @ keyword start.
   - Transition: soft whoosh at −28 LUFS, 0.5 s before cut.
   - Hero breathing: underscore pad at −20 LUFS, swells ±2 dB on hero peak.

3. **Master chain:**
   - EQ: gentle presence boost at 3–4 kHz (clarity).
   - Compression: 2:1 ratio, soft knee, thresh −20 LUFS (catch peaks).
   - Limiter: −0.1 dB (prevent digital clipping).
   - Final loudness: −16 LUFS (YouTube Shorts standard).

4. **Export master audio:**
   ```bash
   ffmpeg -i timeline_with_all_audio.mp4 \
     -af "compand=0|0,0.5|0.5,10|10,-inf,-35/-35,-35,-35,0,-inf, \
           eq=f=1000:t=l:w=0.3:g=3, \
           eq=f=3000:t=p:w=0.5:g=2, \
           compressor=threshold=-20:ratio=2:knee=0.3, \
           alimiter=limit=0.0" \
     -c:a pcm_s24le \
     master_audio.wav
   ```

**Deliverable:** Master audio file (−16 LUFS, stereo, 48 kHz).

---

### 5.3 QA & Export

**Checklist:**

- [ ] **Duration:** Measure with ffprobe. Must equal 115 s exactly.
  ```bash
  ffprobe -v error -show_entries format=duration -of csv=p=0 master.mp4
  ```

- [ ] **All shots present:** Count cuts. Should match timeline (4 heroes + 15 stills = 19 cuts).

- [ ] **Shot duration accuracy:** Spot-check 5 shots; confirm they match timeline.json ±0.05 s.

- [ ] **VO sync:** Play back with subtitles. Keyword punches land within ±0.1 s of marked times.

- [ ] **Color accuracy:** 
  - Blacks in image histogram @ RGB (10–20, 10–20, 35–45).
  - Highlights @ RGB (230–240, 230–240, 240–245).
  - Plum accent visible but not blown out.

- [ ] **Audio loudness:** ffmpeg-analyze shows −16 LUFS (±0.5 dB).

- [ ] **Frame rate:** Constant 30 FPS (no dropped frames). Measure:
  ```bash
  ffprobe -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 master.mp4
  ```

- [ ] **No artifacts:** Watch full video. No jitter, no color banding, no audio dropouts.

**Export variants:**

1. **YouTube Shorts master** (H.264, 40 Mbps, AAC 128 kbps):
   ```bash
   ffmpeg -i timeline.mp4 -c:v libx264 -preset slow -b:v 40M \
     -c:a aac -b:a 128k -y "episode_title_YOUTUBE.mp4"
   ```

2. **Archive master** (ProRes 422 HQ, uncompressed for future re-cuts):
   ```bash
   ffmpeg -i timeline.mp4 -c:v prores_ks -q:v 0 -c:a pcm_s24le \
     -y "episode_title_ARCHIVE.mov"
   ```

3. **Social repost clip** (15 s, split-hero variant: H1 + H4):
   - Trim: 0–4 s (H1 hook) + 90–105 s (H4 payoff) + crossfade @ 2 s.
   - Use as YouTube Shorts excerpt or Instagram Reels.

**Deliverable:** Master MP4 + Archive ProRes + repost 15 s clip.

---

## PART 6: DELIVERY & DOCUMENTATION

### 6.1 Production Package

**Files to deliver:**

```
meaning-channel-[EPISODE_SLUG]/
├── 01_script/
│   ├── script_final.md          # Final VO script with timecodes
│   ├── timeline.json            # Locked timeline (shot durations, VO blocks, FFmpeg moves)
│   └── beat_analysis.json       # Beat scoring, hero placement logic
├── 02_assets/
│   ├── images/                  # 14 final still PNGs (1080×1920)
│   │   ├── s01.png
│   │   ├── s02.png
│   │   └── ...
│   ├── heroes/                  # 4 I2V MP4s (1080×1920, 30 FPS)
│   │   ├── H1.mp4
│   │   └── ...
│   ├── stills_rendered/         # 15 FFmpeg zoompan MP4s (3–8 s, with camera moves)
│   │   ├── s01_pushIn.mp4
│   │   └── ...
│   └── audio/
│       ├── vo_blocks/           # 21 VO files (normalized, −20 LUFS)
│       ├── audio_bed.wav        # Music + ambient
│       └── sfx/                 # SFX library (impacts, transitions, breaths)
├── 03_assembly/
│   ├── timeline_project.mp4     # Assembled timeline (before final export)
│   ├── color_grade_lut.cube     # Color grading LUT (for consistency across episodes)
│   └── master_audio.wav         # Final mixed audio (−16 LUFS)
├── 04_final/
│   ├── episode_title_YOUTUBE.mp4            # H.264, 40 Mbps (YouTube-ready)
│   ├── episode_title_ARCHIVE.mov            # ProRes 422 HQ (archive quality)
│   ├── episode_title_REPOST_15s.mp4         # Social media excerpt
│   └── metadata.json                        # Title, description, tags, thumbnail frame
└── 05_docs/
    ├── PRODUCTION_LOG.md        # Timeline, issues, decisions
    ├── COST_BREAKDOWN.md        # Hero costs, image costs, audio costs, total
    ├── QA_CHECKLIST.md          # All checks passed/failed with notes
    └── NOTES_FOR_NEXT_EPISODE.md # Lessons learned, prompt refinements
```

---

### 6.2 Cost Summary Template

**Fill in after each episode:**

```markdown
# Cost Breakdown: [EPISODE_TITLE]

## Production Assets
| Item | Unit Cost | Qty | Total |
|---|---|---|---|
| I2V generation | $15 | 4 | $60 |
| Still images | $2 | 14 | $28 |
| FFmpeg renders | free | 15 | $0 |
| **Subtotal (images + I2V)** | — | — | **$88** |

## Audio
| Item | Cost | Notes |
|---|---|---|
| VO recording | [varies] | [in-house / outsourced] |
| Ambient music | free | [Splice / composition] |
| SFX library | free | [Freesound / AI generation] |
| Audio mixing | [labor] | 2 h @ [rate] |
| **Subtotal (audio)** | **$[X]** | |

## Post-Production
| Task | Labor (h) | Cost |
|---|---|---|
| Assembly | 1.5 | [rate] |
| Color grade | 0.5 | [rate] |
| QA & export | 0.5 | [rate] |
| **Subtotal (labor)** | **3 h** | **$[Y]** |

## **TOTAL PRODUCTION COST** | | | **$88 + Audio + Labor** |
| Timeline | | | 10–14 h |
| Cost per minute | | | $[X] |
| Reusability | | | Color LUT + templates for 4+ episodes |
```

---

### 6.3 Metadata & Upload

**YouTube Shorts metadata:**

```
Title (60 char max, keyword-rich):
"Why Déjà Vu Feels So Real — Neuroscience & Consciousness Explained"

Description (template):
"Have you ever felt like you've lived a moment before? In this Meaning Channel 
short, we explore déjà vu through three lenses: the neuroscience of memory, the 
symbolism of eternal return, and what it reveals about consciousness itself.

🧠 Learn: How your brain's pattern-matching system creates this eerie sensation
🌀 Reflect: What déjà vu teaches us about the nature of memory and time
∞ Wonder: Is consciousness more mysterious than we thought?

Subscribe for explorations of psychology, neuroscience, history, and meaning.

Chapters:
0:00 Experience — Disorientation
0:30 Science — How Memory Works
1:00 Symbolism — Eternal Return
1:30 Reflection — What It Means

Sources: [neuroscience papers], [philosophical references]"

Tags:
déjà vu, neuroscience, psychology, consciousness, memory, philosophy, education

Thumbnail:
[Frame from H3 climax, high contrast, text overlay: "Why Déjà Vu Feels REAL"]

Category: Education
License: Standard (YouTube)
Comments: Allowed, limited
```

---

## PART 7: SCALING TO SERIES

### 7.1 Batch Workflow (5 Episodes)

**Timeline for 5 episodes (parallel where possible):**

| Phase | Duration | Episodes | Notes |
|---|---|---|---|
| **1. Story + VO** | 2–3 h each | All 5 in parallel | Scripts lock VO |
| **2. Asset planning** | 1–2 h each | All 5 in parallel | Timeline.json + prompts |
| **3. Image generation** | 2 h (batch) | 70 images @ $2 = $140 | Midjourney batch mode |
| **4. I2V generation** | 0.5 h (parallel) | 20 heroes @ $15 = $300 | Runway concurrent jobs |
| **5. FFmpeg renders** | 1 h (batch) | 75 stills (free) | CPU rendering overnight |
| **6. Audio + mixing** | 2 h each | Each episode separately | ~1 h design, 1 h mixing |
| **7. Assembly + QA** | 2 h each | Each episode separately | Parallel editing |
| **TOTAL (for 5)** | **~50 h labor** | | **~$440 assets** |

**Cost per episode (series rate):**
- Assets: $88 (images) + $60 (I2V) = $148.
- Labor: ~10 h @ [your rate] = [X].
- **Total: $148 + labor.**

---

### 7.2 SOP Refinements Between Episodes

**After Episode 1, document:**

1. **Prompt refinements:**
   - Which hero prompts generated first try?
   - Which needed iteration (motion ramp-in, color inaccuracy)?
   - Update prompt templates with successful language.

2. **Timeline patterns:**
   - Did the 4-hero, 15-still formula hold for diverse topics?
   - Were there beat-scoring surprises?
   - Refine beat_weights if needed.

3. **Audio insights:**
   - What WPM worked best for this niche (125–135 WPM effective)?
   - Which SFX placements landed best (punches, transitions, breaths)?
   - Update audio design defaults.

4. **Team capacity:**
   - Which tasks could be automated (script generation, reuse mapping, FFmpeg batch)?
   - Which benefit from human judgment (image selection, hero placement, color grading)?

**Output:** Updated `REFINEMENTS_LOG.md` + revised prompt templates + refined beat_weights.

---

## PART 8: TOOLS & RESOURCES

### Quick Reference

**Prompting (Claude):**
- `[HERO_I2V_PROMPT_GENERATOR]` — Hero video prompt template.
- `[STILL_IMAGE_PROMPT_GENERATOR]` — Still image prompt template.
- `[MEANING_CHANNEL_STORY_BRIEF]` — Story outline + script template.

**Image generation:**
- Midjourney: `/imagine [prompt] --ar 9:16 --q 2`
- Flux (Replicate): API call with custom aspect ratio.

**I2V:**
- Runway Gen-3: Web UI or API, 10 s duration, 1080×1920 px.
- Adobe Firefly (Motion): Web UI, similar specs.

**Audio:**
- TTS: Google Cloud Wavenet, ElevenLabs.
- Music: Splice (CC-licensed).
- SFX: Freesound.org, Adobe Audition built-in library.
- Normalization: `ffmpeg-normalize`.
- Mixing: Reaper, Audacity, Adobe Audition.

**Video assembly:**
- Premiere Pro, DaVinci Resolve, Final Cut Pro, Shotcut.

**FFmpeg reference:**
- Zoompan filter: `ffmpeg -i input.png -vf "zoompan=..." output.mp4`.
- Duration measurement: `ffprobe -v error -show_entries format=duration -of csv=p=0`.
- Loudness analysis: `ffmpeg-normalize input.mp4 -l -16 LUFS`.

---

## PART 9: CHECKLIST (COMPLETE WORKFLOW)

Use this for every episode:

### Pre-Production
- [ ] Story brief finalized (4-act structure confirmed).
- [ ] Script drafted (~350–400 words, tagged blocks).
- [ ] VO recorded/TTS generated, measured, locked to 115 s.
- [ ] Timeline created (`timeline.json`): 4 heroes @ [times], 15 stills @ [durations].
- [ ] Hero beats selected and scored.
- [ ] Reuse map approved (keyframe bookends, harvests).

### Asset Generation
- [ ] 14 still-image prompts finalized and copy-pasted.
- [ ] 4 hero I2V prompts finalized and copy-pasted.
- [ ] 15 still images generated, upscaled to 1080×1920, color-checked.
- [ ] 4 hero I2V clips generated, trimmed heads, peak-aligned.
- [ ] 15 FFmpeg zoompan clips rendered with correct camera moves.

### Audio
- [ ] 21 VO blocks normalized to −20 LUFS, EQ applied.
- [ ] Ambient music bed (~115 s) prepared, −18 LUFS.
- [ ] SFX library ready (punches, transitions, breaths).

### Assembly
- [ ] Timeline assembled: H1 → S01 → S02 → ... → S15.
- [ ] VO synced to shots, J-cuts applied, keyword punches verified.
- [ ] Music ducked, SFX layered, master audio mixed to −16 LUFS.
- [ ] Color graded: blacks #0a0e27, highlights #e8e8e8, palette unified.
- [ ] (Optional) On-screen text overlays placed.

### QA
- [ ] Duration = exactly 115 s.
- [ ] All shots >= 3 s; stills <= 8 s.
- [ ] VO sync within ±0.1 s for keyword punches.
- [ ] Audio loudness = −16 LUFS ±0.5 dB.
- [ ] Color palette verified (blacks, highlights, accents).
- [ ] Frame rate constant 30 FPS.
- [ ] No artifacts, jitter, dropouts.

### Export & Delivery
- [ ] YouTube Shorts H.264 MP4 (40 Mbps, AAC 128 kbps).
- [ ] ProRes archive (uncompressed, for re-cuts).
- [ ] 15 s repost clip (split-hero variant).
- [ ] Metadata file (title, description, tags, thumbnail frame).
- [ ] Production package organized and documented.
- [ ] Cost summary filled in.
- [ ] Lessons learned noted for next episode.

---

## PART 10: EXAMPLE TIMELINES

### "Why Déjà Vu Feels So Real" (Complete)

```json
{
  "episode": "Why Déjà Vu Feels So Real",
  "total_seconds": 115,
  "hero_count": 4,
  "still_count": 15,
  "segments": [
    {
      "segment": 1,
      "time_range": "0:00–0:30",
      "act": "Experience",
      "blocks": [
        {
          "idx": 1,
          "type": "hero",
          "id": "H1",
          "beat": "Overlapping Realities",
          "start": 0,
          "duration": 10,
          "vo_text": "You're in a familiar place for the first time...",
          "vo_duration": 4.2,
          "camera": "pull_back",
          "peak_motion_t": 4.5,
          "reveal_word": "without knowing it"
        },
        {
          "idx": 2,
          "type": "still",
          "id": "S01",
          "beat": "Entering Café",
          "start": 10,
          "duration": 5,
          "vo_text": "Your eyes widen...",
          "camera": "push_in 0.08",
          "reuse": null
        },
        {
          "idx": 3,
          "type": "still",
          "id": "S02",
          "beat": "Eyes Widening",
          "start": 15,
          "duration": 5,
          "vo_text": "Your gut tightens...",
          "camera": "pan 0.05",
          "reuse": "keyframe_bookend:H1"
        },
        {
          "idx": 4,
          "type": "still",
          "id": "S03",
          "beat": "Memory Fragments",
          "start": 20,
          "duration": 5,
          "vo_text": "This is déjà vu...",
          "camera": "punch_in 1.2",
          "keyword": {"word": "recognition", "t": 2.8}
        },
        {
          "idx": 5,
          "type": "still",
          "id": "S04",
          "beat": "Settling Confusion",
          "start": 25,
          "duration": 5,
          "vo_text": "For centuries, we dismissed it...",
          "camera": "pull_out 0.05",
          "reuse": "harvest:H1"
        }
      ]
    },
    {
      "segment": 2,
      "time_range": "0:30–1:00",
      "act": "Science",
      "blocks": [
        {
          "idx": 6,
          "type": "hero",
          "id": "H2",
          "beat": "Neural Pathways Firing",
          "start": 30,
          "duration": 10,
          "vo_text": "Your memory isn't a recording device...",
          "peak_motion_t": 6.2,
          "reveal_word": "pattern-matching"
        },
        // ... S05–S08 (stills)
      ]
    },
    {
      "segment": 3,
      "time_range": "1:00–1:30",
      "act": "Symbolism",
      "blocks": [
        {
          "idx": 16,
          "type": "hero",
          "id": "H3",
          "beat": "Spiral of Recognition",
          "start": 60,
          "duration": 10,
          "vo_text": "What if déjà vu is the moment...",
          "peak_motion_t": 5.8
        },
        // ... S09–S12 (stills)
      ]
    },
    {
      "segment": 4,
      "time_range": "1:30–1:55",
      "act": "Reflection",
      "blocks": [
        {
          "idx": 21,
          "type": "hero",
          "id": "H4",
          "beat": "Return to Presence",
          "start": 90,
          "duration": 10,
          "vo_text": "So the next time you experience...",
          "peak_motion_t": 7.2,
          "reveal_word": "remembers",
          "note": "Trim last 2s for segment 4 (25s total). H4 10s + S13 5s + S14 5s + S15 remaining."
        },
        {
          "idx": 22,
          "type": "still",
          "id": "S13",
          "beat": "Observer Effect",
          "start": 100,
          "duration": 5,
          "camera": "push_in 0.04"
        },
        {
          "idx": 23,
          "type": "still",
          "id": "S14",
          "beat": "Memory as Living",
          "start": 105,
          "duration": 5,
          "camera": "pan 0.06"
        },
        {
          "idx": 24,
          "type": "still",
          "id": "S15",
          "beat": "Open Horizon",
          "start": 110,
          "duration": 5,
          "camera": "hold + dissolve 2s"
        }
      ]
    }
  ],
  "audio": {
    "vo_total_duration": 114.8,
    "vo_loudness_lufs": -20,
    "music_bed_duration": 115,
    "music_loudness_under_vo": -26,
    "master_loudness": -16
  },
  "cost": {
    "images": 28,
    "i2v": 60,
    "ffmpeg": 0,
    "audio": 0,
    "total": 88
  }
}
```

---

## PART 11: TEAM STRUCTURE & ROLES

For batch production (5 episodes):

| Role | Responsibilities | Hours per Episode |
|---|---|---|
| **Producer** | Story brief, beat selection, timeline management, QA | 2 h |
| **Script/VO Coordinator** | Script drafting, VO recording/TTS, sync validation | 3 h |
| **AI Image Specialist** | Prompt writing, image generation, upscaling, color check | 2.5 h |
| **I2V Specialist** | Hero prompt refining, I2V job submission, trimming, peak alignment | 1.5 h |
| **Audio Designer** | Ambient bed, SFX, mixing, ducking, loudness | 2 h |
| **Editor/Assembler** | Timeline building, sync, color grading, export | 2 h |
| **QA/Deliverables** | Checklist verification, metadata, documentation | 1.5 h |
| **TOTAL** | | **~14.5 h/ep** |

**Bottleneck:** I2V generation (10–15 min per clip, serial). Parallelize with image generation.

---

## PART 12: FUTURE ITERATIONS

### Automation Opportunities

- **Story generation:** Claude prompt → outline → script (2 h → 0.5 h).
- **Reuse mapping:** Automated based on hero duration + adjacent still position (manual → 5 min).
- **FFmpeg batch rendering:** Shell script (manual FFmpeg → 1 min bash execution).
- **Loudness validation:** Post-export script checking LUFS, reporting pass/fail.
- **Metadata template:** Pre-fill YouTube SEO fields based on title + keywords.

### Quality Improvements

- **Color grading LUT:** Create once per series, apply to all episodes → consistency.
- **Hero timing refinement:** Extract peak motion frame automatically, snap VO reveal to it.
- **VO quality:** Invest in professional voice actor (more natural than TTS) for flagship episodes.
- **Music licensing:** Commission original score (epic, 2–3 min loopable) instead of Splice.

### Scaling to 10+ Episodes

- **Production team:** Add dedicated I2V operator to parallelize image + I2V generation.
- **Story library:** Pre-write 20 episode concepts; rotate through topics.
- **Prompt templates:** Maintain versioned library; track which prompts generate best results.
- **Analytics feedback loop:** Track YouTube retention, CTR, audience sentiment → refine future scripts.

---

## APPENDIX A: BEAT SCORING REFERENCE

| Beat Type | Weight | Example |
|---|---|---|
| hook | 5 | Opening that grabs attention (disorientation in Act 1) |
| revelation | 5 | New information, insight (neural pathways lighting up) |
| climax | 5 | Emotional / narrative peak (eternal return spiral) |
| transformation | 4 | Visible change in subject (chrysalis opening, falling) |
| payoff | 4 | CTA, resolution, integration (return to presence) |
| action | 4 | Movement-driven beat (chase, metamorphosis, neural activity) |
| chapter_open | 3 | Act boundary (transition from Science to Symbolism) |
| emotional_peak | 3 | Feeling moment (awe, wonder, peace) |
| setup | 1 | Exposition, context |
| explain | 0 | Data, diagram (stills only; no I2V for stationary content) |
| data | 0 | Numbers, text |
| transition | 0 | Link between acts (stills only) |

---

## APPENDIX B: COLOR PALETTE TEMPLATES

Use one palette per episode for consistency.

### Template 1: Indigo + Gold (11:11)
```
Primary:    #1a1f3a (Deep Indigo, mysterious)
Accent:     #d4a574 (Warm Gold, spiritual)
Highlight:  #f5f3f0 (Cream, calm)
Shadow:     #5a6e8f (Slate, grounding)
```

### Template 2: Charcoal + Bronze (Crows)
```
Primary:    #1a1a1f (Charcoal, intelligence)
Accent:     #8b6f47 (Bronze, warmth)
Highlight:  #f5f3f0 (Cream)
Shadow:     #5a6e8f (Slate)
```

### Template 3: Deep Purple + Lavender (Butterflies)
```
Primary:    #2d1b3d (Deep Purple, transformation)
Accent:     #c084e8 (Lavender, emergence)
Highlight:  #f5f3f0 (Cream)
Shadow:     #5a6e8f (Slate)
```

### Template 4: Navy + Teal (Dreams)
```
Primary:    #0f1419 (Navy, dream state)
Accent:     #5eb3b3 (Teal, consciousness)
Highlight:  #f5f3f0 (Cream)
Shadow:     #5a6e8f (Slate)
```

### Template 5: Midnight + Silver (Déjà Vu)
```
Primary:    #0a0e27 (Deep Midnight, uncanny)
Accent:     #e8e8e8 (Silver White, familiarity)
Highlight:  #f5f3f0 (Cream, clarity)
Shadow:     #4a1a6f (Deep Plum, mystery)
```

---

## APPENDIX C: TROUBLESHOOTING

| Issue | Cause | Fix |
|---|---|---|
| I2V hero ramps in too slowly (motion doesn't start until 2–3 s) | Model default behavior (model tends to ease-in) | Prompt "mid-action on frame 1"; trim head 0.5–2 s after generation |
| VO block < 3 s (too short for still) | Over-condensed script | Merge with adjacent block; add padding |
| VO block > 8 s (too long for single still) | Over-wordy narration | Split into 2 stills; edit VO for brevity |
| Hero VO > 6.5 s | Hero should have breathing room | Trim VO line; reduce I2V duration to 8–9 s |
| Color palette not matching prompts | Prompt language not precise enough | Add exact hex codes to all image prompts; reference palette by name |
| FFmpeg zoompan not smooth | Frame rate mismatch or low fps | Ensure 30 FPS input; use `fps=30` in filter |
| Master audio clips at peaks | Compression not applied | Add limiter: `alimiter=limit=0.0`; reduce VO volume −2 dB |
| VO sync drifts over time | Audio delay accumulation | Check audio codec; render as PCM; re-sync per segment |
| Keyword punch timing off | Whisper forced alignment inaccurate | Use human VO with manual timestamp; verify in playback |

---

## APPENDIX D: RESOURCES & LINKS

**Inspiration & Analysis:**
- Meaning Channel on YouTube (all published episodes).
- Theory: Joseph Campbell's *The Hero with a Thousand Faces*, Carl Jung *Man and His Symbols*.

**Tools & Platforms:**
- Image gen: [Midjourney](https://midjourney.com), [Flux](https://flux.ai).
- I2V: [Runway Gen-3](https://runwayml.com), [Adobe Firefly Motion](https://firefly.adobe.com).
- VO: [Google Cloud Wavenet](https://cloud.google.com/text-to-speech), [ElevenLabs](https://elevenlabs.io).
- Audio: [Reaper](https://www.reaper.fm), [Audacity](https://www.audacityteam.org).
- Editing: [Adobe Premiere Pro](https://adobe.com), [DaVinci Resolve](https://www.davinciresolve.com).

**FFmpeg Docs:**
- [Zoompan filter](https://ffmpeg.org/ffmpeg-filters.html#zoompan).
- [Loudness / LUFS](https://ffmpeg.org/ffmpeg-filters.html#loudness).

**Community:**
- r/audiovisual (discussion, feedback).
- Runway community ([runwayml.com/community](https://runwayml.com/community)).
- Midjourney docs ([docs.midjourney.com](https://docs.midjourney.com)).

---

## VERSION HISTORY

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-10-01 | Original: 26 images + 7 heroes per episode |
| 2.0 | 2026-10-11 | **Hybrid I2V + FFmpeg pipeline: 4 heroes + 15 stills + 14 images per episode** |

---

## SIGN-OFF

**SOP Owner:** Meaning Channel Production Team  
**Last Reviewed:** 2026-10-11  
**Next Review:** After episode 6 production complete  
**Contact:** [team email]

---

**End of SOP**

