# Edge Detection Module Guide

## Overview

The Edge Detection module identifies trading opportunities in Polymarket by comparing **market-implied probabilities** against **estimated true probabilities** using LLM-powered forecasting.

### The Core Concept

A trading edge exists when:
```
True Probability ≠ Market Probability + (Threshold to overcome fees)
```

**Example:**
- Market price implies: 45% (betting odds suggest Trump has 45% chance)
- True probability (by your analysis): 65% (you estimate 65% based on polling, history, etc.)
- Gap: 20%
- Action: BUY at 0.45, expecting it to move toward 0.65

## Key Components

### 1. MarketEdgeAnalysis (Main Output)

The complete edge analysis for a market:

```python
from agents.application.edge_detection import EdgeDetector
from agents.utils.objects import MarketEdgeAnalysis

# Returns:
analysis = MarketEdgeAnalysis(
    market_id="12345",
    market_question="Will Trump win 2024?",
    
    # Individual outcome analysis
    outcome_analyses=[
        OutcomeEdgeAnalysis(
            outcome="Yes",
            market_implied_probability=0.45,
            estimated_true_probability=0.65,
            probability_gap=0.20,
            edge_strength=0.75,  # 0-1, normalized edge quality
            confidence=0.95,
        ),
        # ... other outcomes
    ],
    
    best_edge_outcome="Yes",
    strongest_edge_probability_gap=0.20,
    
    # Efficiency metrics
    efficiency_score=MarketEfficiencyScore(
        liquidity_score=0.8,  # 0-1
        volume_score=0.7,
        spread_score=0.6,
        overall_efficiency=0.75,
    ),
    
    # Edge signals detected
    detected_signals=[EdgeSignal.INFORMATION_ASYMMETRY, ...],
    
    # Overall metrics
    edge_quality_score=0.65,  # 0-1, composite score
    is_tradeable=True,
    trade_recommendation="Strong edge detected. BUY Yes (true probability: 65.0%). Risk level: low",
    
    # Risk assessment
    potential_invalidators=["New polling data", "Regulatory changes"],
    risk_level="low",
)
```

### 2. EdgeSignals

Signals that indicate market inefficiency:

- **INFORMATION_ASYMMETRY**: Low volume markets where you might know more
- **EMOTIONAL_OVERREACTION**: Recent price spikes suggesting panic/euphoria
- **LOW_LIQUIDITY**: Tight spreads indicate consensus but hard to exit
- **PROBABILITY_MATH_ERROR**: Traders misunderstanding compound probabilities
- **TIME_ZONE_LAG**: Overnight/weekend markets reacting slower
- **COMPLEX_WORDING**: Hard-to-understand terms create mispricing
- **SPECIALIST_DOMAIN**: Niche markets where deep knowledge matters

### 3. Risk Levels

- **low**: Clear edge, clear resolution path, strong data
- **medium**: Good edge but some uncertainty
- **high**: Weak edge or high invalidation risk

## Usage Examples

### Example 1: Analyze Single Market

```python
from agents.application.executor import Executor
from agents.polymarket.gamma import GammaMarketClient

executor = Executor()
gamma = GammaMarketClient()

# Get a market
market = gamma.get_market("12345")

# Analyze for edges
analysis = executor.detect_edge_in_market(market)

if analysis.is_tradeable:
    print(f"Edge: {analysis.trade_recommendation}")
    print(f"Quality: {analysis.edge_quality_score:.1%}")
    print(f"Risk: {analysis.risk_level}")
    
    # Details on best outcome
    best = analysis.outcome_analyses[0]
    print(f"True probability: {best.estimated_true_probability:.1%}")
    print(f"Market probability: {best.market_implied_probability:.1%}")
    print(f"Gap: {best.probability_gap:.1%}")
```

### Example 2: Find Best Edges Across Markets

```python
executor = Executor()

# Get filtered markets (from your event filtering)
filtered_events = executor.filter_events_with_rag(all_events)
markets = executor.map_filtered_events_to_markets(filtered_events)

# Find best edges
best_edges = executor.find_best_edges_in_markets(
    markets,
    min_quality=0.15  # Only show edges with 15%+ quality
)

for market, analysis in best_edges:
    print(f"{market.question}")
    print(f"  Quality: {analysis.edge_quality_score:.1%}")
    print(f"  Recommendation: {analysis.trade_recommendation}")
```

### Example 3: Integrate Into Trading Workflow

```python
from agents.application.trade import Trader

class SmartTrader(Trader):
    def find_edge_based_trade(self):
        """Find trade with strongest edge instead of arbitrary selection."""
        events = self.polymarket.get_all_tradeable_events()
        filtered_events = self.agent.filter_events_with_rag(events)
        markets = self.agent.map_filtered_events_to_markets(filtered_events)
        
        # Find best edges
        best_edges = self.agent.find_best_edges_in_markets(markets, min_quality=0.20)
        
        if not best_edges:
            print("No tradeable edges found")
            return
        
        market, analysis = best_edges[0]  # Best edge
        
        # Only trade if low/medium risk
        if analysis.risk_level == "high":
            print(f"Skipping {market.question} - too risky")
            return
        
        # Execute trade based on edge
        print(f"Trading: {analysis.trade_recommendation}")
        # TODO: Execute trade via API
```

### Example 4: Risk-Adjusted Position Sizing

```python
# Kelly Criterion for position sizing
def calculate_kelly_position(analysis):
    """
    Kelly Criterion: f = (bp - q) / b
    where:
    - b = decimal odds - 1 (0.45 -> 0.45 - 1 = -0.55 loss for losing bet)
    - p = true probability
    - q = 1 - p
    """
    
    best = analysis.outcome_analyses[0]
    
    if best.probability_gap <= 0:
        return 0  # No edge
    
    # Simplified: use gap as edge, discount by risk
    base_kelly = best.probability_gap * 0.5  # 50% of Kelly for safety
    
    risk_discount = {
        "low": 1.0,
        "medium": 0.7,
        "high": 0.3,
    }.get(analysis.risk_level, 0.5)
    
    position_size = base_kelly * risk_discount
    return min(0.05, position_size)  # Cap at 5% per trade

# Usage
analysis = executor.detect_edge_in_market(market)
position_size = calculate_kelly_position(analysis)
```

## How It Works Internally

### 1. Price Extraction & Normalization

Market prices are extracted and normalized to probabilities:
```python
prices = [0.45, 0.55]  # Raw prices
implied_probs = [0.45/1.0, 0.55/1.0] = [0.45, 0.55]  # Normalized
```

### 2. LLM Probability Estimation

For each outcome, the LLM estimates true probability using:
- Base rates (historical frequency)
- Reference classes (similar past events)
- Quantitative factors (data/metrics)
- Qualitative factors (narrative)
- Time decay (how probability changes with time)

The LLM returns:
```json
{
  "probability": 0.65,
  "reasoning": "Polling averages show 63-67% range...",
  "confidence": "high",
  "key_factors": ["Recent polling surge", "Enthusiasm gap"],
  "base_rate": 0.52
}
```

### 3. Edge Strength Scoring

Gap-based scoring:
```
edge_strength = max(0, (gap - 0.03)) / 0.07) * confidence
  where:
    - 3% minimum gap (fee threshold)
    - 10% gap = max score
    - Discounted by confidence
```

### 4. Market Efficiency Scoring

Composite score of:
- **Liquidity**: How much USDC trading volume
- **Volume**: Total market activity
- **Spread**: Wider = less efficient
- **Age**: Older markets = more efficient
- **Volatility**: Higher = potential mispricing

Lower efficiency = more opportunity for edge.

### 5. Signal Detection

Checks for:
- Low volume (info asymmetry opportunity)
- Wide spreads (inefficiency)
- Complex wording (misunderstanding)
- Recent volatility (overreaction)
- etc.

### 6. Risk Assessment

Identifies factors that could invalidate the edge:
- Market resolves too soon (no time for correction)
- Wide confidence disagreement
- Multiple conflicting edges
- External events pending (regulation, etc.)

### 7. Tradeability Decision

Trade only if:
- Edge quality ≥ 15%
- Risk level ≤ acceptable threshold

## Common Patterns

### Pattern 1: Information Speed

**Situation**: Niche crypto governance vote scheduled for 2pm US time, market hasn't reacted yet (11am).

**Edge Signals**:
- `TIME_ZONE_LAG`
- `LOW_LIQUIDITY`
- `INFORMATION_ASYMMETRY`

**Action**: Research the vote quickly, get true probability, trade before market reacts.

### Pattern 2: Narrative Divergence

**Situation**: Market thinks 35% based on headlines; deep research suggests 60%.

**Why it happens**:
- Most traders follow headlines
- Detailed analysis requires time
- Complex events are hard to model

**Action**: Take 60% side at 0.35, hold until market catches up.

### Pattern 3: Low-Liquidity Inefficiency

**Situation**: Small niche market, 5% spread, little volume.

**Edge**: More mispricing possible, but harder to exit.

**Risk**: Can you actually sell if you need to exit?

**Mitigation**: Only take if high conviction + long time to resolution.

## Key Thresholds

These can be tuned per your risk tolerance:

```python
MIN_EDGE_QUALITY = 0.15        # 15% minimum quality to trade
MIN_EDGE_GAP = 0.03            # 3% minimum gap (fees)
MIN_CONFIDENCE = 0.5           # Discount low-confidence estimates
MAX_SPREAD = 0.20              # 20%+ spread = very inefficient
MIN_LIQUIDITY = 10000          # $10k minimum liquidity
MAX_DAYS_TO_RESOLUTION = 180   # Trade only if decent runway
```

Adjust based on:
- Your trading capital (smaller positions = higher spread tolerance)
- Time availability (faster markets = need faster analysis)
- Risk tolerance (low risk = need higher edge quality)

## Common Pitfalls

### 1. Overconfident Estimates

**Problem**: LLM assigns 90% confidence to an estimate.

**Reality**: Most events have irreducible uncertainty.

**Fix**: Discount high-confidence estimates; demand strong evidence.

### 2. Gap vs. Execution Risk

**Problem**: You found a 20% gap! But the spread is 15%, so net edge is only 5%.

**Reality**: Fees, slippage, and execution costs eat into edge.

**Fix**: Account for transaction costs in edge calculation.

### 3. Time Decay

**Problem**: You estimate 70% true probability, but market resolves in 3 days and you think 50% of moves happen in last week.

**Reality**: Time to event affects how fast edge plays out.

**Fix**: Consider time horizon in position sizing.

### 4. Correlated Outcomes

**Problem**: You identify edge in "Yes", but overlook that "No" outcome has inverse edge.

**Reality**: Markets must sum to 100%; edges can be relative.

**Fix**: Analyze full outcome set, not just favorites.

## Monitoring & Adjustment

### Track Edge Performance

```python
# Log each trade
trades = [
    {
        "market_id": "12345",
        "edge_quality_at_entry": 0.65,
        "risk_level": "low",
        "true_prob_estimate": 0.70,
        "market_prob": 0.45,
        "realized_prob": 0.52,  # How it actually resolved
        "pnl": 500,
    }
]

# Analyze patterns
avg_edge_quality = sum(t['edge_quality_at_entry'] for t in trades) / len(trades)
win_rate = sum(1 for t in trades if t['pnl'] > 0) / len(trades)
```

### Calibrate Confidence

After ~50 trades:
- Are high-confidence estimates actually accurate?
- Do low-efficiency markets move as expected?
- What edge signals correlate with wins?

Adjust accordingly.

## Advanced: Building a Domain-Specific Detector

```python
class CryptoEdgeDetector(EdgeDetector):
    """Specialized detector for crypto governance events."""
    
    def estimate_true_probability(self, market, outcome, outcomes):
        # Override: Use specialized crypto knowledge
        prompt = self.prompter.crypto_governance_forecast(
            question=market.question,
            description=market.description,
            outcome=outcome,
        )
        # ... custom logic
```

## See Also

- CLAUDE.md: High-level architecture
- Prompts.py: LLM instructions for probability estimation
- Objects.py: Data model definitions
- Executor.py: Agent orchestration
