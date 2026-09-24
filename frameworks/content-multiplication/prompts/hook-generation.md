# Hook Generation Prompt

## Purpose
Generate 3-5 compelling hooks (opening lines) for each angle. Hooks are the critical difference between content that gets clicked/watched and content that gets scrolled past.

## Input Format
```json
{
  "angle_id": "angle_01_why_smart_fail",
  "angle_name": "Why Intelligent People Make Irrational Money Decisions",
  "hook_style": "question|curiosity|pattern_interrupt|emotional|data",
  "target_audience": "mixed",
  "niche": "behavioral finance",
  "core_insight": "Knowledge doesn't equal execution; emotions are more powerful than facts"
}
```

## System Prompt

You are a master copywriter specializing in attention-grabbing hooks.

Your task: Generate 3-5 different, high-impact opening lines for a specific angle and audience.

Each hook should:
- Stop scrolling/grab attention in 1-3 seconds
- Match the angle's style and intent
- Be specific (not generic)
- Tease the unique insight without fully revealing it
- Be authentically aligned with the angle (not clickbait)
- Work across multiple platforms

Avoid:
- "Here's X things about Y" (generic list intro)
- "You won't believe" or "This one trick" (cheap clickbait)
- Questions everyone asks (too common)
- Vague statements (no specificity)

Create hooks that create genuine curiosity, pattern interruption, or emotional resonance.

## User Prompt

**Angle:** {angle_name}
**Hook Style:** {hook_style}
**Audience:** {target_audience}
**Core Insight:** {core_insight}
**Niche:** {niche}

---

Generate 5 distinct, high-impact hooks for this angle. Return valid JSON:

```json
{
  "angle_id": "{angle_id}",
  "hooks": [
    {
      "id": "hook_01",
      "text": "The exact opening line",
      "type": "curiosity|pattern_interrupt|problem_statement|question|data|contrarian|story|emotional|personal",
      "impact_mechanism": "Why this hook works (what it triggers psychologically)",
      "platform_strength": ["platform_1", "platform_2"],
      "audience_appeal": "Why this resonates with the target audience",
      "estimated_ctr": 0.0-1.0,
      "variations": [
        "Alternative wording 1",
        "Alternative wording 2"
      ]
    }
  ]
}
```

## Hook Styles Explained

### Curiosity Hook
Creates an open loop the brain wants to close. Reveals outcome but not how/why.
- "The #1 mistake traders make isn't what you think."
- "There's a reason you lose money the same way every expert does."

### Pattern Interrupt
Breaks expected pattern or contradicts what people believe.
- "Stop trying to have discipline. Here's what actually works."
- "Financial education is making you worse at money."

### Problem Statement
Name the pain point with specificity and validation.
- "You know exactly what to do. You just don't do it. Here's why."
- "That ₹20L portfolio loss? It wasn't the market's fault."

### Question Hook
Pose a provocative, specific question (not rhetorical).
- "Why do people with MBAs panic-sell the same way beginners do?"
- "What would you do if your portfolio dropped 30% overnight?"

### Data Hook
Start with surprising statistic or fact.
- "80% of traders lose money despite having a documented strategy."
- "During the 2008 crash, panic selling wiped out gains from 5+ years."

### Contrarian Hook
Challenge conventional wisdom directly.
- "You've been taught financial discipline all wrong."
- "More knowledge isn't your problem. This is."

### Story Hook
Open with a specific scenario or character moment.
- "She watched ₹10 lakh disappear in 3 emotional decisions."
- "On March 23, 2020, he learned the most expensive lesson of his life."

### Emotional Hook
Tap into fear, desire, or identity.
- "Your biggest trading enemy isn't volatility. It's you."
- "Every time you panic-sell, you're betting against your future self."

### Personal Hook
First-person realization or vulnerability.
- "I knew I shouldn't sell. I sold anyway. Here's what I learned."
- "The moment I realized: discipline doesn't matter without systems."

## Example Output

For angle: "Why Intelligent People Make Irrational Money Decisions"

```json
{
  "angle_id": "angle_01_why_smart_fail",
  "hooks": [
    {
      "id": "hook_01",
      "text": "Why do people with MBAs panic-sell the same way beginners do?",
      "type": "question",
      "impact_mechanism": "Creates immediate curiosity and cognitive dissonance (MBAs should know better)",
      "platform_strength": ["linkedin", "twitter", "instagram"],
      "audience_appeal": "Appeals to intelligent audience's self-image while teasing a gap in their knowledge",
      "estimated_ctr": 0.35,
      "variations": [
        "Intelligent investors panic-sell just like everyone else. Here's why.",
        "Your MBA won't save you from this psychological trap."
      ]
    },
    {
      "id": "hook_02",
      "text": "Knowledge doesn't equal execution. Emotions are 10x more powerful.",
      "type": "pattern_interrupt",
      "impact_mechanism": "Directly contradicts what audience has been taught (study = success)",
      "platform_strength": ["youtube", "tiktok", "instagram_reels"],
      "audience_appeal": "Validating (you're not failing because you're stupid) while revealing new insight",
      "estimated_ctr": 0.28,
      "variations": [
        "Here's why everything you learned about financial discipline is wrong.",
        "You know what to do. Emotions prevent you from doing it."
      ]
    },
    {
      "id": "hook_03",
      "text": "She watched ₹10 lakh disappear in 3 emotional decisions. Here's how.",
      "type": "story",
      "impact_mechanism": "Specific monetary loss triggers emotional resonance; narrative promise draws in listener",
      "platform_strength": ["youtube", "podcast", "linkedin"],
      "audience_appeal": "Relatability + cautionary tale creates fear + curiosity",
      "estimated_ctr": 0.42,
      "variations": [
        "The day this successful trader lost everything: an emotional decision breakdown.",
        "₹10 lakh gone in 3 choices. A trader's psychology breakdown."
      ]
    },
    {
      "id": "hook_04",
      "text": "Your biggest trading enemy isn't volatility. It's you.",
      "type": "emotional",
      "impact_mechanism": "Shifts blame from external market to internal control (empowering but challenging)",
      "platform_strength": ["instagram", "twitter", "youtube_shorts"],
      "audience_appeal": "Creates identity challenge while suggesting solution is in their hands",
      "estimated_ctr": 0.32,
      "variations": [
        "The real market crash happens inside your head.",
        "You're not losing money to market conditions. You're losing it to yourself."
      ]
    },
    {
      "id": "hook_05",
      "text": "During 2008, panic selling destroyed gains earned over 5+ years in days.",
      "type": "data",
      "impact_mechanism": "Provides evidence/validation + stakes (years of progress lost instantly)",
      "platform_strength": ["linkedin", "twitter", "blog"],
      "audience_appeal": "For analytical audience; proven pattern from history",
      "estimated_ctr": 0.25,
      "variations": [
        "Historical market crashes reveal a consistent psychological pattern.",
        "Every major crash shows the same psychological behavior. Here's the pattern."
      ]
    }
  ]
}
```

## Usage in Code

```javascript
// Generate hooks for each angle
const allHooks = [];
for (const angle of parsedAngles.angles) {
  const hooks = await generateWithClaude(
    "hook-generation",
    {
      angle_id: angle.id,
      angle_name: angle.name,
      hook_style: angle.hook_style,
      target_audience: userInput.audience,
      niche: userInput.niche,
      core_insight: userInput.core_insight
    }
  );
  
  allHooks.push(JSON.parse(hooks));
}
```

## Integration

Hooks feed into:
- **Format selection**: Different formats need different hook types
- **Platform adaptation**: Short platforms (TikTok) need punchier hooks
- **CTR prediction**: Hook type + audience = estimated click-through rate
- **Scoring**: High-quality hooks increase engagement potential score
