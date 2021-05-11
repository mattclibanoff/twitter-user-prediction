# Twit-Off
A Flask web application which aims to predict, between two Twitter users, who is more likely to post a given Tweet.

## Tech Stack
---
This application is primarily written in *Python 3.8.5* however, the webpages are written with *HTML incorporating Python*.  

*Tweepy* is used in this application (in tandem with developer API access) to connect to the Twitter API to obtain user Tweets.

The microframework used to build this application is *Flask* and eventually, with the help of *Gunicorn*, will be deployed to Heroku.

The database is a *PostgreSQL* instance generated using ElephantSQL.com.

This application also uses *Flask SQLAlchemy* which is an ORM (object-relational-mapper) that assists in the creation of the database and insertion of data via the front-end.

User Tweets are stored as embeddings in the Postgres database and are processed using NLP (Natural Language Processing) with *SpaCy*'s word vectorizer and pre-compiled model.  Formerly, Tweets were embedded using *Basilica* and code can be changed to facilitate this should Basilica.ai become accessible again.

Finally, the model used to predict Twitter users is a simple *Logistic Regression* model from *Scikit Learn*.

## Directory Structure
---
```
├─ twitoff                    → App Directory
│   ├─ my_model/              → Pre-compiled NLP model
│   ├─ templates              → HTML Templates
│   │    ├─ base.html         → Simple about page for application
│   │    ├─ base.html         → Base Webpage
│   │    ├─ prediction.html   → Prediction Page
│   │    └─ user.html         → User Tweets Page
│   │
│   ├─ __init__.py
│   ├─ app.py                 → Main Application
│   ├─ models.py              → SQLAlchemy Model
│   ├─ predict.py             → Logistic Regression Model
│   └─ twitter.py             → Twitter API Authentication
│
├─ .gitignore
├─ LICENSE
├─ Procfile
├─ README.md
├─ TwitOff Application Architecture.pdf
├─ TwitOff Database Entity Relationship Diagram.pdf
├─ requirements.txt
└─ runtime.txt                → Specifies Python version for Heroku
```

## Running the Application (Reproducibility)
---
### Prerequisites
To run this application, you will need Twitter Developer credentials which can be obtained by submitting an application [here](https://developer.twitter.com/en).  Once the application is able to exist on Heroku, I will provide a link in this document.

I would also recommend setting up a free (20 MB) PostgreSQL instance through [ElephantSQL.com](https://www.elephantsql.com/) and obtaining a database URL to use in your `.env` file.

### Spinning up the Flask Application
You will need to create a virtual environment.  For this application, we used *virtualenv*.
    
1. Clone the repository locally using: `git clone https://github.com/JamesBarciz/twitoff-ds16-jjb.git`
2. Create a virtualenv for this project   
3. Activate your environment by running a command that works with your platform [here](https://docs.python.org/3/library/venv.html#creating-virtual-environments).
4. Once in the environment install the dependencies with `pip install -r requirements.txt`.  
    - Side Note: If you do not use the pre-compiled model `my_model` you will need to do two additional steps.
        a. Upgrade SpaCy to the latest version.
        b. Install one of the SpaCy english models.  Accomplish this by running in the terminal:
            - `python -m spacy download en_core_web_lg`
            - If this is causing errors, you will have to go for one of the lesser models [found on SpaCy's website](https://spacy.io/models/en) - simply replace `en_core_web_lg` with `en_core_web_md` or `en_core_web_sm`
3. Create a `.env` file which will house all of your environment variables which is necessary for each of these items (but not limited to) this list... keep in mind running the code as is the variables **must be named exactly as such**:

    - TWITTER_API_KEY
    - TWITTER_API_SECRET
    - DATABASE_URI

4. Depending on your system, you will need to set the Flask application variable in one of two ways.
    
    - Windows: `set FLASK_APP=twitoff:APP`
    - Mac: `export FLASK_APP=twitoff:APP`
    - _Optional:_ You can add `FLASK_APP='twitoff:APP` to your `.env` file to avoid setting these variables each time you enter your environment.

5. Test out your application first by executing `flask shell` which will take you into a Python REPL within your Flask application.  Next, follow these steps to test out your database:

    - `from twitoff.twitter import TWITTER`
    - `from twitoff.models import DB, User, Tweet`
    - `import spacy`
    - ***`DB.drop_all()`* - only perform this if you already created the database
    - `DB.create_all()`
    - `username = 'alyankovic'` - or, another username
    - `twitter_user = TWITTER.get_user(username)`
    - `tweets = twitter_user.timeline(count=200, include_replies=False, include_rts=False`
    - `nlp = spacy.load('my_model')` - remember to replace `my_model` with the proper model if downloaded from SpaCy.io
    - `db_user = User(name=username)` - this will be used to populate the `user` table
    - `for tweet in tweets:`
        - `text = tweet.text`
        - `embedding = list(nlp(text).vector)`
        - `db_tweet = Tweet(id=tweet.id, tweet=text, embedding=embedding)`
        - `db_user.tweets.append(db_tweet)` - this uses the `backref` parameter we set in the `tweet` table
    - `DB.session.add(db_user)` - this will add the user to the `user` table and their Tweets to the `tweet` table
    - `DB.session.commit()` - don't forget to commit!

6. Lastly, connect to your PostgreSQL instance.
- If you generated this through ElephantSQL, follow these directions:
    - Log into ElephantSQL.com
    - Choose the instance name you created
    - On the left dashboard, choose the third option down called `BROWSER`
    - In the SQL Browser, click the `Table queries` drop-down menue, and you should see two tables:
        - `user (public)`
        - `tweet (public)`
    - These are your tables you generated with the ORM *SQLAlchemy*
- If you have a local browser such as [Tableplus](https://tableplus.com/) (free version is fine) you can provide information from your instance dashboard to connect to this instance.

### Post Setup
If this process works, you can open the application locally by running `flask run`
 - you should be provided a link to take you to your local host 
 - copy/paste the link in the web browser, and you should see the application!
 - To view the processes in this application, check out my [Application Architecture map](https://github.com/JamesBarciz/twitoff-ds16-jjb/blob/master/TwitOff%20Application%20Architecture.pdf)

The base route of the application should show you have one user in the database if you followed the prerequisites.  To add another user, type another Twitter username in the text box and click `Add User`.  This could take several minutes because the application is obtaining the last 200 Tweets that user has made.  When the process is complete, you will be directed to the route `/user/<username>` which displays their username in bold as well as the obtained Tweets.  They should now be present in your database!

After adding another user, go back to the base route and click the two Twitter users on the opposite drop-down menues.

Next, to test out the predictive model, copy/paste a Tweet that was made by one of the Twitter users into the text box that says: `"Tweet text to predict"` then, click `Compare Users`

Because we trained the model on the embeddings of both user's Tweets, copy/pasting an exact Tweet should be a 100% match for that user thus, displaying an output in this format:
- `"<PREDICTED_TEXT> is more likely to be said by <USER_A> than <USER_B>"`

As stated before, this model uses *Logistic Regression*.  Similarly to *Linear Regression*, which aims to predict a continuous variable such as stock price or some value, Logistic Regression classifies a prediction to be either True or False - User A or User B respectively.  Rather than give an exact answer User A or User B, Logistic Regression fits a *sigmoid* curve on a graph between 0 and 1.  If the prediction is greater than the threshold (likely >= 0.5), it is True, if less than the threshold, it is False.

For a more-detailed explanation, check out [some notes I took](https://docs.google.com/document/d/1U3GQTPF2JY8DY9y6kqiH2gVc2OuKo888QBdwybhgHW0/edit?usp=sharing) on a [StatQuest video on Logistic Regression](https://www.youtube.com/watch?v=yIYKR4sgzI8)!

## Questions
---
Questions can be directed to my email jamesjbarciz@gmail.com.  I am generally quick to respond depending on work schedule!