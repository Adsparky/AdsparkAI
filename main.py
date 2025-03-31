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
        <!DOCTYPE html>
        <html>
        <head>
            <title>AdSpark AI</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: 'Poppins', sans-serif;
                    background: #f7f9fc;
                    color: #333;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                header {
                    position: fixed;
                    top: 0;
                    width: 100%;
                    background: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    padding: 15px 20px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                header h1 {
                    color: #2c3e50;
                    font-size: 1.8em;
                    font-weight: 600;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                    max-width: 500px;
                    width: 100%;
                    margin-top: 80px;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                }
                label {
                    font-size: 1em;
                    color: #555;
                }
                input[type="text"] {
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    font-size: 1em;
                    width: 100%;
                    transition: border-color 0.3s;
                }
                input[type="text"]:focus {
                    border-color: #6366f1;
                    outline: none;
                }
                input[type="submit"] {
                    padding: 12px;
                    background: #6366f1;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 1em;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                input[type="submit"]:hover {
                    background: #5455d5;
                }
                p {
                    margin-top: 20px;
                    font-size: 1.1em;
                    font-weight: 600;
                    color: #2c3e50;
                }
                p:last-child {
                    color: #e63946;
                    font-weight: 400;
                }
                footer {
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                    background: #fff;
                    padding: 10px;
                    text-align: center;
                    color: #777;
                    font-size: 0.9em;
                    box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
                }
                footer a {
                    color: #6366f1;
                    text-decoration: none;
                }
                footer a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>AdSpark AI</h1>
            </header>
            <div class="container">
                <form method="POST">
                    <label>Product:</label>
                    <input type="text" name="product" placeholder="e.g., coffee">
                    <label>Audience:</label>
                    <input type="text" name="audience" placeholder="e.g., moms">
                    <label>Budget:</label>
                    <input type="text" name="budget" placeholder="e.g., 10">
                    <label>Category:</label>
                    <input type="text" name="category" placeholder="e.g., drink">
                    <input type="submit" value="Generate Ad">
                </form>
                <p>{{ ad }}</p>
                <p>{{ warning }}</p>
            </div>
            <footer>
                © 2025 AdSpark AI | Built by <a href="https://github.com/Adsparky" target="_blank">Adsparky</a>
            </footer>
        </body>
        </html>
    ''', ad=ad, warning=warning)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
