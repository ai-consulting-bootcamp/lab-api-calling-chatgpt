# API Calling to ChatGPT — Lab Report

## 1. How It Works

I built a Python program that automatically generates e-commerce product listings using the OpenAI API.

The program loads product images and metadata from a Hugging Face dataset, converts images into Base64 format, and sends them to the `gpt-4o-mini` model.

The model generates product titles, descriptions, features, and SEO keywords. The results are saved in a JSON file.

## 2. Challenges

I encountered several challenges:

- Installing missing Python libraries, including `datasets`, `Pillow`, and `python-dotenv`.
- Working with different Python environments.
- Generating product descriptions that meet the required word count.

I also tested error handling for missing images and invalid JSON.

## 3. Results and Quality

The program successfully generated listings for three products with no failed API requests.

The descriptions were relevant to the products, but some were shorter than the required 150–200 words.

## 4. Future Improvements

- Automatically check and improve description length.
- Add stronger validation of product information.
- Improve consistency and accuracy of generated content.
- Track API usage and costs.

## Conclusion

This lab helped me understand how to integrate image analysis, prompt engineering, API calls, and error handling into an automated workflow.