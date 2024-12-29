from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://sasanksaimanda:Sasank%40123@cluster0.n3cyl.mongodb.net/portfolio_db?retryWrites=true&w=majority")
db = client['portfolio_db']
queries_collection = db['queries']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    if name and email and message:
        queries_collection.insert_one({'name': name, 'email': email, 'message': message})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
