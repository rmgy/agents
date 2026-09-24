# Angle Generation Prompt

## Purpose
Generate 15-20 unique editorial angles from a deconstructed Core Idea. Each angle is a distinct way to present/frame the same core insight.

## Input Format
```json
{
  "core_idea_object": { /* full Core Idea Object from deconstruction */ },
  "target_audience": "string",
  "niche": "string",
  "num_angles": 15
}
```

## System Prompt

You are a content strategist and creative director. Your specialty: taking a single insight and finding 15+ completely different, unique, valuable ways to frame and present it.

Each angle should:
- Be distinct from others (not slight variations)
- Be valuable to the audience
- Be defensible in itself (could stand alone as content)
- Have a clear hook style
- Be actionable/producible

Avoid generic angles like "beginner's guide" or "advanced tips". Get specific.

## User Prompt

**Core Idea:**
{core_insight}

**Target Audience:**
{target_audience}

**Niche:**
{niche}

**Problem:** {problem}
**Root Cause:** {root_cause}
**Contrarian Angle:** {contrarian_angle}
**Psychological Mechanisms:** {psychological_mechanisms}
**Framework:** {framework_name}

---

Generate 15-20 unique editorial angles to present this idea. Return valid JSON:

```json
{
  "angles": [
    {
      "id": "angle_01_unique_slug",
      "name": "Angle Name",
      "description": "What makes this angle unique and valuable?",
      "hook_style": "curiosity|pattern_interrupt|problem_statement|question|data|contrarian|story|emotional|personal",
      "sample_hook": "Sample opening line that would grab attention",
      "key_message": "The central claim of this angle",
      "audience_fit": "beginner|intermediate|advanced|mixed",
      "content_strength": "Why this angle works for this audience",
      "potential_formats": ["format_1", "format_2"],
      "estimated_novelty": 0-10,
      "reasoning": "Why this is a distinct angle"
    }
  ]
}
```

## Angle Types to Consider

- **Educational**: Explain the mechanism/principle in depth
- **Contrarian**: Challenge a widely-held belief
- **Story-based**: Lead with narrative or character arc
- **Data-driven**: Use statistics, trends, historical patterns
- **How-to/Action**: Practical steps to apply the insight
- **Mistake-based**: Showcase common errors
- **Myth-busting**: Debunk a false belief
- **Question-based**: Frame as exploration of a provocative question
- **Beginner-friendly**: Simplify for newcomers
- **Advanced**: Deep dive for experts
- **Personal/Reflection**: First-person realization or journey
- **Debate/Dialogue**: Present opposing views
- **Framework-based**: Introduce a structured model
- **Checklist**: Tactical, actionable takeaways
- **Analogy**: Use metaphor/comparison to explain
- **Prediction/Scenario**: "What if?" thinking
- **Philosophical**: Explore deeper principles/meaning
- **Experiment/Challenge**: Invite audience participation
- **Time-based**: Historical pattern, future trend, timeless principle
- **Psychological**: Deep dive into human behavior drivers

## Example Output

For idea: "Emotions override financial knowledge"

```json
{
  "angles": [
    {
      "id": "angle_01_why_smart_fail",
      "name": "Why Intelligent People Make Irrational Money Decisions",
      "description": "Deep exploration of how IQ and financial knowledge don't protect you from emotional mistakes",
      "hook_style": "question",
      "sample_hook": "Why do people with MBAs panic-sell the same way beginners do?",
      "key_message": "Knowledge doesn't equal execution; emotions are more powerful than facts",
      "audience_fit": "mixed",
      "content_strength": "Appeals to ego (we think we're smarter) and creates curiosity",
      "potential_formats": ["article", "video_essay", "podcast"],
      "estimated_novelty": 8,
      "reasoning": "Directly addresses the psychological gap between knowledge and action"
    },
    {
      "id": "angle_02_behavioral_patterns",
      "name": "5 Psychological Patterns That Make You Lose Money",
      "description": "Specific psychological biases that trigger poor financial decisions, with recognition checklist",
      "hook_style": "pattern_interrupt",
      "sample_hook": "You've probably lost money to one of these 5 mental patterns without realizing it",
      "key_message": "If you can recognize the pattern, you can break the cycle",
      "audience_fit": "beginner",
      "content_strength": "Educational, actionable, formatters well into lists/carousels",
      "potential_formats": ["carousel", "checklist", "infographic"],
      "estimated_novelty": 6,
      "reasoning": "Good entry point for newcomers; breaks complex psychology into digestible pieces"
    },
    {
      "id": "angle_03_panic_selling_case",
      "name": "The Day She Sold at the Bottom: A ₹20L Mistake",
      "description": "Detailed case study of a specific investor's panic-sell decision, causes, and lessons",
      "hook_style": "story",
      "sample_hook": "She watched her portfolio rise for 5 years. Then one market day, she erased all gains.",
      "key_message": "Even experienced investors fall prey to emotional decision-making under stress",
      "audience_fit": "mixed",
      "content_strength": "Narrative drives engagement and relatability; memorable structure",
      "potential_formats": ["long_video", "article", "podcast"],
      "estimated_novelty": 7,
      "reasoning": "Stories stick; case study + emotional consequence creates strong takeaway"
    },
    {
      "id": "angle_04_systems_over_discipline",
      "name": "Build Systems That Protect You From Yourself",
      "description": "How to design decision frameworks and automated safeguards instead of relying on willpower",
      "hook_style": "contrarian",
      "sample_hook": "Stop trying to have 'discipline.' Design a system that doesn't require it.",
      "key_message": "Systems > willpower. Automate your decisions before emotions can override them.",
      "audience_fit": "intermediate",
      "content_strength": "Actionable, empowering, solves the core problem",
      "potential_formats": ["how_to_guide", "framework", "video"],
      "estimated_novelty": 9,
      "reasoning": "Shifts from explaining problem to providing real solution; high value"
    }
  ]
}
```

## Usage in Code

```javascript
const angles = await generateWithClaude(
  "angle-generation",
  {
    core_idea_object: coreIdea,
    target_audience: userInput.audience,
    niche: userInput.niche,
    num_angles: 18
  }
);

const parsedAngles = JSON.parse(angles);
```

## Integration with Downstream Steps

Each angle ID will be used in:
- Hook generation (angle_01_why_smart_fail → creates hooks specific to that angle)
- Format selection (angle_02_behavioral_patterns → carousel-friendly angle)
- Platform adaptation (angle_03_panic_selling_case → narrative-friendly platforms like YouTube)
- Scoring (novelty, reach potential, business value based on angle type)
