# LAB | API Calling to ChatGPT

Delivered by Carolina, November 2026

## Summary

**Scenario:** We are working as an AI automation specialist for an e-commerce company. Our team needs to automate the creation of product listings from product images and basic information. Instead of manually writing descriptions, we used ChatGPT's vision capabilities (`gpt-4o`) to generate the listings.

**What we built:** a Python pipeline that:

1. Loads 100 fashion products from the HuggingFace dataset `ashraq/fashion-product-images-small` and saves their images to disk
2. Encodes each image in base64
3. Builds a copywriting prompt from the product data (name, category, colour, gender, season, usage)
4. Sends prompt + image to the OpenAI API and asks for a JSON response (title, description, features, keywords)
5. Runs the pipeline in batch over 5 products and saves the results to `listings.json`

The API key is read from a local `.env` file (listed in `.gitignore`, not committed).

## Files

| File                                                 | What it is                                      |
| ---------------------------------------------------- | ----------------------------------------------- |
| `lab_proof.md`                                       | This file: entry point for the reviewer         |
| [LAB_API_ChatGPT.ipynb](LAB_API_ChatGPT.ipynb)       | Full Jupyter notebook with code and outputs     |
| [listings.json](listings.json)                       | Final output: generated listings for 5 products |
| [product_images/15970.jpg](product_images/15970.jpg) | Image used in the example run below             |

---

## Example run

**Input**

- Image: [product_images/15970.jpg](product_images/15970.jpg)
- Product data (from the dataset): Turtle Check Men Navy Blue Shirt · Apparel > Topwear > Shirts · Navy Blue · Men · Fall · Casual
- Price: €49.99 (sample value; the dataset has no prices)
- Prompt sent to the API together with the image (first part):

```
You are an expert e-commerce copywriter. Analyze the product image and create a compelling product listing.

Use a friendly and casual tone.
Use simple language.
Write for everyday online shoppers.

Product Information:
- Name: Turtle Check Men Navy Blue Shirt
- Price: €49.99
- Category: Apparel > Topwear > Shirts
- Additional Info: Colour: Navy Blue, Gender: Men, Season: Fall, Usage: Casual

Please create a professional product listing that includes:
1. Product Title (catchy, SEO-friendly, 60 characters max)
2. Product Description (detailed, 150-200 words)
3. Key Features (bullet points, 5-7 items)
4. SEO Keywords (comma-separated, 10-15 relevant keywords)

Format your response as JSON (title, description, features, keywords).
```

**Evidence (API response, parsed JSON)**

```json
{
  "title": "Stylish Turtle Check Navy Blue Men's Shirt",
  "description": "Step up your casual wardrobe game with the Turtle Check Men Navy Blue Shirt! Designed for the modern man, this shirt brings a perfect blend of style and comfort. Its striking navy blue check pattern adds a fresh twist to the classic men's shirt, making it a versatile piece for any casual outing. The premium fabric is soft against your skin, ensuring all-day comfort. Tailored for the fall season, this shirt is perfect for layering or wearing on its own. Whether you're heading to a casual meet-up or a relaxed day out, this shirt is your go-to choice for effortless style. Pair it with your favorite jeans or chinos, and you're ready to rock any look!",
  "features": [
    "Navy blue check pattern for a classic yet modern look",
    "Comfortable premium fabric, perfect for all-day wear",
    "Ideal for fall season with its breathable material",
    "Versatile style, suitable for casual occasions",
    "Easy to pair with jeans, chinos, or shorts",
    "Durable stitching ensures long-lasting use"
  ],
  "keywords": "men's shirt, navy blue shirt, casual shirt, fall fashion, men's topwear, check pattern shirt, breathable fabric, stylish men's shirt, versatile men's clothing, turtle check shirt"
}
```

## Final output

Batch run over the first 5 products (IDs 15970, 39386, 59263, 21379, 53759):

```
Successful listings: 5
Failed listings: 0
```

All 5 listings are saved in [listings.json](listings.json), each with `id`, `name`, `status` and the generated `listing`.

## Code (full Jupyter notebook export)

```python
#STEP 1: Setting Up OpenAI API Access

#!pip install python-dotenv

from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os #operational system

load_dotenv()  # reads .env and puts its values into the environment

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    input="What is machine learning?"
)

print(response.output_text)
```

    Machine learning is a subset of artificial intelligence (AI) that focuses on the development of algorithms and statistical models that enable computers to learn from and make predictions or decisions based on data. It involves training a model on a dataset to recognize patterns and improve its performance over time without being explicitly programmed for specific tasks.

    Key aspects of machine learning include:

    1. **Data**: The foundation for machine learning models, data is used to train algorithms to make predictions or decisions.

    2. **Algorithms**: Methods or procedures that the model uses to learn from data. Common types include supervised learning, unsupervised learning, and reinforcement learning.

    3. **Model**: A mathematical representation of the learning process. Once trained, the model can make predictions or decisions.

    4. **Training**: The process of feeding data to an algorithm and allowing it to learn underlying patterns.

    5. **Evaluation**: Assessing the model’s accuracy and performance using validation data that wasn't part of the training set.

    6. **Iteration**: Refining the model through repeated training and evaluation to improve its accuracy and generalization.

    Applications of machine learning span various fields, such as finance, healthcare, marketing, and autonomous systems, enabling advancements in areas like natural language processing, computer vision, and predictive analytics.

```python
# STEP 2: PREPARING THE DATA SET

# Install: pip install datasets
from datasets import load_dataset
import requests
from PIL import Image
import pandas as pd
from pathlib import Path

# Load dataset from HuggingFace
print("Loading product dataset...")
try:
    # Try loading the dataset
    dataset = load_dataset("ashraq/fashion-product-images-small", split="train[:100]")  # First 100 samples
    print(f"✓ Loaded {len(dataset)} products")

    # Convert to pandas for easier manipulation
    products_df = pd.DataFrame(dataset)
    print(f"Dataset columns: {products_df.columns.tolist()}")

except Exception as e:
    print(f"⚠ Could not load HuggingFace dataset: {e}")
    print("Using local images instead...")

    # Alternative: Use local images
    # Create a products.json file with product information
    products_data = [
        {
            "id": 1,
            "name": "Wireless Headphones",
            "price": 79.99,
            "category": "Electronics",
            "image_path": "images/product1.jpg"
        },
        # Add more products...
    ]

    products_df = pd.DataFrame(products_data)

# Create images directory
images_dir = Path("product_images")
images_dir.mkdir(exist_ok=True)

# Save each product image to disk and record its path
image_paths = []
for _, row in products_df.iterrows():
    path = images_dir / f"{row['id']}.jpg"
    row["image"].convert("RGB").save(path)
    image_paths.append(str(path))

products_df["image_path"] = image_paths
print(f"  Images saved to: {images_dir}/")

print(f"\n✓ Dataset prepared!")
print(f"  Total products: {len(products_df)}")
```

    Loading product dataset...
    ✓ Loaded 100 products
    Dataset columns: ['id', 'gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage', 'productDisplayName', 'image']
      Images saved to: product_images/

    ✓ Dataset prepared!
      Total products: 100

```python
# STEP 3: ENCODING IMAGES FOR API
##Objective: Convert product images to base64 format for API transmission.

import base64

def encode_image_to_base64(image_path):
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return encoded

# Example usage
sample_path = products_df.iloc[0]["image_path"]
encoded_image = encode_image_to_base64(sample_path)
print(f"Encoded image length: {len(encoded_image)} characters")
print(f"Encoded prefix: {encoded_image[:40]}...")
```

    Encoded image length: 2388 characters
    Encoded prefix: /9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcG...

```python
# STEP 4: CREATING THE PRODUCT LISTING PROMPT
##Design an effective prompt for generating product listings.


def create_product_listing_prompt(
    product_name,
    price,
    category,
    additional_info=None,
    tone="casual",
    language_level="simple",
    target_audience="general shoppers"
):
    """
    Create a prompt for generating product listings.

    Parameters:
    - product_name: Name of the product
    - price: Price of the product
    - category: Product category
    - additional_info: baseColour, season, or gender-specific information (optional)
    - tone: Writing tone, such as casual or formal
    - language_level: Language complexity, such as simple or technical
    - target_audience: Intended audience for the listing

    Returns:
    - Formatted prompt string
    """
    prompt = f"""You are an expert e-commerce copywriter. Analyze the product image and create a compelling product listing.

Use a {tone} tone.
Use {language_level} language.
Write for {target_audience}.

Product Information:
- Name: {product_name}
- Price: €{price:.2f}
- Category: {category}
{f'- Additional Info: {additional_info}' if additional_info else ''}

Please create a professional product listing that includes:

1. **Product Title** (catchy, SEO-friendly, 60 characters max)
2. **Product Description** (detailed, 150-200 words)
   - Highlight key features and benefits
   - Use persuasive language
   - Include relevant details visible in the image
3. **Key Features** (bullet points, 5-7 items)
4. **SEO Keywords** (comma-separated, 10-15 relevant keywords)

Format your response as JSON with the following structure:
{{
    "title": "Product title here",
    "description": "Full description here",
    "features": ["Feature 1", "Feature 2", ...],
    "keywords": "keyword1, keyword2, ..."
}}

Analyze the product image and create a compelling product listing.
Return the result as JSON.
"""
    return prompt

# Test prompt creation

row = products_df.iloc[0]

test_prompt = create_product_listing_prompt(
    product_name=row["productDisplayName"],
    price=49.99,                      # dataset has no price, so use a sample value
    category=f"{row['masterCategory']} > {row['subCategory']} > {row['articleType']}",
    additional_info=f"Colour: {row['baseColour']}, Gender: {row['gender']}, Season: {row['season']}, Usage: {row['usage']}",
    tone="friendly and casual",
    language_level="simple",
    target_audience="everyday online shoppers"
)

print("\n" + "="*50)
print("PROMPT TEMPLATE")
print("="*50)
print(test_prompt[:500] + "...")  # Show first 500 characters
```

    ==================================================
    PROMPT TEMPLATE
    ==================================================
    You are an expert e-commerce copywriter. Analyze the product image and create a compelling product listing.

    Use a friendly and casual tone.
    Use simple language.
    Write for everyday online shoppers.

    Product Information:
    - Name: Turtle Check Men Navy Blue Shirt
    - Price: €49.99
    - Category: Apparel > Topwear > Shirts
    - Additional Info: Colour: Navy Blue, Gender: Men, Season: Fall, Usage: Casual

    Please create a professional product listing that includes:

    1. **Product Title** (catchy, SEO-friendly,...

````python
# STEP 5: Calling the ChatGPT API with Vision
## Send image + text to the API, receive the response, parse the JSON

import json
from pathlib import Path

def generate_listing(prompt, image_path, model="gpt-4o"):
    """
    Send a prompt + product image to the ChatGPT API
    and return the listing as a dictionary.
    """
    # 1. Encode the image and build the data URL
    image_b64 = encode_image_to_base64(image_path)
    suffix = Path(image_path).suffix.lower().replace(".", "")
    mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
    image_url = f"data:image/{mime};base64,{image_b64}"

    # 2. Call the API
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
    except Exception as e:
        print(f"⚠ API call failed: {e}")
        return None

    # 3. Get the text of the response
    raw_text = response.choices[0].message.content

    # 4. Parse the JSON (strip ```json fences just in case)
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("⚠ Could not parse JSON, returning raw text")
        return {"raw_response": raw_text}


# Test with one product
listing = generate_listing(test_prompt, row["image_path"])

if listing:
    print(json.dumps(listing, indent=2, ensure_ascii=False))
````

Output: see **Evidence** in the Example run section above.

```python
#STEP 6: Processing Multiple Products
##Objective: Generate listings for multiple products in batch.

import time

sample = products_df.head(5)  # Process first 5 products for testing
results = []

for index, row in sample.iterrows():
    print(f"Processing {row['id']}...")

    prompt = create_product_listing_prompt(
        product_name=row["productDisplayName"],
        price=49.99,  # Sample price
        category=f"{row['masterCategory']} > {row['subCategory']} > {row['articleType']}",
        additional_info=f"Colour: {row['baseColour']}, Gender: {row['gender']}, Season: {row['season']}, Usage: {row['usage']}"
    )

    listing = generate_listing(prompt, row["image_path"])

    if listing is None:
        status = "failed"
    elif "raw_response" in listing:
        status = "json_error"
    else:
        status = "success"

    results.append({
        "id": row['id'],
        "name": row['productDisplayName'],
        "status": status,
        "listing": listing
    })

    time.sleep(1)

# Save
with open("listings.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Summary
success_count = sum(1 for r in results if r["status"] == "success")
failure_count = len(results) - success_count
print(f"Successful listings: {success_count}")
print(f"Failed listings: {failure_count}")
```

    Processing 15970...
    Processing 39386...
    Processing 59263...
    Processing 21379...
    Processing 53759...
    Successful listings: 5
    Failed listings: 0
