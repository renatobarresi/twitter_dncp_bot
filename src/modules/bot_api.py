import tweepy
import json

def read_credential(creadentialPath, key):
    """
    Reads the file located at `credentialPath` and retrieves the value for `key` from the file.
    The file is expected to contain a JSON object with the `key` and its corresponding value.

    Parameters:
    - credentialPath (str): The path to the file containing the credentials.
    - key (str): The key whose value should be retrieved from the file.

    Returns:
    - The value associated with the given `key`.
    """
    f = open(creadentialPath)
    data = json.load(f)
    return data[key]

class twitterBot:
    def __init__(self, consumerKey, consumerSecret, accessToken, accessTokenSecret):
        """
        Initializes a `twitterBot` object with the given consumer key, consumer secret, access token, and access token secret.
        
        Parameters:
        - consumerKey (str): The consumer key provided by Twitter.
        - consumerSecret (str): The consumer secret provided by Twitter.
        - accessToken (str): The access token provided by Twitter.
        - accessTokenSecret (str): The access token secret provided by Twitter.
        """
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.accessTokenSecret = accessTokenSecret
        self.accessToken = accessToken

    def __str__(self):
        return f"twitterBot object with consumer key {self.consumerKey}, consumer secret {self.consumerSecret}, access token {self.accessToken}, and access token secret {self.accessTokenSecret}"

    '''
        oauth 1.0
        retorna puntero a objeto API creado
    '''
    def oauth(self):
        """
        Returns a pointer to an API object created using the consumer key, consumer secret, access token, and access token secret of the `twitterBot` object.
        
        Returns:
        - tweepy.API: The API object.
        """

        try:
            auth = tweepy.OAuth1UserHandler(consumer_key = self.consumerKey, 
            consumer_secret = self.consumerSecret, access_token = self.accessToken, 
            access_token_secret = self.accessTokenSecret)
            
            return tweepy.API(auth)

        except Exception as e:
            print(e)
            return None

    def tweet(self, api, msg, id_rsp):
        """
        Tweets the given message using the given API object. If `id_rsp` is not 0, the tweet is a reply to the tweet with the given ID.
        
        Parameters:
        - api (tweepy.API): The API object to use for tweeting.
        - msg (str): The message to tweet.
        - id_rsp (int): The ID of the tweet to reply to. If 0, the tweet is not a reply.
        
        Returns:
        - int: The ID of the last tweet sent.
        """
        
        # Validate input
        if api is None:
            print("Error: API object is None")
            return id_rsp
        if len(msg) == 0 or len(msg) > 280:
            print("Error: Invalid tweet message")
            return id_rsp
       
        try:
            if id_rsp == 0:
                id_rsp = api.update_status(status = msg).id
                print("Tuiteado!")
            else:
                api.update_status(status = msg, in_reply_to_status_id = id_rsp)
                print("Tuiteado!")

        except tweepy.TweepError as error:
            if error.api_code == 187:
                print("Duplicate message")
            if error.api_code == 135:
                print("Timestamp out of bounds")
            else:
                print("There was an exception")
        return id_rsp