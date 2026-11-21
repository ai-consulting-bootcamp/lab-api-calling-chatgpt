# Lab Proof – E-commerce Product Listing Generation

## 1. Project Overview

This project uses the OpenAI API with image input to generate professional e-commerce product listings.

The workflow:
- Loads product information from a Hugging Face dataset.
- Downloads product images.
- Encodes images into Base64 format.
- Sends product information and images to the OpenAI API.
- Generates structured product listings in JSON format.
- Processes multiple products and saves the results.

## 2. Code and Supporting Files

- [main.py](main.py) – Complete Python workflow and API integration.
- [products.csv](products.csv) – Product dataset in CSV format.
- [products.json](products.json) – Product information in JSON format.
- [generated_listings.json](generated_listings.json) – Final AI-generated product listings.
- [images](images/) – Product images used as input.

## 3. Example Input

The first product processed was:

- **Name:** Openwork V-Neck Slit Cover-Up
- **Category:** Swimwear
- **Price:** $28.99
- **Image:** images/product_001.jpg

The workflow combined this product information with its image and a structured prompt requesting an SEO-friendly title, a 150–200-word description, key features and SEO keywords.

## 4. Evidence – Batch Processing

The following output was produced in the Terminal:

```text
Processing: Openwork V-Neck Slit Cover-Up
Listing generated successfully!

Processing: Flower PU Leather Stiletto Heel Sandals
Listing generated successfully!

Processing: Round Toe Platform Sneakers
Listing generated successfully!

BATCH PROCESSING COMPLETE
Successful listings: 3
Errors: 0
Results saved to generated_listings.json
```

## 5. Final Output

The workflow successfully generated three product listings and saved them in:

[generated_listings.json](generated_listings.json)

The JSON file contains the generated titles, descriptions, key features and SEO keywords for each successfully processed product.

## 6. Failure or Limitation

For this test, the workflow was configured to process only the first three products rather than the full dataset of 20.

This was a deliberate limitation to test the batch-processing workflow while controlling API usage. The three products were processed successfully, with no errors.

## 7. Conclusion

The project successfully demonstrates image-based product analysis, OpenAI API integration, structured JSON generation and batch processing with error handling.
