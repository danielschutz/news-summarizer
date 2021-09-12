from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import requests


def summarize_html(url: str, sentences_count: int, language: str = 'english') -> str:
    """
    Summarizes text from URL
    
    Inputs
    ----------
    url: URL for full text
    sentences_count: specifies max number of sentences for return value
    language: specifies language of text
    
    Return
    ----------
    summary of text from URL
    """
    parser = HtmlParser.from_url(url, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)

    summary = ''
    for sentence in summarizer(parser.document, sentences_count):
        if not summary:
            summary += str(sentence)
        else:
            summary += ' ' + str(sentence)

    return summary


def news_api_request(url: str, **kwargs) -> list:
    """
    Sends GET request to News API endpoint
    
    Inputs
    ----------
    url: full URL for endpoint
    kwargs: please refer to 
            News API documentations: 
            https://newsapi.org/docs/endpoints/
            (apiKey argument is required)
            
    Return
    ----------
    list containing data for each article in response
    """
    params = kwargs
    res = requests.get(url, params=params)
    articles = res.json().get('articles')
    return articles


def summarize_news_api(articles: list, sentences_count: int) -> list:
    """
    summarizes text at URL for each element of articles dict 
    (return value from news_api_request) and adds a new element 
    articles dict where the key is 'summary' and the value is 
    the summarized text
    
    Inputs
    ----------
    articles: list of dict returned from news_api_request()
    sentences_count: specifies max number of sentences for 
                     return value
    
    Return
    ----------
    articles list with summary element added to each dict
    """
    for article in articles:
        summary = summarize_html(article.get('url'), sentences_count)
        article.update({'summary': summary})

    return articles


def search_articles(sentences_count: int, **kwargs) -> list:
    """
    Sends GET request to News API /v2/everything endpoint,
    and summarizes data at each URL
    
    Inputs
    ----------
    sentences_count: specifies max number of sentences 
                     for return value
    kwargs: see News API 
            documentation: 
            https://newsapi.org/docs/endpoints/everything
            
    Return
    ----------
    list where each element is a dict containing info about a single article
    """
    url = 'https://newsapi.org/v2/everything/'
    articles = news_api_request(url, **kwargs)
    return summarize_news_api(articles, sentences_count)


def get_top_headlines(sentences_count: int, **kwargs) -> list:
    """
    Sends GET request to News API /v2/top-headlines endpoint,
    and summarizes data at each URL
    
    Inputs
    ----------
    sentences_count: specifies max number of sentences for return value
    kwargs: see News API 
            documentation: 
            https://newsapi.org/docs/endpoints/top-headlines
    
    Return
    ----------
    list where each element is a dict containing info 
    about a single article
    """
    url = 'https://newsapi.org/v2/top-headlines/'
    articles = news_api_request(url, **kwargs)
    return summarize_news_api(articles, sentences_count)