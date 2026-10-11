# ==========================================
# AI PRODUCT LISTING GENERATOR
# Ironhack - ChatGPT API Lab
# ==========================================

# Import libraries
import os
import json
import base64

from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset


# ==========================================
# 1. CONFIGURATION
# ==========================================

# Load API key from .env
load_dotenv()

api_key = os.getenv("OPENAI_ADMIN_KEY")

if not api_key:
    raise ValueError("API key not found in .env")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Create output folder
output_dir = Path("generated_listings")
output_dir.mkdir(exist_ok=True)

print("Configuration completed successfully!")

# ==========================================
# 2. CREATE PRODUCT PROMPT
# ==========================================

def create_product_prompt(product):

    prompt = f"""
You are an expert e-commerce copywriter.

Create a professional product listing using the product
information below and the product image.

PRODUCT INFORMATION:
Name: {product['productDisplayName']}
Category: {product['masterCategory']}
Subcategory: {product['subCategory']}
Type: {product['articleType']}
Color: {product['baseColour']}
Gender: {product['gender']}
Usage: {product['usage']}

REQUIREMENTS:
1. Create an attractive product title.
2. Write a detailed description between 160 and 180 words.
3. Include 5-7 key product features.
4. Generate 10-15 SEO keywords.
5. Use a professional and persuasive tone.
6. Do not invent materials, specifications or prices.
7. Return only valid JSON.

JSON STRUCTURE:
{{
    "title": "Product title",
    "description": "Product description",
    "features": ["Feature 1", "Feature 2"],
    "keywords": ["Keyword 1", "Keyword 2"]
}}
"""
    return prompt


# ==========================================
# 3. ENCODE PRODUCT IMAGE
# ==========================================

def encode_product_image(product):

    image = product["image"]

    if image is None:
        raise ValueError("Product image is missing")

    buffer = BytesIO()

    image.convert("RGB").save(buffer, format="PNG")

    encoded_image = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return encoded_image


print("Product functions loaded successfully!")

# ==========================================
# 4. GENERATE PRODUCT LISTING WITH OPENAI
# ==========================================

def generate_product_listing(product):

    try:
        # Prepare the product prompt
        prompt = create_product_prompt(product)

        # Convert product image to Base64
        encoded_image = encode_product_image(product)

        # Send text and image to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=1200
        )

        # Convert the JSON response to a Python dictionary
        listing = json.loads(
            response.choices[0].message.content
        )

        return listing

    except Exception as error:
        print(
            "Error generating product listing:",
            type(error).__name__,
            str(error)
        )
        return None


print("OpenAI generation function loaded successfully!")

# ==========================================
# 5. BATCH PROCESSING
# ==========================================

def process_products(dataset):

    for product in dataset:

        product_id = product["id"]
        product_name = product["productDisplayName"]

        output_file = output_dir / f"product_{product_id}.json"

        print(f"\nProcessing: {product_name}")

        # Check if the product was already generated
        if output_file.exists():
           print("SKIPPED: Product listing already exists.")

           # Load the existing JSON file
           with open(output_file, "r", encoding="utf-8") as file:
            existing_listing = json.load(file)

           # Validate the existing product listing
           errors = validate_listing(existing_listing)

           if not errors:
               print("Validation: PASSED")
           else:
               print("Validation: FAILED")
               for error in errors:
                   print("-", error)

           continue

        # Generate listing only if it does not exist
        listing = generate_product_listing(product)

        if listing is not None:

            # Validate the generated listing
            errors = validate_listing(listing)

            if not errors:

                print("Validation: PASSED")

                with open(output_file, "w", encoding="utf-8") as file:
                    json.dump(
                        listing,
                        file,
                        indent=4,
                        ensure_ascii=False
                    )

                print("Listing saved:", output_file)

            else:

                print("Validation: FAILED")

                for error in errors:
                    print("-", error)

                print("Listing not saved because validation failed.")

        else:
            print("FAILED: Could not generate product listing.")


print("Batch processing function loaded successfully!")

# ==========================================
# 6. VALIDATE PRODUCT LISTING
# ==========================================

def validate_listing(listing):

    description = listing.get("description", "")
    features = listing.get("features", [])
    keywords = listing.get("keywords", [])

    errors = []

    word_count = len(description.split())

    if not 150 <= word_count <= 200:
        errors.append(
            f"Description must have 150-200 words. Found: {word_count}"
        )

    if not 5 <= len(features) <= 7:
        errors.append("Features must contain 5-7 items")

    if not 10 <= len(keywords) <= 15:
        errors.append("Keywords must contain 10-15 items")

    return errors


print("Validation function loaded successfully!")

# ==========================================
# 6. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("\nSTARTING PRODUCT LISTING GENERATOR")
    print("=" * 50)

    # Load the first three products
    dataset = load_dataset(
        "ashraq/fashion-product-images-small",
        split="train[:3]"
    )

    # Process products
    process_products(dataset)

    print("\nBatch processing completed!")

    # ==========================================
# 7. ERROR HANDLING TEST
# ==========================================

def test_error_handling():

    print("\nTESTING ERROR HANDLING")
    print("=" * 50)

    try:
        # Simulate an API connection error
        raise ConnectionError("Simulated API connection failure")

    except ConnectionError as error:
        print("Error detected:", str(error))
        print("Error handled successfully!")

# test_error_handling()