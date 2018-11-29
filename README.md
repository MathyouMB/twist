# Twist
To run this script, you will need to install the Python Tweepy module and create a twitter app. 
You will need to add your app's tokens and keys, and change 'LIST ID' on line 68 to the id of your desired twitter list.

To use this twitter app, make sure you generate consumer and access keys

```python
 def __init__(self):
        #Access tokens are under a test account
        #Creat a twitter appliction here 'https://apps.twitter.com/' and get your own access keys
        self.consumer_key='' 
        self.consumer_secret=''
        self.access_token=''
        self.access_token_secret=''
        self.api = self.authenticate()
```