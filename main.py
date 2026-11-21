import base64
import json
import os
from datasets import load_dataset
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load the product dataset
dataset = load_dataset(
    "arturayupov/womens-fashion-catalog",
    "products"
)

products = dataset["train"].select(range(20)).to_pandas()

# Create images folder
Path("images").mkdir(exist_ok=True)

# Download product images
for index, row in products.iterrows():

    image_url = row["featured_image_url"]

    if pd.notna(image_url):
        response = requests.get(image_url, timeout=30)

        if response.status_code == 200:
            image_path = Path("images") / f"product_{index + 1:03}.jpg"
            image_path.write_bytes(response.content)
            print(f"Downloaded product {index + 1}")

# Save product information
products.to_csv("products.csv", index=False)

print("\nDownload complete!")

# Create a list of product dictionaries
product_list = []

for index, row in products.iterrows():

    product = {
        "id": row["id"],
        "name": row["title"],
        "category": row["product_type"],
        "price": row["price_min_usd"],
        "description": row["description"],
        "image": f"images/product_{index + 1:03}.jpg"
    }

    product_list.append(product)

print("\nFirst product:")
print(product_list[0])

print("\nTotal products:", len(product_list))

# Save products as JSON
with open("products.json", "w", encoding="utf-8") as file:
    json.dump(product_list, file, indent=4, ensure_ascii=False)

print("\nProducts saved to products.json")

# Encode an image to Base64
def encode_image_to_base64(image_path):
    """Encode an image file to a Base64 string."""
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return encoded


# Test with the first product image
sample_path = product_list[0]["image"]

encoded_image = encode_image_to_base64(sample_path)

print(f"Encoded image length: {len(encoded_image)} characters")
print(f"Encoded prefix: {encoded_image[:40]}...")

def create_product_listing_prompt(
    product_name, price, category, additional_info=None
):
    """Create a prompt for generating product listings."""

    prompt = f"""
You are an expert e-commerce copywriter.

Analyze the product image and create a compelling product listing.

Product Information:
- Name: {product_name}
- Price: ${price:.2f}
- Category: {category}
{f'- Additional Info: {additional_info}' if additional_info else ''}

Please create a professional product listing that includes:

1. Product Title (SEO-friendly, maximum 60 characters)
2. Product Description (150-200 words)
3. Key Features (5-7 bullet points)
4. SEO Keywords (10-15 relevant keywords)

Format your response as JSON:

{{
    "title": "Product title here",
    "description": "Full description here",
    "features": ["Feature 1", "Feature 2"],
    "keywords": "keyword1, keyword2"
}}

Be specific about visible details in the image.
Mention colours, materials, design elements and distinctive features.
"""

    return prompt


# Test prompt creation
test_prompt = create_product_listing_prompt(
    product_name="Wireless Bluetooth Headphones",
    price=79.99,
    category="Electronics",
    additional_info="Noise cancelling, 30-hour battery"
)

print("\n" + "=" * 50)
print("PROMPT TEMPLATE")
print("=" * 50)
print(test_prompt[:500] + "...")

# Load the API key
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialise OpenAI client
client = OpenAI()


# Function to generate a listing for one product
def generate_product_listing(product):

    prompt = create_product_listing_prompt(
        product_name=product["name"],
        price=product["price"],
        category=product["category"],
        additional_info=product["description"]
    )

    # Encode product image
    encoded_image = encode_image_to_base64(product["image"])
    image_data_url = f"data:image/jpeg;base64,{encoded_image}"

    # Call OpenAI API
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": image_data_url}
                ]
            }
        ],
        text={"format": {"type": "json_object"}}
    )

    return json.loads(response.output_text)


# Process multiple products
generated_listings = []
errors = []

for product in product_list[:3]:

    print(f"\nProcessing: {product['name']}")

    try:
        listing = generate_product_listing(product)

        generated_listings.append({
            "id": product["id"],
            "original_name": product["name"],
            "generated_listing": listing
        })

        print("Listing generated successfully!")

    except Exception as error:
        errors.append({
            "product": product["name"],
            "error": str(error)
        })

        print(f"Error processing product: {error}")


# Save results
results = {
    "listings": generated_listings,
    "errors": errors
}

with open("generated_listings.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print("\nBATCH PROCESSING COMPLETE")
print(f"Successful listings: {len(generated_listings)}")
print(f"Errors: {len(errors)}")
print("Results saved to generated_listings.json")