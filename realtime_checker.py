import nltk

# Download punkt tokenizer (required for NLTK's sentence tokenizer)
nltk.download('punkt')

import pickle
from scraper import fetch_article
from vectorizer import preprocess_text

# Load your model and vectorizer
model = pickle.load(open('fake_news_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

def predict_news(news_text):
    cleaned_text = preprocess_text(news_text)
    vect_text = vectorizer.transform([cleaned_text])
    prediction = model.predict(vect_text)[0]
    return 'Fake News' if prediction == 1 else 'Real News'

def main():
    print("📢 Real-time Fake News Checker")
    print("Enter 'URL <url>' to check a news link or 'TEXT <your news>' to check news text directly.")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYour Input: ")
        if user_input.lower() == 'exit':
            break
        
        if user_input.lower().startswith("url "):
            url = user_input[4:].strip()
            article_text = fetch_article(url)
            if article_text:
                result = predict_news(article_text)
                print(f"📰 News from URL is: {result}")
            else:
                print("❌ Failed to fetch or extract article.")
        
        elif user_input.lower().startswith("text "):
            news_text = user_input[5:].strip()
            result = predict_news(news_text)
            print(f"📰 Entered News is: {result}")
        
        else:
            print("❗ Invalid format. Use 'URL <url>' or 'TEXT <news text>'.")

if __name__ == '__main__':
    main()
