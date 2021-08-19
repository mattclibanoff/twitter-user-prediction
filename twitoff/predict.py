"""Prediction of Users based on Tweet embeddings."""

# Package imports
import numpy as np
import spacy
from sklearn.linear_model import LogisticRegression

# Local imports
from twitoff.models import User


def predict_user(user1_name, user2_name, tweet_text):
    """Determine and returns which user is more likely to say a given Tweet."""
    # SELECT name FROM User WHERE name = <user1_name> LIMIT 1;
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()

    # Embed the tweets using Basilica's functionality
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])

    # X = embeddings
    # y = labels
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.zeros(len(user1.tweets)),
                             np.ones(len(user2.tweets))])

    # Fit a LogisticRegression model on X and y
    log_reg = LogisticRegression().fit(embeddings, labels)

    # Embed the tweet_text using SpaCy vectorizer to use with predictive model
    nlp = spacy.load('twitoff/my_model')
    tweet_embedding = nlp(tweet_text).vector

    # Return the predicted label
    # [0.] = user1  //  [1.] = user2
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
