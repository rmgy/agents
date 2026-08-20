# Cloudflare AI Integration Guide

This guide covers the integration of Cloudflare Workers AI into the Polymarket Agents framework for image generation, text embeddings, and text classification tasks.

## Overview

Cloudflare Workers AI provides access to various AI models for:
- **Image Generation**: Flux and Stable Diffusion models
- **Text Embeddings**: BGE-base embeddings for semantic search
- **Text Classification**: Sentiment analysis and content classification

## Setup

### 1. Get Cloudflare Credentials

1. Sign up for a [Cloudflare account](https://dash.cloudflare.com/)
2. Navigate to **Cloudflare Dashboard** → **Account Home** → **API Tokens**
3. Create a new API Token with **Workers AI** permissions
4. Get your **Account ID** from the Account Home page

### 2. Configure Environment Variables

Create a `.env` file in the project root with your Cloudflare credentials:

```bash
CLOUDFLARE_API_TOKEN=your_api_token_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
```

You can also copy from the example:

```bash
cp .env.example .env
# Then edit .env with your actual credentials
```

### 3. Verify Installation

The required `requests` library is already included in `requirements.txt`. No additional dependencies are needed.

## Usage

### Python API

#### Image Generation

```python
from agents.connectors.cloudflare import CloudflareAI

# Initialize the connector
cloudflare_ai = CloudflareAI()

# Generate an image
result = cloudflare_ai.generate_image(
    prompt="A serene landscape with mountains and lakes at sunset",
    model="flux-pro"
)

if result.success:
    print(f"Image generated successfully")
    print(f"Result: {result.result}")
else:
    print(f"Error: {result.errors}")
```

#### Save Generated Image to File

```python
# Generate and save directly to file
success = cloudflare_ai.generate_image_file(
    prompt="A futuristic trading dashboard",
    output_path="/path/to/output.png",
    model="flux-pro"
)
```

#### Available Models

```python
# List all available models
models = cloudflare_ai.list_available_models()
# Output:
# {
#     'flux-pro': 'black-forest-labs/flux-1-pro',
#     'flux-realism': 'black-forest-labs/flux-1-realism',
#     'flux-raw': 'black-forest-labs/flux-1-raw',
#     'flux-kontext': 'black-forest-labs/flux-1-kontext-max',
#     'stable-diffusion': 'stabilityai/stable-diffusion-3-large-turbo'
# }
```

#### Text Embeddings

```python
# Generate embeddings for semantic search
embeddings = cloudflare_ai.text_to_embeddings(
    text="Bitcoin prediction market sentiment"
)

if embeddings:
    print(f"Embedding vector: {embeddings[0]['embedding']}")
```

#### Text Classification

```python
# Classify text sentiment
result = cloudflare_ai.text_classification(
    text="Markets surge on positive earnings reports",
    labels=["bullish", "bearish", "neutral"]
)

print(f"Classification: {result}")
```

### Command Line Interface

#### List Available Models

```bash
python scripts/python/cli.py list-cloudflare-models
```

Output:
```
Available Cloudflare AI Models:
  flux-pro: black-forest-labs/flux-1-pro
  flux-realism: black-forest-labs/flux-1-realism
  flux-raw: black-forest-labs/flux-1-raw
  flux-kontext: black-forest-labs/flux-1-kontext-max
  stable-diffusion: stabilityai/stable-diffusion-3-large-turbo
```

#### Generate Image

```bash
# Generate image and display result
python scripts/python/cli.py generate-image "A prediction market visualization with probability curves"

# Generate and save to file
python scripts/python/cli.py generate-image "Market analysis dashboard" \
  --model flux-pro \
  --output-file market_dashboard.png
```

### Example Scripts

A comprehensive example script is provided at `agents/application/cloudflare_image_gen.py`:

```bash
python agents/application/cloudflare_image_gen.py
```

This demonstrates:
- Generating market visualization images
- Using different image generation models
- Generating text embeddings
- Performing sentiment analysis

## API Reference

### CloudflareAI Class

#### Methods

##### `__init__()`
Initialize the CloudflareAI connector with credentials from environment variables.

**Raises:** `ValueError` if `CLOUDFLARE_API_TOKEN` or `CLOUDFLARE_ACCOUNT_ID` are not set.

##### `generate_image(prompt, model="flux-pro", num_steps=None)`
Generate an image using specified model.

**Parameters:**
- `prompt` (str): Text description of the image to generate
- `model` (str): Model alias or full model ID (default: "flux-pro")
- `num_steps` (int, optional): Number of inference steps

**Returns:** `GeneratedImage` object

##### `generate_image_file(prompt, output_path, model="flux-pro", num_steps=None)`
Generate an image and save to file.

**Parameters:**
- `prompt` (str): Text description of the image
- `output_path` (str): Path where to save the PNG image
- `model` (str): Model alias or full model ID
- `num_steps` (int, optional): Number of inference steps

**Returns:** `bool` - True if successful, False otherwise

##### `text_to_embeddings(text)`
Generate embeddings for text.

**Parameters:**
- `text` (str): Text to embed

**Returns:** `list` - Embedding vectors or None if failed

##### `text_classification(text, labels)`
Classify text into provided labels.

**Parameters:**
- `text` (str): Text to classify
- `labels` (list): List of classification labels

**Returns:** `dict` - Classification results or None if failed

##### `list_available_models()`
Get dictionary of available models.

**Returns:** `dict` - Mapping of model aliases to model IDs

## Image Generation Models

### Flux Models (Recommended)

- **flux-pro** (`black-forest-labs/flux-1-pro`)
  - Best quality, highest detail
  - Slowest generation time
  - Best for professional/commercial use

- **flux-realism** (`black-forest-labs/flux-1-realism`)
  - Photorealistic images
  - Good balance of quality and speed
  - Best for realistic market data visualizations

- **flux-raw** (`black-forest-labs/flux-1-raw`)
  - Raw artistic style
  - Faster than pro
  - Good for creative visualizations

- **flux-kontext** (`black-forest-labs/flux-1-kontext-max`)
  - Maximum context understanding
  - Improved prompt following
  - Good for complex, detailed descriptions

### Stable Diffusion

- **stable-diffusion** (`stabilityai/stable-diffusion-3-large-turbo`)
  - Fast, reliable model
  - Good general-purpose image generation
  - Lower latency than Flux models

## Pricing

Cloudflare Workers AI pricing is based on model API calls. Check the [Cloudflare Pricing page](https://developers.cloudflare.com/workers-ai/platform/pricing/) for current rates.

## Limitations

- API calls timeout after 120 seconds
- Image generation may take 10-30 seconds depending on model
- Rate limiting applies based on your Cloudflare plan
- Some models may not be available in all regions

## Error Handling

The connector returns detailed error information:

```python
result = cloudflare_ai.generate_image(prompt)

if not result.success:
    print(f"Errors: {result.errors}")
    print(f"Messages: {result.messages}")
```

Common errors:
- `CLOUDFLARE_API_TOKEN not set`: Missing credentials
- `CLOUDFLARE_ACCOUNT_ID not set`: Missing account ID
- `Request timeout`: Generation took too long
- `Invalid model`: Specified model not available

## Integration with Polymarket Agents

### Use Cases

1. **Market Visualization**: Generate charts and dashboards for market analysis
2. **Event Imagery**: Create visual representations of prediction market events
3. **Analysis Reports**: Generate images to accompany market analysis reports
4. **Social Media**: Create visuals for social media announcements

### Example Integration

```python
from agents.connectors.cloudflare import CloudflareAI
from agents.polymarket.polymarket import Polymarket

polymarket = Polymarket()
cloudflare_ai = CloudflareAI()

# Get market data
markets = polymarket.get_all_markets()

# Generate visualization for top market
top_market = markets[0]
prompt = f"Professional trading chart for {top_market.description}, showing trend analysis"

cloudflare_ai.generate_image_file(
    prompt=prompt,
    output_path=f"market_viz_{top_market.id}.png"
)
```

## Troubleshooting

### "CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID must be set"

1. Verify `.env` file exists in project root
2. Check that environment variables are properly formatted
3. Ensure no extra whitespace in the `.env` file

```bash
# Verify environment variables are set
echo $CLOUDFLARE_API_TOKEN
echo $CLOUDFLARE_ACCOUNT_ID
```

### Image Generation Timeout

- Try using a faster model like `stable-diffusion` or `flux-raw`
- Reduce prompt complexity
- Check your internet connection

### Poor Image Quality

- Try different models to find best fit for your use case
- Refine the prompt with more specific details
- Use model-specific parameters like `num_steps`

## Further Reading

- [Cloudflare Workers AI Documentation](https://developers.cloudflare.com/workers-ai/)
- [Flux Model Documentation](https://blackforestlabs.ai/flux-1-pro/)
- [Stable Diffusion 3 Documentation](https://stability.ai/blog/stable-diffusion-3)
