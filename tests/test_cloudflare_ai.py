"""
Unit tests for Cloudflare AI connector.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from agents.connectors.cloudflare import CloudflareAI
from agents.utils.objects import GeneratedImage


class TestCloudflareAIInit:
    """Test CloudflareAI initialization."""

    def test_init_with_valid_credentials(self):
        """Test initialization with valid credentials."""
        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            assert ai.api_token == "test_token"
            assert ai.account_id == "test_account"

    def test_init_missing_api_token(self):
        """Test initialization fails without API token."""
        with patch.dict(os.environ, {"CLOUDFLARE_ACCOUNT_ID": "test_account"}, clear=True):
            with pytest.raises(ValueError, match="CLOUDFLARE_API_TOKEN"):
                CloudflareAI()

    def test_init_missing_account_id(self):
        """Test initialization fails without account ID."""
        with patch.dict(os.environ, {"CLOUDFLARE_API_TOKEN": "test_token"}, clear=True):
            with pytest.raises(ValueError, match="CLOUDFLARE_ACCOUNT_ID"):
                CloudflareAI()

    def test_init_headers_format(self):
        """Test that headers are properly formatted."""
        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            assert ai.headers["Authorization"] == "Bearer test_token"
            assert ai.headers["Content-Type"] == "application/json"


class TestImageGeneration:
    """Test image generation methods."""

    @patch("agents.connectors.cloudflare.requests.post")
    def test_generate_image_success(self, mock_post):
        """Test successful image generation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": {"image": "base64_encoded_image"},
            "errors": None,
            "messages": None,
        }
        mock_post.return_value = mock_response

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            result = ai.generate_image("Test prompt", model="flux-pro")

            assert isinstance(result, GeneratedImage)
            assert result.success is True
            assert result.model == "black-forest-labs/flux-1-pro"
            assert result.prompt == "Test prompt"
            assert result.result == {"image": "base64_encoded_image"}

    @patch("agents.connectors.cloudflare.requests.post")
    def test_generate_image_with_custom_steps(self, mock_post):
        """Test image generation with custom num_steps."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            ai.generate_image("Test prompt", num_steps=50)

            # Verify the payload includes num_steps
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            assert payload["input"]["num_steps"] == 50

    @patch("agents.connectors.cloudflare.requests.post")
    def test_generate_image_failure(self, mock_post):
        """Test handling of image generation failure."""
        mock_post.side_effect = Exception("API Error")

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            result = ai.generate_image("Test prompt")

            assert result.success is False
            assert "API Error" in result.errors[0]

    @patch("agents.connectors.cloudflare.CloudflareAI.generate_image")
    @patch("builtins.open", create=True)
    def test_generate_image_file_success(self, mock_open, mock_gen_image):
        """Test saving generated image to file."""
        import base64

        # Create dummy image data
        dummy_image = b"fake_image_data"
        encoded_image = base64.b64encode(dummy_image).decode()

        mock_result = GeneratedImage(
            success=True,
            result={"image": encoded_image},
            model="flux-pro",
            prompt="Test",
        )
        mock_gen_image.return_value = mock_result

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            success = ai.generate_image_file("Test prompt", "/tmp/test.png")

            assert success is True
            mock_open.assert_called_once_with("/tmp/test.png", "wb")

    @patch("agents.connectors.cloudflare.CloudflareAI.generate_image")
    def test_generate_image_file_no_image_data(self, mock_gen_image):
        """Test handling when result has no image data."""
        mock_result = GeneratedImage(
            success=True,
            result={},  # No image data
            model="flux-pro",
            prompt="Test",
        )
        mock_gen_image.return_value = mock_result

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            success = ai.generate_image_file("Test prompt", "/tmp/test.png")

            assert success is False

    @patch("agents.connectors.cloudflare.CloudflareAI.generate_image")
    def test_generate_image_file_generation_failed(self, mock_gen_image):
        """Test handling when image generation fails."""
        mock_result = GeneratedImage(
            success=False,
            errors=["Generation failed"],
            model="flux-pro",
            prompt="Test",
        )
        mock_gen_image.return_value = mock_result

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            success = ai.generate_image_file("Test prompt", "/tmp/test.png")

            assert success is False


class TestModelResolution:
    """Test model name resolution."""

    def test_model_alias_resolution(self):
        """Test that model aliases resolve correctly."""
        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()

            assert (
                ai.models["flux-pro"]
                == "black-forest-labs/flux-1-pro"
            )
            assert (
                ai.models["stable-diffusion"]
                == "stabilityai/stable-diffusion-3-large-turbo"
            )

    def test_list_available_models(self):
        """Test listing available models."""
        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            models = ai.list_available_models()

            assert isinstance(models, dict)
            assert len(models) > 0
            assert "flux-pro" in models
            assert "stable-diffusion" in models


class TestTextOperations:
    """Test text embedding and classification."""

    @patch("agents.connectors.cloudflare.requests.post")
    def test_text_to_embeddings_success(self, mock_post):
        """Test successful text embedding generation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": {"data": [[0.1, 0.2, 0.3]]},
        }
        mock_post.return_value = mock_response

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            result = ai.text_to_embeddings("Test text")

            assert result == [[0.1, 0.2, 0.3]]

    @patch("agents.connectors.cloudflare.requests.post")
    def test_text_to_embeddings_failure(self, mock_post):
        """Test handling of embedding generation failure."""
        mock_post.side_effect = Exception("API Error")

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            result = ai.text_to_embeddings("Test text")

            assert result is None

    @patch("agents.connectors.cloudflare.requests.post")
    def test_text_classification_success(self, mock_post):
        """Test successful text classification."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": {"labels": ["positive", "negative"]},
        }
        mock_post.return_value = mock_response

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            result = ai.text_classification(
                "Test text", ["positive", "negative"]
            )

            assert result == {"labels": ["positive", "negative"]}

    @patch("agents.connectors.cloudflare.requests.post")
    def test_text_classification_failure(self, mock_post):
        """Test handling of text classification failure."""
        mock_post.side_effect = Exception("API Error")

        with patch.dict(
            os.environ,
            {
                "CLOUDFLARE_API_TOKEN": "test_token",
                "CLOUDFLARE_ACCOUNT_ID": "test_account",
            },
        ):
            ai = CloudflareAI()
            result = ai.text_classification("Test text", ["label1"])

            assert result is None
