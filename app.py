from flask import Flask, render_template, request
import pickle
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

app = Flask(__name__)

# Load the model and vectorizer
with open('fake_news_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'@\w+|\#', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    label = ""
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        combined = preprocess_text(title + " " + text)
        vec_input = vectorizer.transform([combined])
        prediction = model.predict(vec_input)[0]
        
        # Set label based on prediction (1 -> Fake News, 0 -> Real News)
        if prediction == 1:
            label = "Fake News"
        else:
            label = "Real News"

    return render_template('index.html', prediction=label)

if __name__ == '__main__':
    app.run(debug=True)
