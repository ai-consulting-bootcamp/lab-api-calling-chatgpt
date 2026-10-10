# API Calling to ChatGPT — Automated Product Listing Generator
**Ironhack AI Consulting Bootcamp | Lab Report**

## 1. How the API Integration Works

The objective of this lab was to automate e-commerce product listing creation using Python and the OpenAI API. I used product information and images from a fashion dataset to generate titles, descriptions, features, and SEO keywords with GPT-4o mini.

| Step | Component | Role |
|---|---|---|
| 1 | Python / Pandas | Load and prepare product data, including names, categories, and placeholder prices |
| 2 | Image processing | Save product images and convert them into base64 |
| 3 | Prompt template | Define instructions and the expected JSON structure |
| 4 | OpenAI API | Send product information and images to GPT-4o mini |
| 5 | LLM | Generate product titles, descriptions, features, and keywords |
| 6 | Python / JSON | Parse the responses, process multiple products, and save the results |

The integration successfully generated **five product listings**, saved in `generated_listings.json`.

## 2. Challenges Encountered

The main challenges were related to data preparation and Python integration.

- **Missing columns:** The original dataset did not contain `name`, `price`, or `image_path`. I created these columns, assigned placeholder prices based on product categories, and saved the images locally.
- **Function naming:** The API function initially referenced `encode_image()`, while my existing image encoding function was named `encode_image_to_base64()`. Correcting the function call resolved the error.
- **API initialization:** The OpenAI client was not initialized in the notebook session. I loaded the API key from an environment variable and initialized the client.
- **Error handling:** I tested missing image files, invalid API credentials, and JSON responses containing Markdown formatting. All three tests passed.

These challenges helped me understand how different components depend on each other and how to debug an API-based workflow.

## 3. Quality of the Generated Listings

The five listings were successfully generated in the requested JSON format. Their titles generally matched the original product names, including product types and colours such as navy blue, silver, black, and grey.

However, I identified some limitations. Several titles and descriptions used generic marketing expressions such as "Stylish and Comfortable." The model also generated potentially unsupported claims, including fabric durability, comfort, and size availability.

Although the product information was generally consistent with the dataset, **a complete visual comparison of every generated detail against the product images is still needed**. Successful JSON generation does not guarantee factual accuracy.

## 4. Possible Improvements

- **Multiple images:** Provide front, back, and detail views to improve the model's understanding of each product.
- **Different writing tones:** Adapt prompts for luxury, casual, professional, or other brand styles.
- **Retries and error logging:** Automatically retry temporary API failures and record unsuccessful requests.
- **Stronger validation:** Check required JSON fields, feature counts, keyword counts, and unsupported product claims.
- **Human review:** Introduce an approval step before publishing listings, especially when product information is incomplete.

## 5. Conclusion

This lab demonstrated how Python, image encoding, prompt engineering, and an LLM API can be combined into an automated workflow. I successfully generated and saved five product listings and tested three error-handling scenarios.

My main takeaway is that **technical success is different from business readiness**. Before deploying this solution in an actual e-commerce environment, I would prioritize factual accuracy, output validation, reliability, and human oversight.