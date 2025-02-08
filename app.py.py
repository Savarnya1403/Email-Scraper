from flask import Flask, request, jsonify, render_template
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

# Function to extract emails from a webpage
def extract_emails(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error if request fails
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # Email regex
        emails = list(set(re.findall(email_pattern, text)))  # Remove duplicates
        
        return emails
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    result = extract_emails(url)
    
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 500
    
    return jsonify({'emails': result})

if __name__ == '__main__':
    app.run(debug=True)
