# ChatGPT API Lab – Product Listing Generator

**Project:** AI Product Listing Generator

## 1. API Integration

In this project, I created a Python program to generate product descriptions for an online store using the OpenAI API.

I used a fashion dataset from Hugging Face and the GPT-4o mini model. The program uses product information and images to create titles, descriptions, features, and SEO keywords.

I also used a `.env` file to keep my API key private. The program saves the results in JSON files and avoids repeating API calls when the files already exist.

## 2. Challenges and Solutions

One of my main challenges was getting descriptions with the correct number of words. Some descriptions were too short.

To solve this problem, I improved my prompts and asked the AI to correct the descriptions.

Another challenge was checking that the results followed the required format. I created a Python function to validate the generated content.

## 3. Quality Evaluation

I tested my program with three products: a shirt, jeans, and a watch.

I checked three requirements:

- Descriptions between 150 and 200 words.
- Between 5 and 7 product features.
- Between 10 and 15 SEO keywords.

All three products passed these checks.

I also tested error handling by simulating a connection error.

## 4. Future Improvements

In the future, I would like to improve the program in three ways:

- Automatically correct descriptions that do not pass validation.
- Generate listings for more products.
- Check that the AI does not include incorrect product information.

## Conclusion

This project helped me understand how to use the OpenAI API with Python. I learned how to create prompts, generate product descriptions, save JSON files, handle errors, and check AI-generated content.

I also learned that AI results need to be reviewed before they are used in a real business.