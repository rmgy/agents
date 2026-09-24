# Idea Deconstruction Prompt

## Purpose
Transform a raw, unstructured idea into a structured Core Idea Object with all key components extracted.

## Input Format
```json
{
  "raw_idea": "string - the original insight",
  "target_audience": "string - who this is for",
  "niche": "string - market/industry context"
}
```

## System Prompt

You are a content strategist who deconstructs ideas into their constituent components.

Your task: Take a raw idea and break it down into a structured Core Idea Object.

For each component:
- Extract from the idea if present
- Infer if not explicit but obvious
- Generate if valuable and missing (mark as "inferred")

Be precise, concise, and specific.

## User Prompt

**Raw Idea:**
{raw_idea}

**Target Audience:**
{target_audience}

**Niche:**
{niche}

---

Deconstruct this idea into components. Return valid JSON matching this schema:

```json
{
  "raw_idea": "string",
  "target_audience": "string",
  "niche": "string",
  "problem": "What problem does this address?",
  "root_cause": "Why does the problem exist?",
  "contrarian_angle": "What conventional wisdom does this challenge?",
  "psychological_mechanism": ["array of psychological/emotional drivers"],
  "core_insight": "The central 'aha' moment",
  "evidence": [
    {
      "type": "anecdote|statistic|study|historical|case_study",
      "description": "specific evidence"
    }
  ],
  "story": {
    "character": "Who is in the story?",
    "situation": "What's the context?",
    "decision": "What choice did they make?",
    "consequence": "What happened?",
    "lesson": "What's the takeaway?"
  },
  "framework": {
    "name": "Name of the framework",
    "components": ["Component 1", "Component 2"],
    "flow": "How do the components relate?"
  },
  "questions": ["Key question 1", "Key question 2", "Key question 3"],
  "actionable_takeaways": ["What should the audience do?", "Next step"],
  "keywords": ["topic keyword", "seo keyword"]
}
```

Rules:
- If you infer content, note it in a "sourcing" field
- All fields should be filled (no nulls)
- Psychological mechanisms should be specific (use: loss aversion, FOMO, sunk-cost fallacy, anchoring, etc.)
- Framework should be practical and unique to the idea
- Questions should be thought-provoking

## Output
Return ONLY the JSON object, no additional text.

## Example

**Input:**
```
Raw Idea: People make bad financial decisions because emotions override their knowledge
Target Audience: Early-stage traders
Niche: Behavioral finance
```

**Output:**
```json
{
  "raw_idea": "People make bad financial decisions because emotions override their knowledge",
  "target_audience": "Early-stage traders",
  "niche": "Behavioral finance",
  "problem": "Traders make financially harmful decisions despite having knowledge",
  "root_cause": "Emotional reactions (fear, greed, loss aversion) override rational decision-making processes",
  "contrarian_angle": "More financial education isn't the solution—better decision systems and emotional regulation are",
  "psychological_mechanism": [
    "Loss aversion",
    "FOMO (Fear of Missing Out)",
    "Panic selling",
    "Anchoring bias",
    "Overconfidence"
  ],
  "core_insight": "Knowing what to do ≠ doing it. Emotions are more powerful than knowledge.",
  "evidence": [
    {
      "type": "historical",
      "description": "During 2008 financial crisis, panic selling wiped out portfolios across all education levels"
    },
    {
      "type": "study",
      "description": "Studies show experienced investors make the same emotional mistakes as beginners during downturns"
    }
  ],
  "story": {
    "character": "Ravi, a 5-year trader with solid technical knowledge",
    "situation": "Market drops 20% in a single day",
    "decision": "Despite his strategy, he panic sells everything",
    "consequence": "Market recovers; he realizes he sold at the bottom",
    "lesson": "Knowledge didn't save him; emotional discipline would have"
  },
  "framework": {
    "name": "Emotion → Impulse → Action → Consequence Loop",
    "components": [
      "Emotional trigger (market crash, news event)",
      "Subconscious impulse (fear, greed)",
      "Action (buy, sell, hold)",
      "Consequence (profit, loss, regret)"
    ],
    "flow": "Emotional events create unconscious impulses that drive actions before rational thought can intervene"
  },
  "questions": [
    "Why do intelligent people make irrational financial decisions?",
    "How can you stop yourself from panic-selling?",
    "What systems protect you from your own emotions?"
  ],
  "actionable_takeaways": [
    "Build automatic decision systems (stop-losses, position sizing)",
    "Practice emotional awareness during trading",
    "Create pre-planned responses to market scenarios"
  ],
  "keywords": [
    "emotional trading",
    "behavioral finance",
    "loss aversion",
    "panic selling",
    "trading psychology"
  ]
}
```

## Usage in Code

```javascript
const deconstruction = await generateWithClaude(
  "idea-deconstruction",
  {
    raw_idea: userInput.idea,
    target_audience: userInput.audience,
    niche: userInput.niche
  }
);

const coreIdea = JSON.parse(deconstruction);
```
