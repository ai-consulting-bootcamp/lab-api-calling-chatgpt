# Lab Proof: Calling the ChatGPT API with Vision

## Reviewer entry point

The notebook contains the runnable workflow and saved cell outputs for dataset preparation, image and prompt handling, a single vision request, JSON parsing, and multi-product processing:

- [Notebook workflow and run evidence](./LAB%20%7C%20API%20Calling%20to%20ChatGPT.ipynb)
- [Saved batch listings](./product_listings.json)

## Workflow export

The notebook is the workflow export. It loads the first 100 rows of `ashraq/fashion-product-images-small`, builds a product prompt, sends a product image and text to the OpenAI Responses API, requests schema-constrained JSON, and parses the response. Its batch cell then processes five rows and saves successful listings or per-product errors to `product_listings.json`.

## Run and input

The saved single-product run used product row `0` from the loaded dataset. Its image was converted to a PNG data URL. The text prompt included the available `productDisplayName`, `masterCategory`, `subCategory`, `articleType`, and `baseColour` fields, and asked for a concise ecommerce title, description, category, color, visible features, and search tags. The exact request code is in the notebook's Step 5 cell.

The batch run used rows `0–4` with the same image-plus-text workflow. The notebook output records **5 products processed, 5 succeeded, 0 failed**.

## Evidence produced

The notebook's saved Step 5 output reports `API response status: completed` and `API call succeeded and JSON parsed correctly`, followed by a parsed JSON listing. The batch cell output records a successful listing for each of the five products and confirms that the results were saved to `product_listings.json`.

## Final output

The Step 5 API response was:

```json
{
  "title": "Turtle Check Men Navy Blue Shirt",
  "description": "Elevate your wardrobe with this Turtle Check Men Navy Blue Shirt. Perfect for casual outings, it features a classic check pattern and a comfortable fit.",
  "category": "Apparel",
  "color": "Navy Blue",
  "features": [
    "Check pattern",
    "Short sleeves",
    "Button-down front"
  ],
  "tags": [
    "men's fashion",
    "shirt",
    "navy blue",
    "check pattern",
    "casual wear"
  ]
}
```

The complete batch output is available in [product_listings.json](./product_listings.json). The saved batch includes listings for Turtle Check Men Navy Blue Shirt, Peter England Men's Party Jeans - Blue, Titan Women Silver Watch, Manchester United Solid Black Track Pants, and Puma Men's Grey T-shirt.

## Failure or limitation encountered

Dataset loading produced a Hugging Face warning that the request was unauthenticated and could have lower rate limits and slower downloads. The dataset still loaded successfully. The batch run itself recorded no failed products.
