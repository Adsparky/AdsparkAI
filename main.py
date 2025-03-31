from flask import Flask, request, render_template
import openai
import os
import base64
import requests
import stripe

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
x_bearer_token = os.getenv("X_BEARER_TOKEN")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe_publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY")

def get_trending_hashtag():
    try:
        if not x_bearer_token:
            print("X_BEARER_TOKEN is not set in environment variables")
            return "#HotDeal"
        headers = {"Authorization": f"Bearer {x_bearer_token}"}
        response = requests.get("https://api.twitter.com/1.1/trends/place.json?id=1", headers=headers)
        response.raise_for_status()
        trends = response.json()
        print(f"X API Response: {trends}")
        if trends and "trends" in trends[0] and trends[0]["trends"]:
            return trends[0]["trends"][0]["name"]
        print("No trends found in response")
        return "#HotDeal"
    except Exception as e:
        print(f"Trend fetch error: {str(e)}")
        static_trends = ["#SpringVibes", "#TechTrend", "#FoodieFinds", "#FitnessGoals"]
        return static_trends[0]

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
        trend = get_trending_hashtag()
        verb = "love" if product == "coffee" else "enjoy"
        cta = "Sip it now!" if category == "drink" else "Grab it now!"
        prompt = f"Write a short punchy ad slogan for {audience} about {product} with no punctuation no special characters no conjunctions"
        response = openai.chat.completions.create(
            model="gmt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=8
        )
        slogan = response.choices[0].message.content.strip().replace("  ", " ")
        ad = f"{audience} {verb} {product}—{slogan} for ${budget}! {trend} {cta}"
        if int(budget) > 20:
            warning = "Tip: Keep it under $20 for max reach!"
        image_prompt = f"A vibrant ad image for {audience} featuring {product}, modern style with a cozy vibe"
        image_response = openai.images.generate(
            model="dall-e-2",
            prompt=image_prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )
        image_data = image_response.data[0].b64_json
    return render_template('index.html', ad=ad, warning=warning, image_data=image_data, audiences=audiences, trend=trend, stripe_publishable_key=stripe_publishable_key)

@app.route('/pay', methods=['POST'])
def pay():
    ad = request.form['ad']
    image_data = request.form['image_data']
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'AdSpark Ad'},
                'unit_amount': 1000,  # $10 in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://vo-adspark-clone.vercel.app/success',
        cancel_url='https://vo-adspark-clone.vercel.app/cancel',
        metadata={'ad': ad, 'image_data': image_data}
    )
    return f'''
        <script src="https://js.stripe.com/v3/"></script>
        <script>
            var stripe = Stripe("{stripe_publishable_key}");
            stripe.redirectToCheckout({{sessionId: "{session.id}"}});
        </script>
    '''

@app.route('/success')
def success():
    return "Payment successful! Your ad is ready to use. Check your email for details."

@app.route('/cancel')
def cancel():
    return "Payment cancelled—try again!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
