"""Ironhack M1.05 — AI product listing generator.

Turn product images and basic metadata into e-commerce listings with OpenAI Vision.

Install (in your existing Ironhack Python environment):
    pip install openai python-dotenv datasets pillow

Commands:
    python product_listing_generator.py --check-existing   # No API call
    python product_listing_generator.py --dry-run          # Prepare images, no API call
    python product_listing_generator.py --test-errors      # Test error handling locally
    python product_listing_generator.py                    # Generate three new listings

Keep your OPENAI_API_KEY in a local .env file. Never commit that file to Git.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "product_images"
DEFAULT_OUTPUT = PROJECT_DIR / "product_listings.json"
DATASET_NAME = "ashraq/fashion-product-images-small"
DEFAULT_MODEL = "gpt-4o-mini"  # Vision-capable model used in the lab notebook


def create_client():
    """Read the API key from .env; never print or hard-code the secret."""
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv(PROJECT_DIR / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY not found. Put it in a local .env file "
            "inside this project folder."
        )
    # Our code handles retryable errors, so turn off the SDK's automatic retries.
    return OpenAI(api_key=api_key, timeout=60.0, max_retries=0)


def load_products(count: int):
    """Load the same fashion dataset used in the completed notebook."""
    from datasets import load_dataset

    print(f"Loading dataset: {DATASET_NAME}...")
    # Loading the first 100 rows matches the notebook and often reuses its cache.
    dataset = load_dataset(DATASET_NAME, split=f"train[:{max(100, count)}]")
    print(f"Dataset loaded successfully: {len(dataset)} rows")
    print("Dataset columns:", dataset.column_names)
    return [dataset[i] for i in range(min(count, len(dataset)))]


def save_product_image(product: dict[str, Any], index: int) -> Path:
    """Save the dataset's image as a local JPEG file."""
    from PIL import Image

    image = product.get("image")
    if not isinstance(image, Image.Image):
        raise ValueError(f"Product {index}: dataset image is not a PIL image")

    IMAGE_DIR.mkdir(exist_ok=True, parents=True)
    image_path = IMAGE_DIR / f"product{index}.jpg"
    image.convert("RGB").save(image_path, format="JPEG")
    return image_path


def encode_image_to_base64(image_path: Path | str) -> str:
    """Encode a local JPEG/PNG image to base64 for the API request."""
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path.name}")
    if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        raise ValueError("Only JPEG and PNG images are supported")
    return base64.b64encode(image_path.read_bytes()).decode("utf-8")


def create_product_listing_prompt(
    product_name: str,
    price: float | None,
    category: str,
    additional_info: str | None = None,
) -> str:
    """Ask for structured copy without inventing product specifications."""
    price_text = f"${price:.2f}" if price is not None else "Not provided"
    return f"""You are an expert e-commerce copywriter. Analyze the attached product image.

Product information:
- Name: {product_name}
- Price: {price_text}
- Category: {category}
- Other known metadata: {additional_info or 'Not provided'}

Create a professional product listing with:
1. An SEO-friendly title (maximum 60 characters)
2. A detailed description of 160-180 words.
Before returning the JSON, check the description's word count.
If it is under 150 words, expand it using only verified
product details. Do not invent specifications.
3. A list of 5-7 key features
4. A comma-separated string of 10-15 SEO keywords

Return ONLY a valid JSON object with exactly this structure:
{{
  "title": "Product title",
  "description": "Product description",
  "features": ["Feature 1", "Feature 2"],
  "keywords": "keyword1, keyword2"
}}

Describe visible color, shape, style and other supported details.
Do not invent materials, fit, technical specifications, warranty, performance,
water resistance, price, or other details that the image/metadata cannot verify.
If information is unknown, omit it rather than guessing.
Write naturally; do not make unsupported claims just to reach the word count.
"""


def parse_listing_response(response_text: str | None) -> dict[str, Any]:
    """Parse and verify the JSON returned by the API."""
    if not response_text:
        raise ValueError("The API returned an empty response")
    listing = json.loads(response_text)
    if not isinstance(listing, dict):
        raise ValueError("Expected a JSON object")
    for field in ("title", "description", "features", "keywords"):
        if field not in listing:
            raise ValueError(f"Missing field in API response: {field}")
    if not isinstance(listing["features"], list):
        raise ValueError("The 'features' field must be a list")
    if not all(isinstance(listing[k], str) for k in ("title", "description", "keywords")):
        raise ValueError("Title, description and keywords must be text")
    return listing


def quality_warnings(listing: dict[str, Any]) -> list[str]:
    """Check whether the result follows the lab's output requirements."""
    warnings = []
    if len(listing["title"]) > 60:
        warnings.append("Title exceeds 60 characters")
    words = len(listing["description"].split())
    if not 150 <= words <= 200:
        warnings.append(f"Description contains {words} words (target: 150-200)")
    n_features = len(listing["features"])
    if not 5 <= n_features <= 7:
        warnings.append(f"Features: {n_features} (target: 5-7)")
    n_keywords = len([k for k in listing["keywords"].split(",") if k.strip()])
    if not 10 <= n_keywords <= 15:
        warnings.append(f"Keywords: {n_keywords} (target: 10-15)")
    return warnings


def call_chatgpt_vision(client, image_path: Path, prompt: str, model: str) -> dict[str, Any]:
    """Call a vision-capable model, retrying only temporary API failures."""
    from openai import APIConnectionError, APITimeoutError, InternalServerError, RateLimitError

    encoded_image = encode_image_to_base64(image_path)
    mime_type = "image/png" if image_path.suffix.lower() == ".png" else "image/jpeg"

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{encoded_image}"
                                },
                            },
                        ],
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=1000,
            )
            return parse_listing_response(response.choices[0].message.content)
        except (RateLimitError, APIConnectionError, APITimeoutError, InternalServerError) as exc:
            if attempt == 2:
                raise
            wait = 2 ** attempt
            print(f"  Temporary API error ({type(exc).__name__}); retry in {wait}s")
            time.sleep(wait)
    raise RuntimeError("Could not get a response from the API")


def product_metadata(product: dict[str, Any]) -> str:
    """Use only fields that are present in the product dataset."""
    fields = ("gender", "subCategory", "articleType", "baseColour", "usage")
    details = [f"{field}: {product[field]}" for field in fields if product.get(field)]
    return "; ".join(details)


def save_results(listings: list[dict[str, Any]], output_path: Path) -> None:
    """Save valid JSON and safely replace the prior output."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(listings, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp_path.replace(output_path)


def process_products(count: int, model: str, output_path: Path, dry_run: bool) -> None:
    products = load_products(count)
    if not products:
        raise RuntimeError("The dataset returned no products")

    client = None if dry_run else create_client()
    generated_listings: list[dict[str, Any]] = []
    failed = 0

    for index, product in enumerate(products, start=1):
        try:
            image_path = save_product_image(product, index)
            name = str(product.get("productDisplayName") or "Fashion Product")
            category = str(product.get("masterCategory") or "Fashion")
            # This dataset has no price column. None is more accurate than $0.00.
            price = product.get("price")
            prompt = create_product_listing_prompt(
                product_name=name,
                price=float(price) if price is not None else None,
                category=category,
                additional_info=product_metadata(product),
            )
            encoded_length = len(encode_image_to_base64(image_path))
            if dry_run:
                print(f"Product {index}: READY — {name} | image encoded ({encoded_length} chars)")
                continue

            listing = call_chatgpt_vision(client, image_path, prompt, model)
            listing["product_id"] = int(product["id"])
            generated_listings.append(listing)
            save_results(generated_listings, output_path)  # Keep successes even if later calls fail.
            print(f"Product {index}: SUCCESS — {name}")
            for warning in quality_warnings(listing):
                print(f"  Quality warning: {warning}")
        except Exception as exc:
            failed += 1
            # Do not print the API key or the complete HTTP request.
            print(f"Product {index}: ERROR — {type(exc).__name__}: {exc}")
        if index < len(products) and not dry_run:
            time.sleep(1)  # Simple pacing for the API.

    if dry_run:
        print("Dry run complete. No API requests were sent and existing JSON was not changed.")
    else:
        print(f"Finished: {len(generated_listings)} success(es), {failed} failure(s)")
        print(f"Results saved to: {output_path}")


def check_existing(output_path: Path) -> None:
    """Inspect an existing output file without downloading or calling the API."""
    if not output_path.is_file():
        print(f"No existing JSON found: {output_path}")
        return
    listings = json.loads(output_path.read_text(encoding="utf-8"))
    if not isinstance(listings, list):
        raise ValueError("Existing JSON must contain a list of product listings")
    print(f"Existing output contains {len(listings)} product listings")
    for index, raw in enumerate(listings, start=1):
        listing = parse_listing_response(json.dumps(raw))
        print(f"Product {index}: {listing['title']}")
        for warning in quality_warnings(listing):
            print(f"  Quality warning: {warning}")


def test_error_handling() -> None:
    """Demonstrate two failures locally; no API key or network needed."""
    cases = [
        ("Missing image", lambda: encode_image_to_base64(IMAGE_DIR / "file_does_not_exist.jpg")),
        ("Invalid JSON", lambda: parse_listing_response("not valid json")),
    ]
    for label, action in cases:
        try:
            action()
            print(f"{label}: ERROR — expected a failure")
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
            print(f"{label}: HANDLED — {type(exc).__name__}")
    print("Error-handling tests complete; no API requests were sent.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate product listings from fashion images")
    parser.add_argument("--limit", type=int, default=3, help="Number of products (default: 3)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Vision-capable model name")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="JSON output path")
    parser.add_argument("--dry-run", action="store_true", help="Download and encode images only")
    parser.add_argument("--check-existing", action="store_true", help="Check existing JSON without API")
    parser.add_argument("--test-errors", action="store_true", help="Simulate errors without API")
    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be at least 1")
    output_path = args.output if args.output.is_absolute() else PROJECT_DIR / args.output

    if args.test_errors:
        test_error_handling()
    elif args.check_existing:
        check_existing(output_path)
    else:
        try:
            process_products(args.limit, args.model, output_path, args.dry_run)
        except Exception as exc:
            print(f"Setup error — {type(exc).__name__}: {exc}")
            raise SystemExit(1) from None


if __name__ == "__main__":
    main()
