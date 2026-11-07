# Lab Proof — API Calling to ChatGPT

## Reviewer entry point

This submission demonstrates an automated product-listing workflow using the OpenAI API with product images. The workflow loads product data, encodes an image as Base64, sends image and text input to a vision-capable model, parses the JSON response, processes three products, and saves the generated listings.

## Code / workflow export

The complete executable workflow is in [`product_listing_generator.ipynb`](product_listing_generator.ipynb).

Supporting files:

- Input image used by the workflow: [`product_images/15970.jpg`](product_images/15970.jpg)
- Final generated listings: [`product_listings.json`](product_listings.json)

The notebook loads the API key from an environment variable. No API key is included in this submission.

## Run and input

The main vision run is in notebook cells 15–21. Its input consists of:

1. The first product image from the loaded dataset, converted to a JPEG Base64 data URL.
2. This text prompt:

```text
Analyze this product image and create a product listing.

Return only valid JSON with these fields:
{
  "title": "...",
  "description": "...",
  "category": "...",
  "features": ["...", "..."],
  "keywords": "keyword1, keyword2"
}
```

The batch run is in notebook cells 22–27. It selects the first three dataset products, sends each image to the API, parses each response, and writes the results to `product_listings.json`.

## Evidence produced

Saved notebook outputs show:

- API key availability was verified: `API key loaded: True`.
- The dataset loaded successfully with 100 products.
- The dataset columns included product metadata and an image field.
- Image encoding succeeded with an encoded length of 2,388 characters.
- The request was prepared with an image data URL and a non-empty prompt.
- The first API response was returned as JSON inside a Markdown code fence and was successfully cleaned and parsed.
- The parsed title and features were accessible from the JSON object.
- The batch run generated 3 listings and saved them successfully.
- The saved file was reopened and verified to contain 3 listings.

## Final output

The final output is [`product_listings.json`](product_listings.json). It contains three generated product listings:

1. Men's Casual Checkered Shirt
2. Men's Classic Fit Denim Jeans
3. Elegant Silver Women's Wristwatch

Each listing contains a title, description, category, features, and SEO keywords.

## Failure or limitation

The notebook contains an error-handling scaffold for API errors, file errors, JSON parsing errors, and missing fields, but this saved run does not include a deliberately triggered failure and therefore does not provide observed failure output.

There is also a workflow limitation: the batch prompt is generic and does not insert each product's individual metadata into the request. As a result, generated listings may be less specific than they would be with product name, category, and other metadata included for every item.

