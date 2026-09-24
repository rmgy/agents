# Content Multiplication Framework — Quickstart Guide

**What you'll do:** Transform 1 core idea into 10 high-scoring content mutations ready for production in ~2 hours.

---

## 5-Minute Overview

The framework has 6 stages:

1. **Deconstruction** (15 min) — Break raw idea into structure
2. **Angle Generation** (15 min) — Generate 15-20 unique perspectives
3. **Hook Generation** (15 min) — Create 3-5 compelling opening lines per angle
4. **Mutation Creation** (15 min) — Combine angles + hooks + formats
5. **Scoring** (30 min) — Rank by business value, ease, engagement
6. **Selection** (5 min) — Pick top 10 for production queue

**Total time:** ~90 minutes for a complete portfolio

---

## Prerequisites

- 1 core idea or insight (doesn't need to be perfect)
- Target audience persona
- Business goals (lead gen, traffic, authority, reach, etc.)
- Claude API access (or Claude.ai with projects)

---

## Step 1: Prepare Your Idea

Before you start, define:

```json
{
  "raw_idea": "Your core insight (1-2 sentences)",
  "target_audience": "Who is this for? (e.g., 'Early-stage traders')",
  "niche": "Market/industry (e.g., 'Behavioral finance')",
  "business_objectives": ["authority", "reach", "lead_generation"],
  "production_capacity": "low|medium|high"
}
```

**Example:**
```json
{
  "raw_idea": "People make bad financial decisions because emotions override knowledge",
  "target_audience": "Early-stage traders",
  "niche": "Behavioral finance",
  "business_objectives": ["authority", "reach"],
  "production_capacity": "medium"
}
```

---

## Step 2: Run the Pipeline

### Option A: Using Claude Projects (Easiest)

1. Go to [claude.ai/projects](https://claude.ai/projects)
2. Create new project
3. Upload the prompts folder (`prompts/`)
4. Create these custom instructions in your project:

```
You are a Content Multiplication Engine.

Your job: Transform ideas into scored content portfolios.

Process:
1. Use the "idea-deconstruction" prompt to deconstruct the user's raw idea
2. Use "angle-generation" to create 18 unique angles
3. Use "hook-generation" to create 3-5 hooks per angle
4. Use "scoring" to rank and score all mutations

For each step:
- Wait for user feedback before proceeding
- Show intermediate results
- Ask clarifying questions if needed
- Provide scoring rationale

Output format:
- Always return valid JSON
- Include reasoning for each decision
- Provide actionable next steps
```

5. Paste your idea and follow the prompts through each stage

### Option B: Using the CLI

```bash
# Install the framework locally
npm install @anthropic-ai/sdk

# Create script: run-mutation-engine.js
const ContentMutationEngine = require('./lib/mutation-engine');
const Anthropic = require('@anthropic-ai/sdk');

const engine = new ContentMutationEngine({
  model: 'claude-haiku-4-5-20251001',
  businessObjectives: ['authority', 'reach'],
  platformFocus: ['youtube', 'instagram', 'linkedin']
});

// Run the full pipeline
const portfolio = await engine.run({
  raw_idea: "People make bad financial decisions because emotions override knowledge",
  target_audience: "Early-stage traders",
  niche: "Behavioral finance"
});

console.log(JSON.stringify(portfolio, null, 2));
```

### Option C: Manual (Step-by-Step in Claude)

Open Claude and follow this flow:

**Step 1: Copy the idea-deconstruction prompt**
1. Open `prompts/idea-deconstruction.md`
2. Copy the entire System Prompt + User Prompt template
3. Paste into Claude
4. Replace `{raw_idea}`, `{target_audience}`, `{niche}` with your values
5. Let Claude return the Core Idea Object (JSON)

**Step 2: Copy the angle-generation prompt**
1. Open `prompts/angle-generation.md`
2. Copy the prompt
3. Paste Claude's Core Idea Object output into the prompt
4. Run and collect the angles JSON

**Step 3: Repeat for hooks, then scoring**
- Same process for each prompt
- Feed output from previous step into next prompt
- Collect final scored mutations

---

## Step 3: Review Results

Look at the output portfolio. The top 10 mutations should show:

```json
{
  "rank": 1,
  "mutation_title": "Short Video: Story Angle",
  "overall_score": 7.8,
  "production_difficulty": 2,
  "estimated_production_time": "4-6 hours",
  "priority": "critical",
  "roi_efficiency": 3.9
}
```

**What makes a good mutation score:**
- **Score 8+** = Do this first (exceptional)
- **Score 7-8** = High value (important)
- **Score 6-7** = Good addition (useful)
- **Score <6** = Lower priority (skip for now)

**What makes good ROI:**
- **ROI > 3.0** = Excellent (high score, low effort)
- **ROI 2-3** = Good (solid score, reasonable effort)
- **ROI < 2** = Less efficient (high effort needed)

---

## Step 4: Production Queue

Export the top 10 as your production roadmap:

```markdown
# Content Production Queue (65 hours total)

## Phase 1: Quick Wins (12 hours) — Start this week
1. Checklist (1-2 hours) — HIGHEST ROI
2. Poll (1-2 hours) — Community engagement
3. Short video (4-6 hours) — Quick content

## Phase 2: Authority (16 hours) — Next 2 weeks
4. Contrarian article (6-8 hours) — SEO + thought leadership
5. Infographic (6-8 hours) — Shareable + visual

## Phase 3: Depth (34 hours) — Month 2+
6-10. Podcasts, long-form guide, debate episode

## Total investment: 65 hours for 10 pieces
## Estimated reach multiplier: 3-5x vs. single idea
```

---

## Step 5: Adapt for Your Platform

Each mutation includes `platform_recommendations`. Adapt to your priorities:

### If you focus on YouTube:
Priority: Long-form videos, podcast-to-video, case studies
Production order: Video #3 → Podcast #6 → Guide #9

### If you focus on LinkedIn:
Priority: Articles, carousels, thought leadership
Production order: Article #4 → Carousel #5 → Debate #10

### If you focus on Instagram:
Priority: Short videos, carousels, polls, infographics
Production order: Video #3 → Carousel #5 → Poll #6 → Infographic #7

---

## Working Example

**Input Idea:**
```
"Early-stage entrepreneurs often confuse activity with progress"
Target: Solopreneurs just starting out
Niche: Entrepreneurship
```

**Output Sample Mutations:**

| Rank | Format | Angle | Hook | Score | Time | Platform |
|------|--------|-------|------|-------|------|----------|
| 1 | Short Video | Story | "He was busy for 2 years, made $0" | 7.8 | 4h | Instagram |
| 2 | Article | Contrarian | "Productivity is overrated for startups" | 7.6 | 6h | LinkedIn |
| 3 | Checklist | How-to | "Before you work today, ask these 5 questions" | 7.5 | 2h | Email |
| 4 | Podcast | Data | "What 100 failed startups have in common" | 7.0 | 10h | Spotify |

---

## Tips & Best Practices

### ✅ Do:
- Start with a **clear, specific idea** (vague ideas = vague mutations)
- Define your **audience precisely** (this drives relevance scoring)
- Pick **formats you can actually produce** (don't score for video if you can't shoot)
- **Batch similar content** in production (3 videos in one shoot, 5 carousels one design session)
- **Repurpose heavily** (one podcast → video clips → carousel → social posts)

### ❌ Don't:
- Try to produce all 50+ mutations (pick top 10-15 max)
- Copy the same exact content to every platform (use platform adaptation prompt)
- Score mutations without considering your capacity (a 10/10 idea is worthless if you can't make it)
- Ignore the evergreen score (time-sensitive content ages fast, evergreen compounds)

---

## Integration with Production Tools

### Send to n8n
Export the portfolio as JSON → n8n webhook:
```
POST https://n8n.example.com/webhook/content-mutations
{
  "mutations": [...],
  "production_schedule": {...}
}
```

N8n then:
- Routes each mutation to appropriate team member
- Sets deadlines based on production time
- Tracks progress
- Publishes to calendars

### Send to Notion
Export mutations → Create database:
- Mutation title
- Score
- Angle
- Production status
- Due date
- Team member assigned

### Send to Google Sheets
Use CSV export for easy tracking:
```
Rank | Title | Score | Difficulty | Status | Notes
1    | Video | 7.8   | 2          | Planning |
2    | Article | 7.6 | 3          | In progress |
```

---

## Example Output Files

In the `/examples/` folder:

- `financial-decision-making.json` — Full portfolio example (10 mutations)
- Includes scores, platform recommendations, production roadmap
- See the exact output format

---

## Troubleshooting

**Q: Mutations seem generic/repetitive**
A: Your idea might be too vague. Deconstruct more carefully. Angles should be distinct, not variations.

**Q: Scores seem low (all 6-7)**
A: This is actually healthy—it means mutations are realistic. Look for ROI instead of high scores.

**Q: I don't have time for the top-ranked mutations**
A: Filter by production_difficulty. Do the high-ROI ones first (high score + low difficulty).

**Q: Platform recommendations don't match my focus**
A: Mutations scored for "best overall platform fit." You can override—use the manual platform_recommendations field.

**Q: Claude keeps returning incomplete JSON**
A: Add explicit instruction: "Return ONLY valid JSON, no additional text or markdown."

---

## Next: Automate This

Once you've run this manually 2-3 times, you can:

1. **Build an n8n workflow** that chains the prompts
2. **Create a Zapier/Make integration** for quick idea → portfolio
3. **Embed in your CMS** as a "generate content portfolio" button
4. **Set up recurring prompts** (weekly idea generation → automatic portfolio)

See `/workflows/` for n8n template.

---

## Quick Command Reference

```bash
# Deconstruct an idea
claude --prompt prompts/idea-deconstruction.md --input idea.json

# Generate angles
claude --prompt prompts/angle-generation.md --input core-idea.json

# Generate hooks
claude --prompt prompts/hook-generation.md --input angles.json

# Score mutations
claude --prompt prompts/scoring.md --input mutations.json

# Export to CSV
jq -r '.selected_mutations[] | [.rank, .mutation_title, .overall_score, .production_difficulty] | @csv' portfolio.json > production-queue.csv
```

---

## You're Ready

1. Prepare your idea
2. Pick your method (Claude project / CLI / manual)
3. Run the pipeline
4. Review top 10
5. Start production on highest ROI items
6. Repeat weekly

**Expected result:** 10 production-ready pieces from 1 idea, scored for impact + ease.

Questions? See the README.md or example portfolio.
