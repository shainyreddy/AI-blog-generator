from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"

API_TOKEN = "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"
API_URLS = [
    "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
    "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
]

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def generate_blog(topic):
    prompt = f"Write a detailed and well-structured blog post on: '{topic}'. " \
             "The blog should include an introduction, body paragraphs, and a conclusion."

    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }

    for api_url in API_URLS:
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()

            # Ensure the response format is handled correctly
            if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                return result[0]['generated_text']
            else:
                return "Blog generation failed. Try again."
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    return "Failed to generate blog. Please try again."

@app.route('/')
def first_home():
    return render_template('firsthome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username and password:  # Simple authentication (Replace with DB in real cases)
            session['username'] = username
            return redirect(url_for('blog'))
    
    return render_template('login.html')

@app.route('/blog')
def blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form['topic']
    blog_content = generate_blog(topic)
    return jsonify({'blog': blog_content})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('first_home'))

if __name__ == '__main__':  # Corrected the main entry point
    app.run(debug=True)
