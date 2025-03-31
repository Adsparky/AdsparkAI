from flask import Flask, request, render_template
import openai
import os
import base64

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate', methods=['GET', 'POST'])
def adspark():
    ad = ""
    warning = ""
    image_data = ""
    if request.method == 'POST':
        product = request.form['product']
        audience = request.form['audience']
        budget = request.form['budget']
        category = request.form['category']
        trend = "#MomLife" if audience == "moms" else "#HotDeal"
        verb = "love" if product == "coffee" else "enjoy"
        cta = "Sip it now!" if category == "drink" else "Grab it now!"
        prompt = f"Write a short punchy ad slogan for {audience} about {product} with no punctuation no special characters no conjunctions"
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        slogan = response.choices[0].message.content.strip().replace("  ", " ")
        ad = f"{audience} {verb} {product}—{slogan} for ${budget}! {trend} {cta}"
        if int(budget) > 20:
            warning = "Tip: Keep it under $20 for max reach!"
        image_prompt = f"A vibrant ad image for {audience} featuring {product}, simple style"
        image_response = openai.images.generate(
            model="dall-e-2",
            prompt=image_prompt,
            n=1,
            size="512x512",
            response_format="b64_json"
        )
        image_data = image_response.data[0].b64_json
    return render_template('index.html', ad=ad, warning=warning, image_data=image_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
