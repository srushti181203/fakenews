from newspaper import Article

def fetch_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()  # Only parse, no NLP
        return article.text
    except Exception as e:
        print(f"Error fetching article: {e}")
        return None
