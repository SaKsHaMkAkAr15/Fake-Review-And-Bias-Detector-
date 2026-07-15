# Fake Review & Bias Detector 🔍
A web application that analyzes product reviews from Amazon, Flipkart 
or Google and detects how trustworthy they are using Natural Language 
Processing and a custom trust scoring algorithm.

## Working of the App
- Analyzes subjectivity — fake reviews are highly opinionated
- Detects product feature mentions — real reviews mention actual 
  product parts like battery, screen, camera etc.
- Calculates a Trust Score from 0-100
- Shows verdict — Trustworthy, Slightly Biased or Potential Fake

## Features of the app
- Trust Score with animated progress bar
- Color coded verdict card (green/orange/red)
- Polarity and subjectivity analysis
- Product feature keyword detection
- Key phrase extraction using noun phrases
- Cyber themed dark professional UI

## What I Got to Learn
- NLP with TextBlob
- Sentiment and subjectivity analysis
- Noun phrase extraction
- Building web apps with Streamlit
- Custom scoring algorithm design
- Advanced CSS in Streamlit

## Steps to run
1. Make sure Python is installed
2. Install required libraries:
pip install streamlit textblob
python -m textblob.download_corpora
3. Run this command:
streamlit run app.py
4. App opens automatically in your browser

## Tech used
- Python
- TextBlob
- Streamlit
- Custom CSS
