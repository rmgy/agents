"""
Edge Detection Module for Polymarket Trading

This module identifies trading edges by:
1. Calculating market-implied probabilities from prices
2. Estimating true probabilities using LLM analysis
3. Scoring edge strength and quality
4. Evaluating market efficiency
5. Detecting inefficiency signals
"""

import os
import ast
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from agents.utils.objects import (
    SimpleMarket,
    MarketEdgeAnalysis,
    MarketEfficiencyScore,
    OutcomeEdgeAnalysis,
    EdgeSignal,
    ProbabilityEstimate,
)
from agents.application.prompts import Prompter


class EdgeDetector:
    """
    Identifies trading edges in Polymarket by comparing market prices
    against estimated true probabilities.
    """

    def __init__(self, model: str = "gpt-3.5-turbo-16k") -> None:
        load_dotenv()
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.prompter = Prompter()

    def extract_prices(self, market: SimpleMarket) -> List[float]:
        """Extract outcome prices from market."""
        try:
            prices = ast.literal_eval(market.outcome_prices)
            if isinstance(prices, list):
                return [float(p) for p in prices]
            return []
        except (ValueError, SyntaxError):
            return []

    def extract_outcomes(self, market: SimpleMarket) -> List[str]:
        """Extract outcome names from market."""
        try:
            outcomes = ast.literal_eval(market.outcomes)
            if isinstance(outcomes, list):
                return [str(o) for o in outcomes]
            return []
        except (ValueError, SyntaxError):
            return []

    def calculate_implied_probabilities(self, prices: List[float]) -> List[float]:
        """
        Convert prices to implied probabilities.
        In Polymarket, prices directly represent probabilities.
        """
        if not prices or sum(prices) == 0:
            return []
        # Normalize to ensure sum = 1.0 (accounting for fees/spreads)
        total = sum(prices)
        return [p / total for p in prices]

    def estimate_true_probability(
        self,
        market: SimpleMarket,
        outcome: str,
        outcomes: List[str],
    ) -> ProbabilityEstimate:
        """
        Use LLM to estimate true probability of an outcome.
        """
        prompt = self.prompter.estimate_outcome_probability(
            question=market.question,
            description=market.description,
            outcome=outcome,
            all_outcomes=outcomes,
        )

        messages = [
            SystemMessage(content=self.prompter.probability_estimator()),
            HumanMessage(content=prompt),
        ]

        result = self.llm.invoke(messages)
        return self._parse_probability_estimate(result.content, outcome)

    def _parse_probability_estimate(
        self, response: str, outcome: str
    ) -> ProbabilityEstimate:
        """Parse LLM response into ProbabilityEstimate."""
        try:
            # Try to extract JSON from response
            if "{" in response and "}" in response:
                json_start = response.index("{")
                json_end = response.rindex("}") + 1
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
            else:
                # Fallback: extract probability from text
                import re

                match = re.search(r"(\d+\.?\d*)\s*(?:%|probability)", response.lower())
                if match:
                    prob = float(match.group(1)) / 100
                    data = {
                        "probability": prob,
                        "reasoning": response,
                        "confidence": "medium",
                    }
                else:
                    # Default to neutral estimate
                    data = {
                        "probability": 0.5,
                        "reasoning": response,
                        "confidence": "low",
                    }

            return ProbabilityEstimate(
                outcome=outcome,
                estimated_probability=float(data.get("probability", 0.5)),
                reasoning=str(data.get("reasoning", "")),
                confidence_level=str(data.get("confidence", "medium")),
                key_factors=data.get("key_factors", []),
                base_rate=data.get("base_rate"),
                time_decay_factor=data.get("time_decay_factor"),
            )
        except Exception as e:
            # Fallback estimate
            return ProbabilityEstimate(
                outcome=outcome,
                estimated_probability=0.5,
                reasoning=f"Error parsing estimate: {str(e)}",
                confidence_level="low",
                key_factors=[],
            )

    def score_edge_strength(
        self, true_prob: float, market_prob: float, confidence: float
    ) -> float:
        """
        Score edge strength (0-1) based on probability gap and confidence.

        Higher score = stronger edge.
        Edge must be:
        - At least 3% gap to be meaningful (fee threshold)
        - Discounted by confidence level
        """
        min_edge_gap = 0.03  # 3% minimum to overcome fees
        probability_gap = abs(true_prob - market_prob)

        if probability_gap < min_edge_gap:
            return 0.0

        # Normalize gap: 0.03 = 0.2 score, 0.10 = 1.0 score
        normalized_gap = min(1.0, (probability_gap - min_edge_gap) / 0.07)

        # Apply confidence discount
        edge_strength = normalized_gap * confidence

        return min(1.0, edge_strength)

    def detect_edge_signals(
        self,
        market: SimpleMarket,
        prices: List[float],
        probability_estimates: List[ProbabilityEstimate],
    ) -> List[EdgeSignal]:
        """Detect inefficiency signals in the market."""
        signals = []

        # 1. Information asymmetry: low volume = less informed traders
        if hasattr(market, "volume") and market.volume and market.volume < 10000:
            signals.append(EdgeSignal.INFORMATION_ASYMMETRY)

        # 2. Low liquidity
        if market.spread and market.spread > 0.05:  # >5% spread
            signals.append(EdgeSignal.LOW_LIQUIDITY)

        # 3. Complex wording (harder to understand = pricing errors)
        question = market.question.lower()
        if any(
            keyword in question
            for keyword in [
                "conditional",
                "if and only if",
                "unless",
                "before",
                "after",
            ]
        ):
            signals.append(EdgeSignal.COMPLEX_WORDING)

        # 4. Probability math errors: Look for high confidence estimates
        # with large gaps from market prices
        for est in probability_estimates:
            if est.confidence_level == "high" and est.estimated_probability:
                if est.estimated_probability > 0.8 or est.estimated_probability < 0.2:
                    signals.append(EdgeSignal.PROBABILITY_MATH_ERROR)
                    break

        # 5. Emotional overreaction: Recent price volatility
        if market.spread and market.spread < 0.02:  # Tight spread = consensus
            # But if recently changed, might be overreaction
            signals.append(EdgeSignal.EMOTIONAL_OVERREACTION)

        return list(set(signals))  # Remove duplicates

    def score_market_efficiency(self, market: SimpleMarket) -> MarketEfficiencyScore:
        """Score market efficiency (lower = more opportunity for edge)."""
        # Liquidity: normalized on $0-$100k scale
        liquidity = getattr(market, "liquidity", 0) or 0
        liquidity_score = min(1.0, liquidity / 100000)

        # Volume: normalized on $0-$1M scale
        volume = getattr(market, "volume", 0) or 0
        volume_score = min(1.0, volume / 1000000)

        # Spread: wider spread = less efficient
        spread = market.spread or 0.03
        spread_score = 1.0 - min(1.0, spread / 0.20)  # 20% spread = 0 score

        # Age: older markets are more efficient
        # Assume 6 months = fully efficient
        try:
            created_at = getattr(market, "createdAt", None)
            if created_at:
                market_age_days = (
                    datetime.now() - datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                ).days
                age_score = min(1.0, market_age_days / 180)  # 180 days = full score
            else:
                age_score = 0.5
        except Exception:
            age_score = 0.5

        # Volatility: estimate from spread
        # Wider spread might indicate uncertainty (higher volatility)
        volatility_score = min(1.0, spread / 0.20)

        # Overall efficiency: weighted average
        overall = (
            liquidity_score * 0.25
            + volume_score * 0.25
            + spread_score * 0.30
            + age_score * 0.15
            + (1 - volatility_score) * 0.05  # Lower volatility = more efficient
        )

        return MarketEfficiencyScore(
            liquidity_score=liquidity_score,
            volume_score=volume_score,
            spread_score=spread_score,
            age_score=age_score,
            volatility_score=volatility_score,
            overall_efficiency=overall,
        )

    def score_edge_quality(
        self,
        outcome_analyses: List[OutcomeEdgeAnalysis],
        efficiency_score: MarketEfficiencyScore,
        signals: List[EdgeSignal],
    ) -> float:
        """
        Score overall edge quality (0-1).

        High edge quality when:
        - Outcome has strong edge (large gap)
        - Market is inefficient (low efficiency score)
        - Multiple edge signals detected
        """
        if not outcome_analyses:
            return 0.0

        # Best edge from outcomes
        best_edge = max(oa.edge_strength for oa in outcome_analyses) if outcome_analyses else 0

        # Inefficiency multiplier (inverse of efficiency)
        inefficiency_bonus = 1.0 - efficiency_score.overall_efficiency

        # Signal count bonus (more signals = more confidence in inefficiency)
        signal_bonus = min(0.3, len(signals) * 0.1)

        # Combined score
        quality = best_edge * (1 + inefficiency_bonus * 0.5 + signal_bonus)
        return min(1.0, quality)

    def determine_tradeability(
        self, edge_quality: float, efficiency: float, risk_level: str
    ) -> bool:
        """Determine if edge is strong enough to trade on."""
        min_edge_quality = 0.15  # Need at least 15% edge quality
        max_risk = {"low": 1.0, "medium": 0.7, "high": 0.0}.get(risk_level, 0.5)

        return edge_quality >= min_edge_quality and efficiency < max_risk

    def assess_risk(
        self,
        outcome_analyses: List[OutcomeEdgeAnalysis],
        market: SimpleMarket,
    ) -> Tuple[str, List[str]]:
        """
        Assess risk level and identify potential edge invalidators.

        Returns: (risk_level, [list of invalidating factors])
        """
        invalidators = []
        risk_score = 0.0  # 0 = low risk, 1.0 = high risk

        # Check if market resolves soon (no time for edge to play out)
        try:
            end_date = datetime.fromisoformat(
                market.end.replace("Z", "+00:00") if isinstance(market.end, str) else market.end
            )
            days_to_resolution = (end_date - datetime.now()).days
            if days_to_resolution < 7:
                invalidators.append("Market resolves within 7 days - no time for edge")
                risk_score += 0.3
            elif days_to_resolution < 30:
                risk_score += 0.1
        except Exception:
            pass

        # Check outcome confidence spread (consensus vs split)
        if outcome_analyses:
            confidences = [oa.confidence for oa in outcome_analyses]
            if max(confidences) - min(confidences) > 0.4:
                invalidators.append("Wide confidence gap across outcomes")
                risk_score += 0.2

        # Check for conflicting signals
        strong_edges = [oa for oa in outcome_analyses if oa.edge_strength > 0.3]
        if len(strong_edges) > 2:
            invalidators.append("Multiple strong edges suggests uncertainty")
            risk_score += 0.2

        # Convert risk score to level
        if risk_score >= 0.6:
            risk_level = "high"
        elif risk_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"

        return risk_level, invalidators

    def analyze_market(self, market: SimpleMarket) -> MarketEdgeAnalysis:
        """
        Comprehensive edge analysis for a single market.
        """
        prices = self.extract_prices(market)
        outcomes = self.extract_outcomes(market)

        if not prices or not outcomes or len(prices) != len(outcomes):
            raise ValueError(f"Invalid market data: {market.id}")

        # Calculate implied probabilities
        implied_probs = self.calculate_implied_probabilities(prices)

        # Estimate true probabilities
        probability_estimates = [
            self.estimate_true_probability(market, outcome, outcomes) for outcome in outcomes
        ]

        # Analyze each outcome
        outcome_analyses = []
        for i, (outcome, implied_prob, est) in enumerate(
            zip(outcomes, implied_probs, probability_estimates)
        ):
            true_prob = est.estimated_probability
            prob_gap = true_prob - implied_prob

            edge_strength = self.score_edge_strength(
                true_prob, implied_prob, self._confidence_to_float(est.confidence_level)
            )

            analysis = OutcomeEdgeAnalysis(
                outcome=outcome,
                outcome_index=i,
                market_implied_probability=implied_prob,
                estimated_true_probability=true_prob,
                probability_gap=prob_gap,
                edge_strength=edge_strength,
                reasoning=est.reasoning,
                confidence=self._confidence_to_float(est.confidence_level),
            )
            outcome_analyses.append(analysis)

        # Detect signals
        signals = self.detect_edge_signals(market, prices, probability_estimates)

        # Score efficiency
        efficiency_score = self.score_market_efficiency(market)

        # Score overall edge quality
        edge_quality = self.score_edge_quality(outcome_analyses, efficiency_score, signals)

        # Assess risk
        risk_level, invalidators = self.assess_risk(outcome_analyses, market)

        # Determine tradeability
        is_tradeable = self.determine_tradeability(edge_quality, efficiency_score.overall_efficiency, risk_level)

        # Generate recommendation
        best_edge_analysis = max(outcome_analyses, key=lambda x: x.edge_strength)
        trade_recommendation = self._generate_recommendation(
            best_edge_analysis, is_tradeable, edge_quality, risk_level
        ) if is_tradeable else None

        return MarketEdgeAnalysis(
            market_id=str(market.id),
            market_question=market.question,
            analysis_timestamp=datetime.now().isoformat(),
            outcome_analyses=outcome_analyses,
            best_edge_outcome=best_edge_analysis.outcome,
            strongest_edge_probability_gap=best_edge_analysis.probability_gap,
            efficiency_score=efficiency_score,
            detected_signals=signals,
            edge_quality_score=edge_quality,
            is_tradeable=is_tradeable,
            trade_recommendation=trade_recommendation,
            potential_invalidators=invalidators,
            risk_level=risk_level,
        )

    def _confidence_to_float(self, confidence: str) -> float:
        """Convert confidence string to float."""
        mapping = {"low": 0.5, "medium": 0.75, "high": 0.95}
        return mapping.get(confidence.lower(), 0.5)

    def _generate_recommendation(
        self,
        edge_analysis: OutcomeEdgeAnalysis,
        is_tradeable: bool,
        quality: float,
        risk_level: str,
    ) -> Optional[str]:
        """Generate specific trading recommendation."""
        if not is_tradeable:
            return None

        if edge_analysis.probability_gap > 0:
            side = "BUY"
            prob_desc = f"{edge_analysis.estimated_true_probability:.1%}"
            action = f"{side} {edge_analysis.outcome} (true probability: {prob_desc})"
        else:
            side = "SELL"
            prob_desc = f"{edge_analysis.market_implied_probability:.1%}"
            action = f"{side} {edge_analysis.outcome} (market overpricing)"

        quality_desc = {True: "Strong", False: "Moderate"}.get(quality > 0.3, "Weak")

        return f"{quality_desc} edge detected. {action}. Risk level: {risk_level}"

    def rank_markets_by_edge(
        self, markets: List[SimpleMarket]
    ) -> List[Tuple[SimpleMarket, MarketEdgeAnalysis]]:
        """
        Analyze multiple markets and rank by edge quality.
        """
        analyses = []
        for market in markets:
            try:
                analysis = self.analyze_market(market)
                analyses.append((market, analysis))
            except Exception as e:
                print(f"Error analyzing market {market.id}: {str(e)}")
                continue

        # Sort by edge quality, descending
        ranked = sorted(analyses, key=lambda x: x[1].edge_quality_score, reverse=True)
        return ranked
