"""
Example script demonstrating Cloudflare AI image generation.

Usage:
    python agents/application/cloudflare_image_gen.py
"""

import os
from agents.connectors.cloudflare import CloudflareAI


def generate_market_visualization():
    """
    Example: Generate a market analysis visualization for Polymarket trading.
    """
    try:
        cloudflare_ai = CloudflareAI()

        # Example prompts for market visualization
        prompts = [
            "A professional trading dashboard showing market trends and candlestick charts, dark theme with blue and green accents",
            "A prediction market visualization with probability distribution curves and betting odds displayed on a modern interface",
            "A cinematic dark fantasy scene with a lone warrior in bloodstained samurai armor standing before a pagoda engulfed in flames",
        ]

        for i, prompt in enumerate(prompts):
            print(f"\n--- Generating image {i+1} ---")
            print(f"Prompt: {prompt}")

            # Generate image and save it
            output_file = f"/tmp/generated_image_{i+1}.png"
            success = cloudflare_ai.generate_image_file(
                prompt=prompt,
                output_path=output_file,
                model="flux-pro",
            )

            if success:
                print(f"Successfully generated and saved to {output_file}")
            else:
                print(f"Failed to generate image {i+1}")

    except ValueError as e:
        print(f"Setup error: {e}")
        print("\nPlease ensure the following environment variables are set:")
        print("  CLOUDFLARE_API_TOKEN")
        print("  CLOUDFLARE_ACCOUNT_ID")


def demonstrate_different_models():
    """
    Example: Show how to use different image generation models.
    """
    try:
        cloudflare_ai = CloudflareAI()

        # Show available models
        models = cloudflare_ai.list_available_models()
        print("Available Models:")
        for alias, model_id in models.items():
            print(f"  {alias}: {model_id}")

        prompt = "A futuristic trading arena with holographic market data floating in the air"

        # Try different models
        for model_alias in ["flux-pro", "flux-realism"]:
            print(f"\n--- Generating with {model_alias} ---")
            result = cloudflare_ai.generate_image(
                prompt=prompt,
                model=model_alias,
            )

            if result.success:
                print(f"Successfully generated image with {model_alias}")
            else:
                print(f"Failed with {model_alias}: {result.errors}")

    except ValueError as e:
        print(f"Setup error: {e}")


def generate_embeddings_example():
    """
    Example: Generate text embeddings using Cloudflare AI.
    Useful for semantic search and similarity matching in market analysis.
    """
    try:
        cloudflare_ai = CloudflareAI()

        texts = [
            "Bitcoin will reach $50,000 by end of 2024",
            "Will Ethereum merge happen this quarter?",
            "Market volatility is increasing",
        ]

        print("Generating text embeddings...\n")
        for text in texts:
            embeddings = cloudflare_ai.text_to_embeddings(text)
            if embeddings:
                embedding_vector = embeddings[0]["embedding"]
                print(f"Text: {text}")
                print(f"Embedding dimension: {len(embedding_vector)}")
                print(f"First 5 values: {embedding_vector[:5]}\n")
            else:
                print(f"Failed to generate embedding for: {text}\n")

    except ValueError as e:
        print(f"Setup error: {e}")


def sentiment_analysis_example():
    """
    Example: Analyze sentiment of market news using Cloudflare AI.
    """
    try:
        cloudflare_ai = CloudflareAI()

        texts = [
            "Markets surge on positive economic data and strong earnings",
            "Investors panic as recession fears mount",
            "Trading remains subdued with mixed signals",
        ]

        labels = ["bullish", "bearish", "neutral"]

        print("Analyzing market sentiment...\n")
        for text in texts:
            result = cloudflare_ai.text_classification(text, labels)
            if result:
                print(f"Text: {text}")
                print(f"Classification: {result}")
                print()
            else:
                print(f"Failed to classify: {text}\n")

    except ValueError as e:
        print(f"Setup error: {e}")


if __name__ == "__main__":
    print("=== Cloudflare AI Image Generation Examples ===\n")

    print("1. Generating market visualizations...")
    generate_market_visualization()

    print("\n\n2. Demonstrating different models...")
    demonstrate_different_models()

    print("\n\n3. Generating text embeddings...")
    generate_embeddings_example()

    print("\n\n4. Sentiment analysis...")
    sentiment_analysis_example()
