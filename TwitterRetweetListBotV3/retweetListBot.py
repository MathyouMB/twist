import tweepy
import datetime
from time import sleep as original_sleep
from time import gmtime, strftime
from datetime import datetime, timedelta
from random import gauss
import random

#25/07/2017
#Twitter List Retweet Bot
#This bot retweets the posts of a specified user's twitter list. 

class Bot:
   
    def __init__(self):
        #Access tokens are under a test account
        #Creat a twitter appliction here 'https://apps.twitter.com/' and get your own access keys
        self.consumer_key='' 
        self.consumer_secret=''
        self.access_token=''
        self.access_token_secret=''
        self.api = self.authenticate()

    def randomize_time(self,mean):
        #To appear less bot like, i've turned the cooldown into a bellcurve
        #This means what ever you put as the parameter is the highest value on the curve
        #Sleep picks a value on this curve as the time value, meaning you never get the same time value again and again.
        
        allowed_range = mean * 0.5
        stdev = allowed_range / 3  

        t = 0
        while abs(mean - t) > allowed_range:
            t = gauss(mean, stdev)

        return t


    def sleep(self,t):
        #original sleep is 'sleep()' from time module.
        original_sleep(self.randomize_time(t))
         
        
    def authenticate(self):
        #Make sure your account and twitter app exist.
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        
        try:
            api.verify_credentials()
        except:
            print("bot was unable to verify your login.")
        else:
            print("The bot was able to authenticate your login.")
            return api
   
 
    def retweet_priority_list(self):
        #retweets anything posted by users in a given twitter list.
        
        oldIds = open("RetweetedIds.txt",'r')
        ids = oldIds.readlines()
        tweetedAlreadyUser = False 
        oldID = False
        
        #loop through everyone in a certain users list. the list name uses the lists url slug.
        for member in tweepy.Cursor(self.api.list_members, 'LIST ID', 'LIST ID',wait_on_rate_limit = True, wait_on_rate_limit_notify = True).items():
            try: 
                tweetedAlreadyUser = False #reset for each new user, because we havent retweeted that person yet
                CUT = self.api.user_timeline(screen_name = member.screen_name, count = 100, include_rts = False, exclude_replies = True) # current user timeline
                self.sleep(5) #limit server requests
                print("selected user: "+ str(member.screen_name))  #selected a specific user
                for tweet in CUT: #for tweet in current timeline, 
                    try:
                        if tweetedAlreadyUser == False: #if this is the users first tweet in this rotation
                            if ((datetime.now() - tweet.created_at).days) < 0: # if its not old
                               
                                for idline in ids: #looks through the file with old ids
                                    if (int(tweet.id)) == (int(idline)): #if id is already used
                                        oldID = True #then it must be an old ID
                                        break #break out of the loop because you know its used
                                    else:
                                        oldID = False #if it never hit the ID then it hasnt been used before
                                        continue #continue loop incase its still in the file
                               
                                #after its been through the loop you know if its old or not      
                                if oldID == False: #if its new
                                    try:
                                        writeUsedID = open("RetweetedIds.txt",'a')
                                        writeUsedID.write(str(tweet.id)+"\n") #write the ID to the file
                                        print("wrote ID") #wrote ID text
                                        tweet.retweet()  #retweet
                                        print("retweeted "+(str(tweet.id))) #retweeted text
                                        tweetedAlreadyUser = True #this user has retweeted, switch to next
                                        self.sleep(90) #wait a bit to ensure you dont break twitter request limit
                                    except tweepy.TweepError as e:
                                        print(e.reason)
                                        if "185" in e.reason:
                                            break     
                        else:
                           #Code used to save leftover tweets to another txt file but thats no longer required
                           #tweetlater = open("tweetLater.txt",'a')
                           #tweetlater.write(str(tweet.id)+"\n")#write the ID to the file
                           print("will retweet later: " +str(tweet.id)) 
                                 
                    except tweepy.TweepError as e:
                        print(e.reason)
                        continue
                    except StopIteration:
                        break
            
            except tweepy.TweepError as e:
                print(e.reason)
                continue
            except StopIteration:
                break

    #The following is not needed to the new way the original method works
    #retweet_priority_list now skips to the net user after one tweet and therefore we no need this stuff
 ##################################################################              
    def retweet_leftovers(self):
        self.shuffle_tweets()
             
    def shuffle_tweets(self):
        lines = open("tweetlater.txt",'r')
        tweetshuffle = []
        for id in lines:
            tweetshuffle.extend(id)
            print(tweetshuffle[id])
            
        random.shuffle(tweetshuffle)
        print("doneshuffle")
        self.tweet_saved(tweetshuffle)
    
    def tweet_saved(self,tweetshuffle):
        print("ok")
        savedtweets = open("tweetlater.txt",'r')
        savedtweets.close()
        
        for id in tweetshuffle:
                try:   
                    print(id)
                    tweet = self.api.get_status(id)
                    print("retweeted "+(str(id)))
                    tweet.retweet()
                    oldIds2 = open("RetweetedIds.txt",'a')
                    oldIds2.write(str(id)+"\n")#write the ID to the file
                    print("wrote ID")
                    self.sleep(25)
                except tweepy.TweepError as e:
                    print(e.reason)
                except StopIteration:
                        break
                        
twitter_bot = Bot()

while True:
    print('------------------------------------------------- '+strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    twitter_bot.retweet_priority_list()
    twitter_bot.sleep(15)
    
    
    
  