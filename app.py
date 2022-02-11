from flask import Flask, render_template, flash, request, url_for, redirect, session
#from matplotlib.pyplot import text
import numpy as np
import pandas as pd
import re

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
app = Flask(__name__)


def init():
    global model
    # load the pre-trained Keras model
    #model = load_model('sentiment_analysis.h5')

#########################Code for Sentiment Analysis
@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template("index.html")

@app.route('/sentiment_analysis_prediction', methods = ['POST', "GET"])
def sent_anly_prediction():
    if request.method=='POST':
        url = request.form['text']
        print(url)
        from selenium import webdriver
        from time import sleep
        from selenium.webdriver.chrome.options import Options
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        #driver = webdriver.Chrome(chromedriver, chrome_options=options)
        #driver = webdriver.Chrome(options=options)
        driver=webdriver.Chrome("chromedriver")
        driver.get(url)
        sleep(2)
        text=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[4]/div/div[3]/div[3]/div[2]/span[2]").text
        print("---------------------------------------------------------------------------------")
        
        print(text)
        print("---------------------------------------------------------------------------------")
        analyzer = SentimentIntensityAnalyzer()
        # function to calculate vader sentiment
        
        
            # Create a SentimentIntensityAnalyzer object.
        sid_obj = SentimentIntensityAnalyzer()

        sentiment_dict = sid_obj.polarity_scores(text)
        print("Overall sentiment dictionary is : ", sentiment_dict)
        print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
        print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
        print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
        
        # decide sentiment as positive, negative and neutral
        if sentiment_dict['compound'] >= 0.05 :
            sentiment='Positive'
        elif sentiment_dict['compound'] <= - 0.05 :
            sentiment='Negative'
        else :
            sentiment='Neutral'
            
        print("___________________-")
        print(sentiment)
        
    #return render_template('index.html', text=text,sentiment=sentiment)
    return render_template('index.html', prediction_text="Review is  {}".format(sentiment))

#########################Code for Sentiment Analysis

if __name__ == "__main__":
    init()
    app.run()
