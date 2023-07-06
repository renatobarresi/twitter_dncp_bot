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
    def __init__(self, consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken):
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
        self.bearerToken = bearerToken

    def __str__(self):
        return f"twitterBot object with consumer key {self.consumerKey}, consumer secret {self.consumerSecret}, access token {self.accessToken}, and access token secret {self.accessTokenSecret}"

    '''
        oauth 1.0
        retorna puntero a objeto API creado
    '''
    def oauth(self):
        """
        Returns a pointer to a Client object created using the consumer key, consumer secret, access token, and access token secret, as well as the bearer token, of the `twitterBot` object.
        
        Returns:
        - tweepy.Client: The Client object.
        """

        try:
            client = tweepy.Client(
                bearer_token=self.bearerToken,  # Use the bearer token for app-only authentication
                consumer_key=self.consumerKey,
                consumer_secret=self.consumerSecret,
                access_token=self.accessToken,
                access_token_secret=self.accessTokenSecret
            )
            
            return client

        except Exception as e:
            print(e)
            return None

    def tweet(self, client, msg, reply_to_id=None, user_auth=True):
        """
        Tweets the given message using the given Client object. If `reply_to_id` is not None, the tweet is a reply to the tweet with the given ID.
        
        Parameters:
        - client (tweepy.Client): The Client object to use for tweeting.
        - msg (str): The message to tweet.
        - reply_to_id (str): The ID of the tweet to reply to. If None, the tweet is not a reply.
        - user_auth (bool): Whether or not to use OAuth 1.0a User Context to authenticate.
        
        Returns:
        - int: The ID of the last tweet sent.
        """
        
        # Validate input
        if client is None:
            print("Error: Client object is None")
            return reply_to_id
        if len(msg) == 0 or len(msg) > 280:
            print("Error: Invalid tweet message")
            return reply_to_id
        
        try:
            # Just Tweet
            if reply_to_id is None:
                response = client.create_tweet(text=msg, user_auth=user_auth)
            # Reply to a tweet
            else:
                response = client.create_tweet(text=msg, in_reply_to_tweet_id=reply_to_id, user_auth=user_auth)
            
            reply_to_id = response.data['id']

            print("Tweeted!")

        except Exception as error:
            error_type = type(error).__name__
            error_message = str(error)
            print("An exception occurred:")
            print("Error Type:", error_type)
            print("Error Message:", error_message)
            
        return reply_to_id