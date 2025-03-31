from flask import Flask, request, render_template
import openai
import os
import base64
import requests

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
x_bearer_token = os.getenv("X_BEARER_TOKEN")

def get_trending_hashtag():
    try:
        headers = {"Authorization": f"Bearer {x_bearer_token}"}
        response = requests.get("https://api.twitter.com/1.1/trends/place.json?id=1", headers=headers)
        response.raise_for_status()
        trends = response.json()[0]["trends"]
        return trends[0]["name"] if trends else "#HotDeal"
    except Exception as e:
        print(f"Trend fetch error: {e}")
        return "#HotDeal"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate', methods=['GET', 'POST'])
def adspark():
    ad = ""
    warning = ""
    image_data = ""
    audiences = ["moms", "teens", "dads", "students", "gamers", "fitness", "foodies", "travelers"]
    if request.method == 'POST':
        product = request.form['product']
        audience = request.form['audience']
        budget = request.form['budget']
        category = request.form['category']
        trend = get_trending_hashtag()  # Fetch dynamic trend
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
    return render_template('index.html', ad=ad, warning=warning, image_data=image_data, audiences=audiences)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
