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

# Viewの処理
columns = [
   "tweet_id",
   "created_at",
   "text",
   "fav",
   "retweets"
   ]

def picked_up():
    messages = [
        "こんにちは、あなたのツイッターのAPIを入力してね",
        "やあ！ツイッターのAPIは何ですか？",
        "あなたのAPIを教えてね"
    ]
    # NumPy の random.choice で配列からランダムに取り出し
    return np.random.choice(messages)

@app.route('/')
def check():
    title = "ようこそ"
    message = picked_up()
    # index.html をレンダリングする
    return render_template('check.html',
                           message=message, title=title)

@app.route('/tweet', methods = ["GET" , "POST"])
def tweet():
    if request.method == 'POST':
        CONSUMER_KEY  = request.form['a']
        CONSUMER_SECRET = request.form['b']
        ACCESS_TOKEN = request.form['c']
        ACCESS_SECRET = request.form['d']
        # #Tweepy
        # auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        # auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        # #グローバル変数
            # global api
        # #APIインスタンスを作成
        # api = tweepy.API(auth)
    # index.html をレンダリングする
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/index', methods = ["GET" , "POST"])
def index():
   if request.method == 'POST':
       query = request.form['query']# formのname = "query"を取得
       cnt = int(request.form['count'])
       button = request.form['button']
       posts = []
       if button == "like":
           posts = like_tweepy(query,cnt,api,posts)
       if button == "retweet":
           tweets_df = retweet_tweepy(query,cnt,api,posts)
       if button == "follow":
           posts = follow_tweepy(query,cnt,api,posts)
       # grouped_df = get_grouped_df(tweets_df)
       # sorted_df = get_sorted_df(tweets_df)
       # 送られてきたものを返すしなきゃ返されない
       return render_template(
           'index.html',
           query = query,
           count = cnt,
           # profile=get_profile(user_id),
           posts = posts
           # grouped_df = grouped_df,
           # sorted_df = sorted_df
           )
   else:
       return render_template('index.html')

def like_tweepy(query,cnt,api,posts):
    search_results = api.search(q=query, count=cnt)
    for tweet in search_results:
        post = {}
        try:
            if not "RT @" in tweet.text: #3
               tweet_id = tweet.id
               api.create_favorite(tweet_id) #ファボする
               post["created_at"] = tweet.created_at
               post["user_id"] = tweet.user.screen_name
               post["text"] = tweet.text.replace('\n','')
               post["fav"] = tweet.favorite_count
               post["retweet"] = tweet.retweet_count
               post["select"] = "いいね"
               posts.append(post)
               time.sleep(1)

        except Exception as e:
            print(e)

    return posts

def follow_tweepy(query,cnt,api,posts):
    search_results = api.search(q=query, count=cnt)
    for tweet in search_results:
        post = {}
        try:
            if not "RT @" in tweet.text: #3
               user_id = tweet.user._json['id']
               api.create_friendship(user_id) #ファボする #ファボする
               post["created_at"] = tweet.created_at
               post["user_id"] = tweet.user.screen_name
               post["text"] = tweet.text.replace('\n','')
               post["fav"] = tweet.favorite_count
               post["retweet"] = tweet.retweet_count
               post["select"] = "フォロー"
               posts.append(post)
               time.sleep(1)

        except Exception as e:
            print(e)

    return posts

def retweet_tweepy(query,cnt,api,posts):
    search_results = api.search(q=query, count=cnt)
    for tweet in search_results:
        post = {}
        try:
            if not "RT @" in tweet.text: #3
               tweet_id = tweet.id
               api.retweet(tweet_id) #ファボする
               post["created_at"] = tweet.created_at
               post["user_id"] = tweet.user.screen_name
               post["text"] = tweet.text.replace('\n','')
               post["fav"] = tweet.favorite_count
               post["retweet"] = tweet.retweet_count
               post["select"] = "リツイート"
               posts.append(post)
               time.sleep(1)

        except Exception as e:
            print(e)

    return posts

def get_profile(user_id):
   user = api.get_user(screen_name= user_id) #1
   profile = { #2
       "id": user.id,
       "user_id": user_id,
       "image": user.profile_image_url,
       "description": user.description # 自己紹介文の取得
   }
   return profile #3

def get_grouped_df(tweets_df):
   grouped_df = tweets_df.groupby(tweets_df.created_at.dt.date).sum().sort_values(by="created_at", ascending=False)
   return grouped_df

def get_sorted_df(tweets_df):
   sorted_df = tweets_df.sort_values(by="retweets", ascending=False)
   return sorted_df

if __name__ == '__main__':
  app.run(host="localhost")
