[labcalling.ipynb](./labcalling.ipynb)
[generated_listings.json](./generated_listings.json)
## Approach
1. API setup: The Ironhack API key is stored in a .env file, loaded with python-dotenv. To make sure it is not committed I stored the env file in a .gitignore file. 
2. Dataset: loaded the first 100 products and used a smaple of 20. Images are saved from PIL objects to JPG files, columns are renamed and placeholder prices are assigned by article type. 
3. Image encoding: each JPG is encoded to base64 so it can be sent inside the JSON request. 
4. Prompt: the template prompt is filled with name, price, category and additional metadata and asks for a json response. 
5. API call: image and prompt are sent in one request (chat.completions.create) with response_format={"type": "json_object"}; the response is parsed with json.loads.
6. Batch processing: a loop processes all prodcuts, catches errors per product with try/except, printsn a summary and saves the results to generated_listings.json 

## Example Run 
### Input:
- Product: Turtle Check Men Navy Blue Shirt (id 15970)
- Metadata: Category: Apparal, Price: $29.99 (placeholder), Atricle type: Shirts, colour: Navy Blue, target group: Men, usage: Casual, season: Fall
- Image: product_images/15970.jpg
- Prompt: template prompt from Step 4, filled with the metadata above 
### Evidence (raw Json returned by the API):
```json
{
  "title": "Turtle Check Men's Navy Blue Checked Shirt",
  "description": "A timeless casual essential, the Turtle Check Men Navy Blue Shirt pairs classic checks with everyday versatility. The shirt features a navy-blue base with crisp white and light-blue grid checks for a clean, contemporary look. Visible details include a classic collar, full button-front closure and a single chest pocket — all shown on a modern, streamlined silhouette. The sleeves are shown rolled for a relaxed, casual vibe, making this shirt ideal for layered fall outfits or weekend wear. Thoughtfully designed to be easy to style, it looks great over a tee or tucked into chinos for smart-casual occasions. The balanced check pattern and rich navy tones bring instant polish to your seasonal wardrobe while keeping the look approachable and comfortable. Whether you’re dressing for a casual office, coffee with friends, or a weekend outing, this shirt delivers an understated, versatile style that’s ready for the season.",
  "features": [
    "Navy-blue base with white and light-blue check pattern",
    "Classic collar with full button-front closure",
    "Single chest pocket visible on the front",
    "Sleeves shown rolled for a relaxed, casual look",
    "Modern, streamlined silhouette suitable for layering",
    "Versatile fall styling—works with jeans or chinos"
  ],
  "keywords": "men's checked shirt, navy check shirt, Turtle Check shirt, men's casual shirt, plaid shirt men, navy blue shirt men, button-front shirt, long sleeve checked shirt, fall casual shirt, men's shirt with pocket, checked button shirt, men's fall wardrobe, casual men's shirts, modern checked shirt"
}
````

### Final Output (formatted):
**Title:** Turtle Check Men's Navy Blue Checked Shirt

**Features:**
- Navy-blue base with white and light-blue check pattern
- Classic collar with full button-front closure
- Single chest pocket visible on the front
- Sleeves shown rolled for a relaxed, casual look
- Modern, streamlined silhouette suitable for layering
- Versatile fall styling—works with jeans or chinos

**Batch result:** 20/20 products processed successfully in 307 seconds (31,076 tokens in total).

## Error Handling
 Errors are caught per product, so one failing product does not stop the batch. To demonstarte this I ran the pipeline with one product whose image files does not exist: 
 - [1/2] BROKEN TEST PRODUCT (missing image) ... ✗ FileNotFoundError
 - [2/2] Peter England Men Party Blue Jeans ... ✓
## Limitation
- the dataset images are only about 60x80 pixels which makes it difficult to see detailed attributes but the model started to hallucinate and described details which I could not recognize myself 
- it already took about 5 minutes to go through 20 products; if you have to go through multiple hundreds or thousands it will take a long time 