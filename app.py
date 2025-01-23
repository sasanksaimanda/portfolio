from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['portfolio_db']
queries_collection = db['queries']

# Function to send email
def send_email(subject, body):
    sender_email = "your-email@gmail.com"
    sender_password = "your-email-password"
    recipient_email = "sasankmanda8@gmail.com"

    # Compose email
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    if name and email and message:
        # Save to MongoDB
        queries_collection.insert_one({'name': name, 'email': email, 'message': message})
        
        # Send email notification
        subject = "New Contact Form Submission"
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        send_email(subject, body)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
