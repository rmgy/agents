#!/usr/bin/env python
"""
Example: Edge Detection in Polymarket Trading

This script demonstrates how to use the edge detection module to:
1. Identify trading edges across multiple markets
2. Filter by quality and risk
3. Make probability-based trading decisions
4. Size positions according to edge strength

Run with:
    export PYTHONPATH="."
    python examples/edge_detection_example.py
"""

from agents.application.executor import Executor
from agents.polymarket.gamma import GammaMarketClient
from agents.polymarket.polymarket import Polymarket


def main():
    print("\n" + "="*70)
    print("POLYMARKET EDGE DETECTION EXAMPLE")
    print("="*70)

    # Initialize components
    executor = Executor()
    gamma = GammaMarketClient()
    polymarket = Polymarket()

    # =========================================================================
    # STEP 1: Get all tradeable events
    # =========================================================================
    print("\n[STEP 1] Fetching all tradeable events...")
    try:
        events = polymarket.get_all_tradeable_events()
        print(f"✓ Found {len(events)} tradeable events")
    except Exception as e:
        print(f"✗ Error fetching events: {e}")
        print("  (This is expected if wallet/API keys not configured)")
        return

    # =========================================================================
    # STEP 2: Filter events using RAG (focus on relevant domains)
    # =========================================================================
    print("\n[STEP 2] Filtering events using RAG...")
    try:
        filtered_events = executor.filter_events_with_rag(events)
        print(f"✓ Filtered down to {len(filtered_events)} relevant events")
    except Exception as e:
        print(f"Note: RAG filtering skipped ({type(e).__name__})")
        filtered_events = events[:5]  # Use first 5 as demo

    # =========================================================================
    # STEP 3: Map events to markets
    # =========================================================================
    print("\n[STEP 3] Mapping events to markets...")
    try:
        markets = executor.map_filtered_events_to_markets(filtered_events)
        print(f"✓ Found {len(markets)} markets from filtered events")
    except Exception as e:
        print(f"Note: Market mapping skipped ({type(e).__name__})")
        return

    if not markets:
        print("✗ No markets found. Exiting.")
        return

    # =========================================================================
    # STEP 4: Detect edges in all markets
    # =========================================================================
    print("\n" + "="*70)
    print("[STEP 4] EDGE DETECTION ANALYSIS")
    print("="*70)

    try:
        # Find all edges, sorted by quality
        best_edges = executor.find_best_edges_in_markets(
            markets,
            min_quality=0.10  # 10% minimum quality
        )

        if not best_edges:
            print("\n✗ No tradeable edges found in these markets")
            print("  (This is common - edges are rare!)")
            return

        # =====================================================================
        # STEP 5: Analyze top edge
        # =====================================================================
        print("\n" + "="*70)
        print("[STEP 5] DETAILED ANALYSIS OF TOP EDGE")
        print("="*70)

        top_market, top_analysis = best_edges[0]

        print(f"\nMarket: {top_market.question}")
        print(f"ID: {top_market.id}")
        print(f"\nEdge Quality Score: {top_analysis.edge_quality_score:.1%}")
        print(f"Risk Level: {top_analysis.risk_level.upper()}")
        print(f"Is Tradeable: {top_analysis.is_tradeable}")

        # Show outcome-by-outcome analysis
        print("\nOutcome Analysis:")
        print("-" * 70)
        for outcome in top_analysis.outcome_analyses:
            print(f"\n  {outcome.outcome}")
            print(f"    Market Price (Implied Prob): {outcome.market_implied_probability:.1%}")
            print(f"    Estimated True Probability: {outcome.estimated_true_probability:.1%}")
            print(f"    Gap: {outcome.probability_gap:+.1%}")
            print(f"    Edge Strength: {outcome.edge_strength:.1%}")
            print(f"    Confidence: {outcome.confidence:.1%}")

        # Market efficiency
        print("\nMarket Efficiency Metrics:")
        print("-" * 70)
        eff = top_analysis.efficiency_score
        print(f"  Liquidity Score: {eff.liquidity_score:.1%}")
        print(f"  Volume Score: {eff.volume_score:.1%}")
        print(f"  Spread Score: {eff.spread_score:.1%}")
        print(f"  Overall Efficiency: {eff.overall_efficiency:.1%}")

        # Edge signals
        if top_analysis.detected_signals:
            print("\nEdge Signals Detected:")
            print("-" * 70)
            for signal in top_analysis.detected_signals:
                print(f"  • {signal.value.replace('_', ' ').title()}")

        # Risk assessment
        print("\nRisk Assessment:")
        print("-" * 70)
        if top_analysis.potential_invalidators:
            for invalidator in top_analysis.potential_invalidators:
                print(f"  ⚠ {invalidator}")
        else:
            print("  ✓ No major invalidators identified")

        # Trading recommendation
        if top_analysis.trade_recommendation:
            print("\nTrading Recommendation:")
            print("-" * 70)
            print(f"  {top_analysis.trade_recommendation}")

        # =====================================================================
        # STEP 6: Position Sizing Example
        # =====================================================================
        print("\n" + "="*70)
        print("[STEP 6] POSITION SIZING")
        print("="*70)

        usdc_balance = polymarket.get_usdc_balance()
        print(f"\nWallet USDC Balance: ${usdc_balance:,.2f}")

        # Simple position sizing based on edge quality and risk
        def calculate_position_size(edge_quality, risk_level, balance, max_pct_per_trade=0.05):
            """
            Size position based on edge quality and risk level.

            Formula:
                size = balance * edge_quality * risk_multiplier * max_pct
            """
            risk_multipliers = {
                "low": 1.0,
                "medium": 0.6,
                "high": 0.3,
            }

            multiplier = risk_multipliers.get(risk_level, 0.5)
            position_size = balance * edge_quality * multiplier * max_pct_per_trade

            return position_size

        position_size = calculate_position_size(
            top_analysis.edge_quality_score,
            top_analysis.risk_level,
            usdc_balance
        )

        print(f"Recommended Position Size: ${position_size:,.2f}")
        print(f"Percentage of Balance: {position_size/usdc_balance:.1%}")

        # =====================================================================
        # STEP 7: Summary of All Edges
        # =====================================================================
        print("\n" + "="*70)
        print("[STEP 7] SUMMARY OF ALL EDGES")
        print("="*70)

        print(f"\nTop 5 Edges by Quality:\n")
        for i, (market, analysis) in enumerate(best_edges[:5], 1):
            status = "✓ TRADE" if analysis.is_tradeable else "✗ SKIP"
            print(
                f"{i}. {market.question[:50]}..."
                f"\n   Quality: {analysis.edge_quality_score:.1%} | "
                f"Risk: {analysis.risk_level.upper()} | "
                f"{status}"
            )

        # =====================================================================
        # STEP 8: Statistics
        # =====================================================================
        print("\n" + "="*70)
        print("[STEP 8] STATISTICS")
        print("="*70)

        tradeable = sum(1 for _, a in best_edges if a.is_tradeable)
        avg_quality = sum(a.edge_quality_score for _, a in best_edges) / len(best_edges)
        low_risk = sum(1 for _, a in best_edges if a.risk_level == "low")

        print(f"\nTotal Edges Found: {len(best_edges)}")
        print(f"Tradeable Edges: {tradeable}")
        print(f"Low-Risk Edges: {low_risk}")
        print(f"Average Quality: {avg_quality:.1%}")

        print("\n" + "="*70)
        print("Edge detection complete!")
        print("="*70 + "\n")

    except Exception as e:
        print(f"\n✗ Error during edge detection: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
