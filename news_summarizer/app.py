import os
from app_functions import get_top_headlines, search_articles
import streamlit as st

API_KEY = os.environ['NEWS_API_KEY']

st.title('News Summarizer')

search_choice = st.sidebar.radio('', options=['Top Headlines', 'Search Term'])
sentences_count = st.sidebar.slider('Max sentences per summary:', min_value=1,
                                                                  max_value=10,
                                                                  value=3)

if search_choice == 'Top Headlines':
    category = st.sidebar.selectbox('Search By Category:', options=['business',
                                                            'entertainment',
                                                            'general',
                                                            'health',
                                                            'science',
                                                            'sports',
                                                            'technology'], index=2)

    summaries = get_top_headlines(sentences_count, apiKey=API_KEY,
                                                   sortBy='publishedAt',
                                                   country='us',
                                                   category=category)


elif search_choice == 'Search Term':
    search_term = st.sidebar.text_input('Enter Search Term:')

    if not search_term:
        summaries = []
        st.write('Please enter a search term =)')
    else:
        summaries = search_articles(sentences_count, apiKey=API_KEY,
                                                     sortBy='publishedAt',
                                                     q=search_term)

for i in range(len(summaries)):
    st.title(summaries[i]['title'])
    st.write(f"published at: {summaries[i]['publishedAt']}")
    st.write(f"source: {summaries[i]['source']['name']}")
    st.write(summaries[i]['summary'])
