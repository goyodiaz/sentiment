import streamlit as st
import feedparser
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

@st.experimental_singleton
def download_lexixons():
    nltk.download('vader_lexicon')
    nltk.download('punkt')

# Function to collect RSS feed URLs
def collect_rss_feeds():
    rss_feeds = st.sidebar.text_input("Enter RSS feed URLs (separated by commas):")
    if rss_feeds:
        return rss_feeds.split(",")
    else:
        return []

# Function to collect keywords
def collect_keywords():
    keywords = st.sidebar.text_input("Enter keywords (separated by commas):")
    if keywords:
        return keywords.split(",")
    else:
        return []

# Function to generate word cloud
def generate_wordcloud(text):
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()

# Function to perform sentiment analysis
def sentiment_analysis(text):
    sentiments = []
    
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    sentiments.append(sentiment)
    for sentiment in sentiments:
        return sentiment

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 4)
    summary_str = " ".join([str(sentence) for sentence in summary])
    return summary_str

# Main function
def main():
    st.set_page_config(page_title="RSS Feed Reader", page_icon=":newspaper:", layout="wide")
    download_lexixons()
    st.title("Welcome to the RSS Feed Reader")
    st.markdown("This application allows you to fetch articles from multiple RSS feed URLs, search for keywords in the articles and then view the sentiment analysis, word clouds and summarization of the articles containing the keywords.")
    btn_st=False
    btn_holder= st.empty()
    # Collect RSS feed URLs and keywords using the menu bar
    rss_feeds = collect_rss_feeds()
    keywords = collect_keywords()
    fetch_btn= btn_holder.button("Fetch articles")
    if fetch_btn :
        # Parse RSS feeds and extract articles
        count=0
        print(count)
        st.write("Articles containing keywords:")
        articles = []
        for rss_feed in rss_feeds:
            parsed_feed = feedparser.parse(rss_feed)
            for entry in parsed_feed.entries:
                articles.append(entry.summary)

        # Search for keywords in articles
        keyword_articles = []
        for keyword in keywords:
            for article in articles:
                if keyword in article:
                    keyword_articles.append(article)
        
        st.session_state["keyword_articles"] = keyword_articles

keyword_articles = st.session_state["keyword_articles"]
article_choice= st.selectbox("select", keyword_articles) 

if article_choice:
    summarization_tab,sentiment_tab,wordcloud_tab= st.tabs(["Summarization", "Sentiment Analysis", "Word Cloud"])
    with sentiment_tab:
        st.subheader("Sentiment Analysis")
        sentiment = sentiment_analysis(article_choice)
        st.write(sentiment)
    with wordcloud_tab:
        st.subheader("Word Cloud")
        generate_wordcloud(article_choice)



    with summarization_tab:
        st.subheader("Summarization")
        summary = summarize_text(article_choice)
        st.write(summary)
            

if __name__== "__main__":
    main()
