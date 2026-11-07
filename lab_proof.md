# Product Listing Lab

## Failure tested
I tested a product with a missing image file. The code caught
FileNotFoundError and displayed:
"Image not found. Check the product's image_path."
## Code
[Open my notebook](product_listing_lab.ipynb)

## Final output
[View three generated product listings](product_listings.json)
## Example input
- Product: Puma Men Grey T-shirt
- Category: Apparel
- Practice price: $189879.99
- Image: [Product photo](product_images/product_4.png)

I sent the image and product details to the model, requesting
JSON with a title, description, features, and keywords.
## Limitation
The model initially claimed comfort and durability without evidence.
I updated the prompt to forbid these claims unless supported by
the product data.