# Content Multiplication Framework

Transform single ideas into a portfolio of content across angles, formats, and platforms.

## Core Concept

One **Core Idea** → **Content Mutation Matrix** → **Scored Content Portfolio** → **Production Queue**

Instead of:
- Generating content once
- Repeating it across platforms

Do:
- Deconstruct the idea
- Generate 50+ mutations (angles × formats × depths)
- Score for novelty, relevance, difficulty, business value
- Select top N for production

## Architecture

### 1. **Core Idea Schema** (`schemas/core-idea.json`)
Structure for ingesting and deconstructing ideas:
- Problem statement
- Root cause/insight
- Psychological/emotional mechanism
- Contrarian element
- Evidence/examples
- Frameworks
- Questions
- Takeaways

### 2. **Mutation Matrix Schema** (`schemas/mutation-matrix.json`)
Defines mutation dimensions:
- **Angles**: Educational, Contrarian, Story, Data, How-to, etc.
- **Formats**: Video, Carousel, Article, Podcast, Infographic, Tool, etc.
- **Depths**: 30sec, 3min, 10min, 30min, long-form
- **Audiences**: Beginner, Intermediate, Advanced
- **Intents**: Learn, Feel, Act, Debate
- **Platforms**: YouTube, Instagram, LinkedIn, X, TikTok, Blog, Email

### 3. **Prompts** (`prompts/`)
- `idea-deconstruction.md` — Break down raw idea into structured components
- `angle-generation.md` — Generate 15-20 unique angles
- `hook-generation.md` — Create compelling hooks for each angle
- `mutation-selection.md` — Recommend angles × formats × depths
- `scoring.md` — Evaluate mutations on novelty, relevance, difficulty, ROI

### 4. **Implementation** (`lib/`)
- `mutation-engine.js` — Main class coordinating the pipeline
- `scorer.js` — Scoring logic (novelty, relevance, production difficulty, business value)
- `formatter.js` — Convert mutations to structured output

### 5. **Examples** (`examples/`)
Pre-built mutation matrices for reference.

## Quick Start

### Step 1: Define Your Core Idea
```json
{
  "raw_idea": "Your insight here",
  "audience": "Target persona",
  "niche": "Your market"
}
```

### Step 2: Run Mutation Engine
```javascript
const engine = new ContentMutationEngine();
const mutations = await engine.deconstruct(coreIdea)
  .generateAngles()
  .generateHooks()
  .selectMutations()
  .score();
```

### Step 3: Review & Select
Filter by:
- Format priority
- Platform focus
- Production difficulty
- Business alignment

### Step 4: Queue for Production
Export top N mutations to your content calendar/production system.

## Workflow Stages

### Stage 1: Deconstruction
Input: Raw idea + audience
Output: Structured Core Idea Object
- Problem
- Cause/Insight
- Psychological mechanism
- Contrarian element
- Example
- Story
- Framework
- Questions
- Takeaway

### Stage 2: Angle Generation
Input: Core Idea Object
Output: 15-20 unique angles
- Educational
- Contrarian
- Story-based
- Data-driven
- How-to
- Mistake-based
- Myth-busting
- Question-based
- Beginner-friendly
- Advanced
- Personal reflection
- Debate
- Framework-based
- Checklist
- Analogy
- Prediction
- Philosophy
- Experiment

### Stage 3: Hook Generation
Input: Core Idea + Angles
Output: 3-5 compelling hooks per angle
- Pattern interrupt hooks
- Curiosity hooks
- Problem-statement hooks
- Question hooks
- Data hooks
- Contrarian hooks
- Story hooks

### Stage 4: Format Selection
Input: Angles + Hooks
Output: Recommended format combinations
- Video (short/long)
- Carousel
- Article (micro/medium/long)
- Podcast (solo/interview/clip)
- Infographic
- Interactive (poll/quiz)
- Utility (checklist/template)
- Lead magnet

### Stage 5: Platform Adaptation
Input: Format + Angle
Output: Platform-specific variants
- Length adjustments
- Visual specifications
- CTA strategies
- Hashtag recommendations

### Stage 6: Scoring & Ranking
Input: All mutations
Output: Ranked portfolio
Scores on:
- **Novelty** (0-10): How fresh vs. existing content
- **Relevance** (0-10): Audience alignment
- **Reach Potential** (0-10): Platform fit + shareability
- **Production Difficulty** (1-5): Resource cost
- **Business Value** (0-10): Lead gen / traffic / authority / sales
- **Evergreen Score** (0-10): Long-term validity
- **Engagement Potential** (0-10): Hook strength + format

**Overall Score** = (Novelty × 0.15) + (Relevance × 0.20) + (Reach × 0.15) + (BusinessValue × 0.20) + (Evergreen × 0.15) + (Engagement × 0.15) - (Difficulty × 0.05)

## Example Flow

**Raw Idea:** "Emotions override financial knowledge in decision-making"

**Deconstruction:**
- Problem: People make financially harmful decisions
- Cause: Emotion overrides knowledge
- Insight: Knowing ≠ doing
- Mechanism: Loss aversion, fear, FOMO
- Contrarian: More education isn't the solution
- Example: Panic selling during crashes

**Angles Generated:**
1. Educational: Why emotions affect decisions
2. Contrarian: Financial education may not help
3. Story: Investor loses ₹10L due to one emotional decision
4. Data: Historical crash behavior patterns
5. How-to: Stop yourself from panic-selling
6. Myth-busting: "Rational investors don't experience fear"
7. Psychological: Your brain treats market loss as physical threat
8. Framework: Emotion → Impulse → Action → Consequence loop

**Hooks (per angle):**
- "Your biggest trading enemy isn't volatility. It's you."
- "Why knowing better doesn't stop you from doing worse."
- "She watched ₹10 lakh disappear in 3 emotional decisions."

**Format Options:**
- 60-sec video (Angle 1 + Hook 1)
- 8-slide carousel (Angle 5 + Hook 2)
- 2,000-word article (Angle 2 + Hook 3)
- 5-minute podcast (Angle 7 + Hook 4)
- Checklist tool (Angle 5 + Hook 2)
- Lead magnet guide (Angle 1 + 2 + 5)

**Scores & Ranking:**
Format: 60-sec video | Angle: Educational | Hook: "Your biggest trading enemy..."
- Novelty: 7/10
- Relevance: 9/10
- Reach: 8/10
- Production Difficulty: 2/5
- Business Value: 6/10
- Evergreen: 7/10
- Engagement: 8/10
- **Overall: 7.6/10** ← High ROI, easy production

## Integration Points

### With n8n
- Trigger: Idea submitted
- Step 1: Call mutation engine (API)
- Step 2: Score mutations
- Step 3: Route top 10 to production dashboard
- Step 4: Generate calendar entries

### With Claude Projects
- Use mutation prompts within custom agents
- Embed scorer in content review workflows

### With Your Content Calendar
- Export mutations as structured JSON
- Auto-populate with platform specs
- Link to production templates

## Cost Optimization

- **Haiku**: Deconstruction, angle generation, basic hooks
- **Sonnet**: Hook refinement, platform adaptation, edge cases
- **Opus**: Only for complex scoring logic or unusual niches (rare)

Default: Haiku first, escalate only if needed.

## Files in This Framework

```
frameworks/content-multiplication/
├── README.md (this file)
├── schemas/
│   ├── core-idea.json
│   ├── mutation-matrix.json
│   └── scored-mutation.json
├── prompts/
│   ├── idea-deconstruction.md
│   ├── angle-generation.md
│   ├── hook-generation.md
│   ├── format-selection.md
│   ├── platform-adaptation.md
│   └── scoring.md
├── lib/
│   ├── mutation-engine.js
│   ├── scorer.js
│   ├── formatter.js
│   └── index.js
├── examples/
│   ├── financial-decision-making.json
│   └── behavioral-psychology.json
└── workflows/
    └── n8n-workflow-template.json
```

## Next Steps

1. Review the schemas (understand data structure)
2. Read the prompts (understand mutation logic)
3. Try the examples (see it in action)
4. Integrate with your system (API/n8n/custom)
5. Run on your own ideas
