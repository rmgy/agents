import os
import requests
import base64
from typing import Optional
from agents.utils.objects import GeneratedImage


class CloudflareAI:
    """
    Connector for Cloudflare Workers AI API.
    Supports various AI models including image generation, text processing, and more.
    """

    def __init__(self) -> None:
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")

        if not self.api_token or not self.account_id:
            raise ValueError(
                "CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID must be set in environment variables"
            )

        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        # Supported models
        self.models = {
            "flux-pro": "black-forest-labs/flux-1-pro",
            "flux-realism": "black-forest-labs/flux-1-realism",
            "flux-raw": "black-forest-labs/flux-1-raw",
            "flux-kontext": "black-forest-labs/flux-1-kontext-max",
            "stable-diffusion": "stabilityai/stable-diffusion-3-large-turbo",
        }

    def generate_image(
        self,
        prompt: str,
        model: str = "flux-pro",
        num_steps: Optional[int] = None,
    ) -> GeneratedImage:
        """
        Generate an image using Cloudflare Workers AI image generation models.

        Args:
            prompt: The text prompt describing the image to generate
            model: The model to use (default: flux-pro)
                Options: flux-pro, flux-realism, flux-raw, flux-kontext, stable-diffusion
            num_steps: Number of inference steps (optional, model-dependent)

        Returns:
            GeneratedImage object containing the result or errors
        """
        # Resolve model name
        model_id = self.models.get(model, model)

        payload = {
            "model": model_id,
            "input": {
                "prompt": prompt,
            },
        }

        if num_steps is not None:
            payload["input"]["num_steps"] = num_steps

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=120,
            )
            response.raise_for_status()

            data = response.json()

            return GeneratedImage(
                success=data.get("success", False),
                result=data.get("result"),
                errors=data.get("errors"),
                messages=data.get("messages"),
                model=model_id,
                prompt=prompt,
            )

        except requests.exceptions.RequestException as e:
            return GeneratedImage(
                success=False,
                errors=[str(e)],
                model=model_id,
                prompt=prompt,
            )

    def generate_image_file(
        self,
        prompt: str,
        output_path: str,
        model: str = "flux-pro",
        num_steps: Optional[int] = None,
    ) -> bool:
        """
        Generate an image and save it to a file.

        Args:
            prompt: The text prompt describing the image to generate
            output_path: Path where to save the generated image
            model: The model to use (default: flux-pro)
            num_steps: Number of inference steps (optional)

        Returns:
            True if successful, False otherwise
        """
        result = self.generate_image(prompt, model, num_steps)

        if not result.success or not result.result:
            print(f"Image generation failed: {result.errors}")
            return False

        try:
            image_data = result.result.get("image")
            if not image_data:
                print("No image data in response")
                return False

            # Image data should be base64 encoded
            image_bytes = base64.b64decode(image_data)

            with open(output_path, "wb") as f:
                f.write(image_bytes)

            print(f"Image saved to {output_path}")
            return True

        except Exception as e:
            print(f"Failed to save image: {str(e)}")
            return False

    def text_to_embeddings(self, text: str) -> Optional[list]:
        """
        Generate embeddings for text using Cloudflare Workers AI.

        Args:
            text: The text to generate embeddings for

        Returns:
            Embedding vector or None if failed
        """
        payload = {
            "model": "@cf/baai/bge-base-en-v1.5",
            "text": text,
        }

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return data.get("result", {}).get("data")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Embeddings generation failed: {str(e)}")
            return None

    def text_classification(self, text: str, labels: list) -> Optional[dict]:
        """
        Classify text using Cloudflare Workers AI.

        Args:
            text: The text to classify
            labels: List of labels to classify into

        Returns:
            Classification results or None if failed
        """
        payload = {
            "model": "@cf/huggingface/distilbert-sst-2-int8",
            "text": text,
            "labels": labels,
        }

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return data.get("result")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Text classification failed: {str(e)}")
            return None

    def list_available_models(self) -> dict:
        """
        Get dictionary of available models.

        Returns:
            Dictionary mapping model aliases to model IDs
        """
        return self.models.copy()
