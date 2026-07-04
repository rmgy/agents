# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Polymarket Agents is a Python framework for building autonomous AI agents that trade on Polymarket prediction markets. It integrates LLM capabilities (OpenAI), blockchain interactions (Web3), and data retrieval (RAG via ChromaDB) to enable intelligent market analysis and trading decisions.

**Target Python version**: 3.9

## Architecture

### Core Components

The project is organized into four main modules within `/agents/`:

- **`agents/polymarket/`**: Market data and trading interfaces
  - `gamma.py`: GammaMarketClient for fetching market/event metadata from Polymarket Gamma API
  - `polymarket.py`: Main Polymarket class for API interactions and order execution; includes order building and signing utilities

- **`agents/connectors/`**: Data source integrations
  - `chroma.py`: ChromaDB vector database wrapper for semantic search over news and market data
  - `news.py`: NewsAPI integration for real-time news sourcing
  - `search.py`: Web search integration (likely Tavily or similar)

- **`agents/application/`**: Agent logic and execution
  - `executor.py`: Core Agent class implementing trading logic and decision-making
  - `trade.py`: Trader class that orchestrates full trading workflows (the primary entry point)
  - `creator.py`: Agent creation and configuration utilities
  - `prompts.py`: LLM prompt templates for decision-making
  - `cron.py`: Scheduled task management

- **`agents/utils/`**: Shared utilities
  - `objects.py`: Pydantic data models (Trade, SimpleMarket, PolymarketEvent, ClobReward, Tag, etc.)
  - `utils.py`: Helper functions

### Data Models

All data models use Pydantic (v2.x) and are defined in `agents/utils/objects.py`. Key models:
- `Trade`: Represents an executed trade
- `SimpleMarket`: Market metadata and pricing info
- `PolymarketEvent`: Event details with timestamps and tags
- `ClobReward`: CLOB incentive structures

When adding new API response types, define them as Pydantic models here for type safety and validation.

### Trading Workflow

The typical flow is: **Trader → Agent (via Executor) → Market Data APIs → LLM Decision → Order Execution**

1. `Trader.one_best_trade()` (main strategy) orchestrates the flow
2. Retrieves all tradeable events from Polymarket
3. Filters events using RAG (Retrieval-Augmented Generation) to focus on relevant markets
4. Maps filtered events to specific markets
5. Evaluates orderbooks and market conditions
6. Uses LLM to generate trading decisions
7. Executes orders via Polymarket API

## Setup & Environment

### Dependencies

Install from `requirements.txt`:
```bash
pip install -r requirements.txt
```

Key dependencies:
- **LLM & AI**: `langchain`, `langchain-openai`, `langchain-chroma`
- **Market data**: `py_clob_client`, `py_order_utils`, web3
- **Vector DB**: `chromadb`
- **Data sources**: `newsapi-python`, `tavily-python`
- **API/Web**: `fastapi`, `uvicorn`, `httpx`
- **Utilities**: `pydantic`, `click`, `rich`

### Environment Variables

Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

Required:
- `POLYGON_WALLET_PRIVATE_KEY`: Ethereum wallet private key for signing orders
- `OPENAI_API_KEY`: OpenAI API key for LLM calls

Optional (for enhanced data sources):
- `TAVILY_API_KEY`: Tavily web search API
- `NEWSAPI_API_KEY`: NewsAPI for news sourcing

### Virtual Environment

```bash
# Create (Python 3.9 required)
virtualenv --python=python3.9 .venv

# Activate
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### PYTHONPATH

When running outside Docker, set:
```bash
export PYTHONPATH="."
```

## Development Commands

### Testing

Run unit tests:
```bash
pytest                    # All tests
pytest tests/test.py      # Specific test file
pytest tests/ -v          # Verbose output
```

Current test suite is minimal (see `tests/test.py`). Expand with property-based tests for agent logic.

### Code Formatting & Linting

**Pre-commit hooks** use Black (configured in `.pre-commit-config.yaml`):
```bash
# Install hooks once
pre-commit install

# Manually run before committing
pre-commit run --all-files

# Format code manually
black .
```

### CLI Usage

The CLI (`scripts/python/cli.py`) is the primary interface for end users. Run commands as:
```bash
python scripts/python/cli.py <command> [--flag value] [--flag value]
```

Examples:
```bash
# Get all markets (limit 5, sort by volume)
python scripts/python/cli.py get-all-markets --limit 5 --sort-by volume

# CLI discovers subcommands dynamically from the agents module
```

Commands are implemented as decorators in `cli.py` and should follow Click conventions.

### Running the Application

**Local execution** (outside Docker):
```bash
# Requires: PYTHONPATH="." and .env configured

# Main trading workflow
python agents/application/trade.py

# Development server (FastAPI backend)
python scripts/python/server.py

# Interactive CLI
python scripts/python/cli.py
```

**Docker execution**:
```bash
# Build image
./scripts/bash/build-docker.sh

# Run dev container (mounted volume)
./scripts/bash/run-docker-dev.sh

# Run production container
./scripts/bash/run-docker.sh

# Start dev environment (includes installation)
./scripts/bash/start-dev.sh
```

### Debugging Tips

- Use `PYTHONPATH="."` when running Python scripts directly
- Check `.env` is configured with valid keys (common issue)
- Import errors often mean PYTHONPATH isn't set
- ChromaDB creates `local_db_*` directories—these are cleared in `Trader.pre_trade_logic()`

## Code Conventions

### Naming & Structure

- Use snake_case for functions and variables; PascalCase for classes
- Pydantic models in `objects.py`; keep data validation centralized
- API client classes (Polymarket, Gamma) are singletons per convention—initialize once in Trader
- Connector classes handle external integrations; keep them loosely coupled

### Adding New Features

1. **New API endpoints**: Add to Polymarket or Gamma classes; return Pydantic models
2. **New data sources**: Create in `agents/connectors/`; follow the pattern of `chroma.py`
3. **New trading strategies**: Subclass or extend Executor; override `filter_events_with_rag()` or `evaluate_market()`
4. **New CLI commands**: Add function with `@click.command()` decorator in `scripts/python/cli.py`
5. **Custom edge detection**: Subclass `EdgeDetector` and override `estimate_true_probability()` or `detect_edge_signals()`
   - Example: Crypto governance detector, sports betting specialist, etc.
   - See `EDGE_DETECTION_GUIDE.md` for patterns

### LLM Integration Patterns

- Prompts are in `agents/application/prompts.py`
- Use LangChain's `ChatOpenAI` for LLM calls; chain with retrievers for RAG
- Always validate LLM outputs (e.g., JSON parsing) before using in trades
- Consider token limits; summarize long market descriptions

### Error Handling

- Let exceptions propagate for critical failures (e.g., failed trades)
- Log warnings for non-critical issues (e.g., skipped events due to filtering)
- Use try-except for external API calls (Polymarket, OpenAI) with retry logic via Tenacity

## Testing Strategy

The current test suite (`tests/test.py`) is minimal. When adding new features:

- Write unit tests for data validation (Pydantic models)
- Write integration tests for API interactions (mock external services)
- Test trading logic with synthetic market data
- Use `pytest` fixtures for reusable test setup

Example:
```python
import pytest
from agents.utils.objects import SimpleMarket

def test_market_validation():
    market = SimpleMarket(
        id=1, question="Will X happen?", end="2025-01-01",
        description="", active=True, funded=True,
        rewardsMinSize=0.0, rewardsMaxSpread=0.1, spread=0.02,
        outcomes="Yes,No", outcome_prices="0.6,0.4", clob_token_ids=None
    )
    assert market.id == 1
```

## Contributing

- Follow the `CONTRIBUTING.md` guidelines
- Run `pre-commit install` to enforce formatting before commits
- Ensure all tests pass before submitting PRs
- Keep changes modular; avoid coupling unrelated features
- Update `CLAUDE.md` if adding new modules or significant workflows

## Edge Detection Module

The edge detection system identifies trading opportunities by comparing **market-implied probabilities** against **estimated true probabilities**.

### Core Concept

A trading edge exists when: `|True Probability - Market Probability| > Fee Threshold (3%)`

### Key Components

- **EdgeDetector** (`agents/application/edge_detection.py`): Main algorithm
- **MarketEdgeAnalysis**: Comprehensive edge analysis output
  - Probability gaps for each outcome
  - Edge strength scores (0-1)
  - Market efficiency metrics
  - Risk assessment and invalidators
  - Trading recommendations
- **EdgeSignals**: Inefficiency indicators
  - Information asymmetry
  - Emotional overreaction
  - Low liquidity
  - Probability math errors
  - Time-zone lag
  - Complex wording

### How It Works

1. **Extract Prices**: Get market prices and normalize to probabilities
2. **Estimate True Probability**: Use LLM with superforecaster prompts to estimate actual probability
3. **Calculate Gap**: Difference between true and market probability
4. **Score Edge**: Gap × confidence, accounting for fee threshold
5. **Assess Efficiency**: Score market liquidity, volume, spread, age
6. **Detect Signals**: Identify inefficiency patterns
7. **Assess Risk**: Identify factors that could invalidate the edge
8. **Rank**: Sort markets by edge quality

### Usage Example

```python
from agents.application.executor import Executor

executor = Executor()

# Get markets (from event filtering, etc.)
markets = get_my_markets()

# Find best edges
best_edges = executor.find_best_edges_in_markets(
    markets,
    min_quality=0.15  # Only 15%+ quality edges
)

for market, analysis in best_edges:
    if analysis.is_tradeable:
        print(f"Trade: {analysis.trade_recommendation}")
        print(f"Quality: {analysis.edge_quality_score:.1%}")
        print(f"Risk: {analysis.risk_level}")

        # Size position based on edge
        position_size = calculate_kelly(analysis)
```

### Key Thresholds

- **Min Edge Quality**: 15% (edge_quality_score ≥ 0.15)
- **Min Probability Gap**: 3% (covers fees)
- **Max Acceptable Spread**: 20% (5%+ = inefficient)
- **Min Liquidity**: $10k USD

These can be tuned in `edge_detection.py` and integrated trading logic.

### Documentation & Examples

- **EDGE_DETECTION_GUIDE.md**: Comprehensive guide with patterns and pitfalls
- **examples/edge_detection_example.py**: End-to-end usage example
- **CONTRIBUTING.md**: Contributing guidelines

## Key Files Reference

| File | Purpose |
|------|---------|
| `agents/application/trade.py` | Main entry point for trading |
| `agents/application/executor.py` | Core agent decision logic + edge detection |
| `agents/application/edge_detection.py` | **NEW: Edge detection algorithm** |
| `agents/polymarket/polymarket.py` | Polymarket API wrapper |
| `agents/polymarket/gamma.py` | Market metadata client |
| `agents/connectors/chroma.py` | Vector DB for RAG |
| `agents/utils/objects.py` | Pydantic data models (+ edge models) |
| `scripts/python/cli.py` | Command-line interface |
| `examples/edge_detection_example.py` | **NEW: Edge detection example** |
| `agents/application/EDGE_DETECTION_GUIDE.md` | **NEW: Detailed guide** |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |
| `.pre-commit-config.yaml` | Code formatting rules |

## Resources

- **Polymarket API Docs**: https://polymarket.com/docs
- **LangChain Docs**: https://python.langchain.com/
- **Web3.py Docs**: https://web3py.readthedocs.io/
- **Pydantic Docs**: https://docs.pydantic.dev/latest/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **CLOB Client**: https://github.com/Polymarket/py-clob-client
- **Order Utils**: https://github.com/Polymarket/python-order-utils
