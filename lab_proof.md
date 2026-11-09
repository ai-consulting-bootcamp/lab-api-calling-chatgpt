# LAB | API Calling to ChatGPT

## Submission overview

This project uses an OpenAI vision-capable model to generate e-commerce product listings from product images and metadata.

Supporting files:

- [Notebook workflow](./prepare_dataset.ipynb)
- [Generated product listings](./product_listings.json)
- [Bonus challenge utilities](./bonus_challenges.py)
- [Bonus challenge web interface](./bonus_app.py)

## Workflow and code

The complete executable workflow is in [prepare_dataset.ipynb](./prepare_dataset.ipynb). It includes:

1. OpenAI API client setup using an environment variable.
2. Product dataset loading from Hugging Face.
3. Product image inspection and Base64 encoding.
4. Prompt construction using product metadata.
5. Vision API requests containing text and image input.
6. JSON response parsing and validation.
7. Multi-product processing with retry handling.
8. Saving results to [product_listings.json](./product_listings.json).

## Run input

The batch run used:

```python
MAX_PRODUCTS = 3
```

Each product was sent with:

- Product image
- Product name
- Category
- Subcategory
- Colour
- Intended customer gender
- Season

The prompt requested a JSON response containing:

- SEO-friendly title
- 100–150 word description
- Five features
- Ten SEO keywords

## Evidence produced

The batch execution produced:

```text
Processing product 1/3...
Success: Turtle Check Men Navy Blue Shirt

Processing product 2/3...
Success: Peter England Men Party Blue Jeans

Processing product 3/3...
Success: Titan Women Silver Watch

Total results: 3
```

The saved output was then validated:

```text
File exists: True
Total saved results: 3
Successful saved results: 3
Validated: Turtle Check Men Navy Blue Shirt (ID: 15970)
Validated: Peter England Men Party Blue Jeans (ID: 39386)
Validated: Titan Women Silver Watch (ID: 59263)
```

## Final output

The final output is stored in [product_listings.json](./product_listings.json). It contains three successful product records. Each record includes:

- Dataset index
- Product ID
- Product name
- Generated listing
- Processing status

Each generated listing contains the requested `title`, `description`, `features`, and `keywords` fields.

## Bonus challenges

The reusable bonus implementation is in [bonus_challenges.py](./bonus_challenges.py):

- Multi-image analysis accepts a sequence of images for one product.
- Style customization supports tone, language style, and target audience.
- Cost tracking records prompt tokens, completion tokens, total tokens, and estimated cost using configurable prices.
- Quality scoring checks title presence, description length, feature count, and keyword count.
- JSON and flat CSV exports are provided for downstream e-commerce systems.

The optional [bonus_app.py](./bonus_app.py) provides a simple Streamlit interface for uploading multiple images, selecting writing style, generating a listing, and viewing quality and usage reports.

## Failure and limitation

During development, the multi-product loop initially failed because `current_listing` had not been assigned. The loop was corrected to call the API and parse each response before saving it.

The workflow also produced an unauthenticated Hugging Face warning. The dataset still loaded successfully, but authenticated Hugging Face access would provide higher rate limits and faster downloads.

Generated copy should be reviewed before publication because vision models can occasionally infer details that are not fully verifiable from a product image, such as material quality, durability, or care instructions.

