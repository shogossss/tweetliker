# coding = utf-8
import tweepy,time
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, logging, Response, redirect, flash
from requests_oauthlib import OAuth1Session
import config,json

# 各種ツイッターのキーをセット
CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_SECRET = config.ACCESS_SECRET

#Tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#APIインスタンスを作成
api = tweepy.API(auth)

# Flask の起動
app = Flask(__name__)

def like_tweepy(query,cnt,api):
    search_results = api.search(q=query, count=cnt)
    for tweet in search_results:
        try:
            if not "RT @" in tweet.text: #3
               tweet_id = tweet.id
               api.create_favorite(tweet_id) #ファボする
               time.sleep(1)

        except Exception as e:
            print(e)

    return

query="アニメ"
cnt=5

like_tweepy(query,cnt,api)
