# LAB | API Calling to ChatGPT
### Automated Product Listing Generator

---

## 1. What are we building?

You work at an online shop with thousands of products. Writing a description for each one by hand takes hours.

In this lab you build a small program that writes those descriptions automatically:

```
Product image  +  basic info (name, price, category)
                      │
                      ▼
               ChatGPT (gpt-4o-mini)
                      │
                      ▼
   Product listing: title, description, features, SEO keywords
```

---

## 2. The big picture: what happens to one product

| # | What happens | Where | Who does it |
|---|---|---|---|
| 1 | Download product data and images | Hugging Face → your computer | Python (`load_dataset`) |
| 2 | Save each image as a `.jpg` file | Your computer | Python |
| 3 | Convert the image into base64 text | Your computer | Python |
| 4 | Fill name, price and category into a prompt template | Your computer | **You** (Python), not the LLM |
| 5 | Send the prompt and the image to ChatGPT | Internet → OpenAI | The API call |
| 6 | ChatGPT looks at the image, reads the prompt and writes the listing | OpenAI | **The LLM** |
| 7 | Convert the JSON answer to Python and save it to a file | Your computer | Python |

> 💡 The LLM is used **only once**, in step 6. Everything else is ordinary Python.

---

## 3. Two things that confuse everyone (read this first!)

### 🖼️ A) The images

**Does the dataset have images or image paths?**
It has the **actual images**, but **no file paths**.

- Each row has an `image` column that holds the picture as a Python image object (a PIL `Image`).
- `load_dataset(...)` **downloads** the data to your computer, and pandas loads the images into **memory (RAM)**.
- After that, Hugging Face is no longer involved. Everything runs on your machine.

**What is base64, and does ChatGPT read text instead of the image?**
No. Base64 is only a **way to transport** the image.

- An API request is sent as text (JSON), so the image bytes are written as base64 text to fit inside it.
- When the request reaches OpenAI, the base64 is **decoded back into the real image**.
- The vision model then **looks at the pixels**. That's how it can say "navy blue, round neck, white logo".

> 📧 Think of it like sending a photo by email: it travels as encoded text, but the person receiving it sees a picture.

### 💲 B) The price

**The dataset has no prices.** It contains name, category, colour, gender, season and usage, but no price.

**But the prompt template needs a price:**

```python
- Price: ${price:.2f}
```

If the price is missing, this line crashes.

**Our solution:** add a simple **placeholder price** for each main category.

| Category | Placeholder price |
|---|---|
| Apparel | $29.99 |
| Accessories | $24.99 |
| Footwear | $59.99 |
| Personal Care | $14.99 |
| Anything else | $19.99 |

> ⚠️ These prices are **not real**. They only make the template work. Say this in your report.

---

## 4. Before you start: setup

**1. Install the libraries** (once):
```bash
pip install openai datasets pandas pillow
```

**2. Store your API key safely.** Never write it in your code!

In the terminal, **before** you start Jupyter:
```bash
# Mac / Linux
export OPENAI_API_KEY="sk-..."

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-..."
```

Then start Jupyter **from that same terminal**, so it can see the key.

---

## 5. The steps

### Step 1: Connect to OpenAI
- Read the key with `os.getenv("OPENAI_API_KEY")`
- Create the client: `client = OpenAI(api_key=api_key)`

✅ **Checkpoint:** you see `✓ OpenAI client created successfully`

---

### Step 2: Prepare the dataset
- Load the first 100 products from Hugging Face (`ashraq/fashion-product-images-small`)
- Save each image to `product_images/<id>.jpg` → new column `image_path`
- Add the placeholder prices → new column `price`
- Copy `productDisplayName` → new column `name`

**What is the `except` part with `"images/product1.jpg"`?**
It's a **backup plan (Plan B)**. It runs **only if** the Hugging Face download fails, for example with no internet or a blocked network. Then you use **your own photos**:
1. Create an `images/` folder next to your notebook
2. Put your product photos in it
3. Describe each photo in the list (name, price, category, image_path)

If Plan B runs, **skip** the cell that saves images and adds prices. Your own data already has `image_path` and `price`.

✅ **Checkpoint:** `products_df.head()` shows the products, and `product_images/` contains `.jpg` files

---

### Step 3: Encode the image to base64
- Open the image file in binary mode (`"rb"`)
- Convert it with `base64.b64encode(...)`

✅ **Checkpoint:** you see a long string that starts with `/9j/...` (this is how every JPEG starts in base64)

---

### Step 4: Build the prompt
- One function fills the product info into a fixed template
- The template asks ChatGPT for a **title, description, 5–7 features and 10–15 keywords**, **as JSON**

✅ **Checkpoint:** the printed prompt contains the name, price, category and the JSON format

---

### Step 5: Call ChatGPT with the image
Send **one message with two parts**:

```python
"content": [
    {"type": "text",      "text": prompt},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
]
```

Then:
- Take the answer text: `response.choices[0].message.content`
- Remove ```` ```json ```` markers if ChatGPT added them
- Convert the text to a dictionary with `json.loads(...)`

✅ **Checkpoint:** you get a clean listing with `title`, `description`, `features` and `keywords`

---

### Step 6: Process many products
- Loop over 5 products (start small to save credits)
- Wrap each call in `try / except`, so **one failure doesn't stop the loop**
- Wait 1 second between calls with `time.sleep(1)` to avoid rate-limit errors
- Save everything to `generated_listings.json`

✅ **Checkpoint:** the JSON file exists, and the loop finished even if one product failed

---

### Step 7: Show error handling
Run the three small examples in the notebook and take screenshots:

| Example | What you'll see |
|---|---|
| Image file doesn't exist | `FileNotFoundError` is caught with a clear message |
| Fake API key | `AuthenticationError` is caught |
| JSON wrapped in ```` ```json ```` | Fails without cleaning, works after cleaning |

---

## 6. Common problems

| Problem | Fix |
|---|---|
| `API key not found` | Set `OPENAI_API_KEY` in the terminal, then start Jupyter **from that terminal** |
| `Invalid API key` | Check the key has no extra spaces, and that your account has credits |
| `Rate limit exceeded` | Increase `time.sleep(...)` or process fewer products |
| `KeyError: 'image_path'` | You skipped the Step 2 cell that saves the images |
| `JSONDecodeError` | ChatGPT added extra text; check the raw answer and clean it |
| Listings are too generic | Add more details to `additional_info` (colour, gender, usage) |

---

## 7. What to submit

- [ ] Your notebook (`.ipynb`)
- [ ] `generated_listings.json` with **at least 3** listings
- [ ] Screenshots: a successful API call, 3 listings, and the error-handling examples
- [ ] A 1-page report:
  - How the API integration works (use the table in section 2)
  - Challenges you faced (e.g. the image paths and missing prices)
  - Quality of the listings (do the colours and details match the images?)
  - Possible improvements (several images per product, different tones, retries)

> 🔒 **Before submitting:** make sure your API key does not appear anywhere in your files.
