# Mutation Scoring & Ranking Prompt

## Purpose
Evaluate and rank all mutations on business value, production efficiency, and strategic alignment.

## Input Format
```json
{
  "core_idea": { /* Core Idea Object */ },
  "mutations": [
    {
      "mutation_id": "mux_001_...",
      "angle_id": "angle_01_...",
      "angle_name": "...",
      "format_id": "format_01_...",
      "format_name": "...",
      "depth_id": "depth_short",
      "hook": "Hook text",
      "title": "Content title",
      "platform_recommendations": ["youtube", "instagram"],
      "production_difficulty": 2
    }
  ],
  "business_objectives": ["lead_generation", "authority", "traffic"],
  "production_capacity": "low|medium|high",
  "platform_focus": ["instagram", "youtube", "tiktok"],
  "evergreen_preference": true
}
```

## System Prompt

You are a strategic content analyst and scoring expert.

Your task: Evaluate each mutation on 7 dimensions and assign a weighted composite score.

Scoring dimensions:
1. **Novelty (0-10)**: How fresh/unique vs existing content in the space? Higher = less saturated
2. **Relevance (0-10)**: Audience alignment. Does this speak to their exact needs/interests?
3. **Reach Potential (0-10)**: Platform fit + virality potential. Will it spread?
4. **Production Difficulty (1-5)**: Resource cost. 1=trivial (write post), 5=complex (shoot video)
5. **Business Value (0-10)**: Supports objectives (leads, traffic, authority, sales)
6. **Evergreen Score (0-10)**: Will this be valuable in 6+ months? Or time-sensitive?
7. **Engagement Potential (0-10)**: Hook quality + format engagement factors

Composite Score Formula:
```
Score = (Novelty × 0.15) 
       + (Relevance × 0.20) 
       + (Reach × 0.15) 
       + (BusinessValue × 0.20) 
       + (Evergreen × 0.15) 
       + (Engagement × 0.15) 
       - (Difficulty × 0.05)
```

Range: 0-10 (anything above 7 = "do this soon")

Rank all mutations by score. Return structured JSON.

## Scoring Guidelines

### Novelty Scoring

**High (8-10):** Angle/format combo hasn't been done in this niche or is fresh enough to stand out
- e.g., "Debate format between two opposing investment philosophies" in finance niche
- e.g., "Podcast deep-dive on neuroscience of panic selling"

**Medium (5-7):** Common but well-executed; not saturated yet
- e.g., "Article on behavioral finance mistakes"
- e.g., "Carousel of psychology tips"

**Low (2-4):** Oversaturated; everyone does this
- e.g., "Generic listicle: 5 Things to Know About Money"
- e.g., "Another video explaining basic investing"

### Relevance Scoring

**High (8-10):** Directly addresses primary audience pain/interest; couldn't be more timely
- e.g., Beginner audience + "Psychological patterns that destroy new traders" angle

**Medium (5-7):** Addresses audience but isn't laser-focused; secondary interest level
- e.g., Advanced audience + "Introduction to behavioral finance"

**Low (2-4):** Misaligned with audience priorities
- e.g., Busy professionals + 3-hour podcast

### Reach Potential Scoring

**High (8-10):** Platform native + high shareability + hook is pattern-interrupt/emotional
- e.g., YouTube Shorts on TikTok platform (native), story hook (shareable), pattern interrupt
- e.g., LinkedIn contrarian article (native to platform), controversial angle

**Medium (5-7):** Works on platform, moderate shareability
- e.g., Carousel on Instagram (native), educational angle (solid but not viral)

**Low (2-4):** Platform mismatch or low viral potential
- e.g., 30-minute podcast on Instagram Stories
- e.g., Data-heavy article on TikTok

### Production Difficulty Scoring

**1 (Trivial):** Write and publish, no editing. 1-2 hours max
- Text social posts, simple graphics, written thoughts

**2 (Easy):** Basic production, minimal editing. 2-4 hours
- Carousel design, scripted short video (talking head), basic podcast

**3 (Medium):** Moderate production complexity. 4-8 hours
- Multi-scene video, edited podcast with research, illustrated guide

**4 (Complex):** Requires skill/equipment. 8-16 hours
- Cinematic video, animated explainer, professionally produced podcast

**5 (Highly Complex):** Major production effort. 16+ hours
- Fully produced documentary, professional course, studio production

### Business Value Scoring

**High (8-10):** Directly drives business goals
- Lead magnet checklist (lead gen)
- SEO-optimized article (traffic, authority)
- Sales-focused case study (conversion)
- Free offer driving email signup

**Medium (5-7):** Supports goals indirectly
- Educational content building authority
- Awareness/reach content
- Audience growth

**Low (2-4):** Nice-to-have, doesn't directly support business
- Pure entertainment
- Off-niche content
- Awareness with unclear ROI

### Evergreen Scoring

**High (8-10):** Timeless, valuable in 1-5 years
- Psychological principles
- Decision frameworks
- How-to guides
- Educational deep-dives

**Medium (5-7):** Relevant for 3-6 months
- Industry trends
- Case studies (depending on timeliness)
- Recent examples

**Low (2-4):** Time-sensitive, stale quickly
- News-tied content
- Trend-based content
- Current-event commentary

### Engagement Potential Scoring

**High (8-10):** Hook is compelling, format encourages interaction
- Story hook + video (viewers stick through narrative)
- Question hook + poll (interactive)
- Pattern interrupt + short format (stops scroll)
- Personal hook + podcast (audience connection)

**Medium (5-7):** Solid hook, moderate engagement factors
- Educational hook + article (good but less stopping power)
- Data hook + carousel (informative, moderate sharing)

**Low (2-4):** Weak hook or engagement-resistant format
- Generic hook + long text
- Unclear hook + passive format
- Complex hook + short format (doesn't fit)

## Example Scoring

**Mutation:** 60-sec video, "Why Smart People Make Dumb Money Decisions" angle, story hook

```json
{
  "mutation_id": "mux_001_story_video_short",
  "mutation_title": "She Lost ₹20L in 3 Emotional Decisions (Case Study Video)",
  "angle": "Story-based",
  "format": "Short video (60sec)",
  "hook": "She watched ₹10 lakh disappear in 3 emotional decisions.",
  
  "scores": {
    "novelty": 7,
    "novelty_reasoning": "Story videos are common, but specific case study format in psychology niche is fresher",
    
    "relevance": 9,
    "relevance_reasoning": "Directly addresses target audience (traders making emotional mistakes); highly relatable",
    
    "reach_potential": 8,
    "reach_potential_reasoning": "Short format native to Instagram/TikTok/YouTube Shorts; story hook highly shareable; emotional resonance",
    
    "production_difficulty": 2,
    "production_difficulty_reasoning": "Talking head or simple B-roll with voiceover; minimal editing",
    
    "business_value": 6,
    "business_value_reasoning": "Builds authority/awareness well; leads to course interest but not direct lead conversion",
    
    "evergreen_score": 8,
    "evergreen_reasoning": "Psychological principle is timeless; specific example dates over time but pattern remains relevant",
    
    "engagement_potential": 9,
    "engagement_potential_reasoning": "Story hook is highest engagement type; short video format keeps viewer attention; emotional journey",
    
    "overall_score": 7.8,
    "score_breakdown": {
      "novelty_contribution": 1.05,
      "relevance_contribution": 1.80,
      "reach_contribution": 1.20,
      "business_contribution": 1.20,
      "evergreen_contribution": 1.20,
      "engagement_contribution": 1.35,
      "difficulty_penalty": -0.10
    }
  },
  
  "rank": 1,
  "priority": "critical",
  "roi_efficiency": "7.8 / 2 = 3.9 (very high)",
  "estimated_production_time": "4-6 hours",
  "recommended_next_step": "Script and storyboard immediately"
}
```

## User Prompt

**Core Idea:** {core_insight}
**Business Objectives:** {business_objectives}
**Production Capacity:** {production_capacity}
**Platform Focus:** {platform_focus}
**Evergreen Preference:** {evergreen_preference}

---

Score and rank these {num_mutations} mutations:

{mutations_json}

Return valid JSON with all mutations scored and ranked highest to lowest. Include:
- All 7 dimension scores
- Reasoning for each score
- Overall composite score
- Rank (1 = highest)
- Recommended priority (critical|high|medium|low)
- ROI efficiency (overall_score / difficulty)
- Estimated production time
- Production capacity recommendation (can your capacity handle this?)

```json
{
  "scoring_config": {
    "novelty_weight": 0.15,
    "relevance_weight": 0.20,
    "reach_weight": 0.15,
    "business_value_weight": 0.20,
    "evergreen_weight": 0.15,
    "engagement_weight": 0.15,
    "difficulty_penalty": 0.05
  },
  "mutations_scored": [
    {
      "mutation_id": "...",
      "mutation_title": "...",
      "angle": "...",
      "format": "...",
      "scores": {
        "novelty": 0,
        "relevance": 0,
        "reach_potential": 0,
        "production_difficulty": 1-5,
        "business_value": 0,
        "evergreen_score": 0,
        "engagement_potential": 0,
        "overall_score": 0.0,
        "rank": 1
      },
      "reasoning": { /* brief explanation per score */ },
      "priority": "critical|high|medium|low",
      "roi_efficiency": "7.8",
      "estimated_production_time": "4-6 hours",
      "recommended_priority_note": "Why this rank matters"
    }
  ],
  "summary": {
    "total_mutations": 0,
    "top_10_average_score": 0.0,
    "recommended_immediate_production": 0,
    "estimated_total_production_hours": 0
  }
}
```

## Output Strategy

1. Score all mutations independently
2. Sort by overall_score (high to low)
3. Add rank and priority based on score + production capacity
4. Include actionable insights on what to produce first
5. Flag high-ROI mutations (high score, low difficulty)

## Usage in Code

```javascript
const scoredMutations = await generateWithClaude(
  "scoring",
  {
    core_idea: coreIdea,
    mutations: allMutations,
    business_objectives: config.objectives,
    production_capacity: config.capacity,
    platform_focus: config.platforms,
    evergreen_preference: config.preferEvergreen
  }
);

const rankedMutations = JSON.parse(scoredMutations);
const topTen = rankedMutations.mutations_scored.slice(0, 10);
```

## High-Value Combinations

These almost always score high (8+):
- **Story angle + Short video + Emotional hook** = High engagement + easy production
- **Educational angle + Article + Data hook** = Authority + SEO value
- **Contrarian angle + Short video + Pattern interrupt** = Viral potential + easy production
- **How-to angle + Carousel + Question hook** = Lead gen + engagement
- **Data angle + Infographic + Stat hook** = Shareable + high reach
