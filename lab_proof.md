# API Calling to ChatGPT Lab — Evidence

This file is the entry point for the reviewer. The primary step-by-step workflow
is the Jupyter notebook [`product_generator.ipynb`](product_generator.ipynb).
The completed Python reference implementation is available in
[`product_generator.py`](product_generator.py).

## Workflow and setup

The project uses the supplied parquet dataset at
`data/train-00000-of-00002-6cff4c59f91661c3.parquet`. It contains 22,036 catalog
rows and embedded image bytes, so a second dataset download is not needed.

The notebook required these packages:

```python
%pip install python-dotenv openai pandas pyarrow pillow
```

Create `.env` locally (never commit it):

```text
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

The API key was stored in `.env` and loaded with `python-dotenv`. It was never
printed or hard-coded in the notebook. `.gitignore` protects `.env` from being
committed.

## Notebook workflow and input

The notebook demonstrates the complete workflow:

1. Initialize the OpenAI client securely.
2. Load the parquet product dataset.
3. Inspect product metadata and an embedded image.
4. Encode the image as Base64.
5. Create a structured product-listing prompt.
6. Send the prompt and image to the OpenAI vision model.
7. Parse and validate the JSON response.
8. Process three products in a batch.
9. Save the generated listings.
10. Test an error case with missing image data.

The model input consisted of each product's metadata, a product-specific prompt,
and a Base64-encoded image data URL. The requested output schema contained
`title`, `description`, `features`, and `keywords`.

## Evidence and final output

The notebook successfully processed three products:

- Turtle Check Men Navy Blue Shirt
- Peter England Men Party Blue Jeans
- Titan Women Silver Watch

Run output:

```text
Batch processing complete.
Total products processed: 3
Successful products: 3
Failed products: 0
```

The final generated listings are saved in
[`outputs/notebook_product_listings.json`](outputs/notebook_product_listings.json).
The extracted sample images are available in
[`product_images/product_15970.jpg`](product_images/product_15970.jpg),
[`product_images/product_39386.jpg`](product_images/product_39386.jpg), and
[`product_images/product_59263.jpg`](product_images/product_59263.jpg).

## Error handling and limitation

The notebook simulated a product with missing image data. The workflow caught
the problem and reported a `ValueError` instead of stopping unexpectedly.

Other limitations are that live requests require a valid OpenAI API key and API
credits, and requests may be affected by network errors or rate limits.

## Reflection

- API integration requires authentication, request preparation, response parsing,
  and error handling.
- Base64 encoding allows local images to be sent to a vision model as data URLs.
- Prompt structure improves consistency by requiring a fixed JSON format.
- Batch processing saves time compared with writing each product listing manually.
- API keys must be stored securely and never committed to version control.
