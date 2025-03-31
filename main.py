from flask import Flask, request, render_template_string
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def adspark():
    ad = ""
    warning = ""
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
    return render_template_string('''
        <h1>AdSpark AI</h1>
        <form method="POST">
            Product: <input name="product"><br>
            Audience: <input name="audience"><br>
            Budget: <input name="budget"><br>
            Category: <input name="category"><br>
            <input type="submit" value="Generate Ad">
        </form>
        <p>{{ ad }}</p>
        <p>{{ warning }}</p>
    ''', ad=ad, warning=warning)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
