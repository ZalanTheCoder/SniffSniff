from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
CORS(app)  # Allow requests from any domain

# Load credentials from environment variables
YOUR_EMAIL = os.environ['YOUR_EMAIL']
YOUR_APP_PASSWORD = os.environ['YOUR_APP_PASSWORD']
RECIPIENT_EMAIL = os.environ['RECIPIENT_EMAIL']

@app.route('/', methods=['GET'])
def home():
    return "✅ IP report backend is running!"

@app.route('/report-ip', methods=['POST'])
def report_ip():
    data = request.json or {}
    ip = data.get('ip', 'Unknown')
    country = data.get('country', 'Unknown')

    msg = EmailMessage()
    msg['Subject'] = "Visitor IP Report"
    msg['From'] = YOUR_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg.set_content(f"Visitor IP: {ip}\nCountry: {country}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(YOUR_EMAIL, YOUR_APP_PASSWORD)
            smtp.send_message(msg)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
