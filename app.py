from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import string
import requests

import textstat
from collections import Counter

nltk.download('punkt')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


def calculate_metrics(original, summary):
    # Readability score
    readability = textstat.flesch_reading_ease(summary)
    
    # Compression ratio
    compression_ratio = len(summary) / len(original)
    
    # Keyword density
    original_words = clean_text(original).split()
    summary_words = clean_text(summary).split()
    original_word_counts = Counter(original_words)
    summary_word_counts = Counter(summary_words)
    
    significant_words = set(summary_words) - set(textstat.textstat._textstatistics__get_stop_words("english"))
    keyword_density = sum(summary_word_counts[word] for word in significant_words) / len(summary_words)
    
    return readability, compression_ratio, keyword_density
class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    summarized_text = db.Column(db.Text, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    summaries = db.relationship('Summary', backref='user', lazy=True)

with app.app_context():
    db.create_all()


def clean_text(text):
    printable = set(string.printable)
    text = ''.join(filter(lambda x: x in printable, text))
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.-]', '', text)
    text = re.sub(r'\.{2,}', '.', text)
    return text.strip()


def summarize_text(text, ratio=0.33):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")
    num_sentences = int(len(parser.document.sentences) * ratio)
    summary = summarizer(parser.document, num_sentences)
    return ' '.join([str(sentence) for sentence in summary])


# def generate_image(summary):
#     # Placeholder function to simulate image generation
#     # Replace this with actual API call to Google's Imagen 3 when available
#     return "https://via.placeholder.com/400"


def generate_image(summary):

    api_key = 'your_api_key'
    endpoint = 'https://imagen3.googleapis.com/generate_image'
    params = {
        'summary': summary,
        'api_key': api_key
    }
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        image_url = response.json()['image_url']
        return image_url
    else:
        return None


def calculate_metrics(original, summary):
    readability = textstat.flesch_reading_ease(summary)
    compression_ratio = len(summary) / len(original)
    keyword_density = len(set(summary.split())) / len(summary.split())
    return readability, compression_ratio, keyword_density


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('summarize'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('login'))
        except:
            flash('Username already exists. Please try a different username.', 'danger')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if 'user_id' not in session:
        flash('You need to login first.', 'danger')
        return redirect(url_for('login'))
    
    original_article = ""
    summarized_article = ""
    generated_image_url = ""
    readability = 0
    compression_ratio = 0
    keyword_density = 0
    length_option = request.form.get('length_option', 'brief')

    if request.method == 'POST':
        original_article = request.form.get('article', '')
        file = request.files.get('file')
        
        if file:
            original_article = file.read().decode('utf-8')
        
        if original_article:
            original_article = clean_text(original_article)
            ratio = 0.2 if length_option == 'brief' else 0.5
            summarized_article = summarize_text(original_article, ratio)
            generated_image_url = generate_image(summarized_article)
            readability, compression_ratio, keyword_density = calculate_metrics(original_article, summarized_article)
            
            # Debugging print statements
            print(f"Readability: {readability}")
            print(f"Compression Ratio: {compression_ratio}")
            print(f"Keyword Density: {keyword_density}")

    return render_template('summarize.html', 
                           original_article=original_article, 
                           summarized_article=summarized_article, 
                           generated_image_url=generated_image_url,
                           readability=readability,
                           compression_ratio=compression_ratio,
                           keyword_density=keyword_density,
                           length_option=length_option)

@app.route('/my_summaries')
def my_summaries():
    if 'user_id' not in session:
        flash('You need to login first.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    summaries = Summary.query.filter_by(user_id=user_id).all()
    return render_template('my_summaries.html', summaries=summaries)


@app.route('/save_summary', methods=['POST'])
def save_summary():
    if 'user_id' not in session:
        flash('You need to login first.', 'danger')
        return redirect(url_for('login'))

    original_text = request.form.get('original_text')
    summarized_text = request.form.get('summarized_text')
    user_id = session['user_id']
    
    new_summary = Summary(user_id=user_id, original_text=original_text, summarized_text=summarized_text)
    db.session.add(new_summary)
    db.session.commit()
    
    flash('Summary saved successfully!', 'success')
    return redirect(url_for('summarize'))

@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    summary = request.json['summary']
    image_url = generate_image(summary)
    return jsonify(image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
