# Twist - Twitter App

Twist is a Twitter app that retweets the posts of users in a specified twitter user list.

To run this script, you will need to install the Python Tweepy module and create a twitter app. 
```shell
pip install tweepy
python -m pip install tweepy
```
To use this twitter app, make sure you generate consumer and access keys.

```python
 def __init__(self):
        #Access tokens are under a test account
        #Create a twitter application here 'https://apps.twitter.com/' and get your own access keys
        self.consumer_key='' 
        self.consumer_secret=''
        self.access_token=''
        self.access_token_secret=''
        self.api = self.authenticate()
```

You will also have to insert the @ of the user and the url extension of the list to specify which list to pull from.

```python
 for member in tweepy.Cursor(self.api.list_members, 'USERNAME', 'LISTURLEXTENSION',wait_on_rate_limit = True, wait_on_rate_limit_notify = True).items():
```