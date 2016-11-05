import praw
import yaml
import pymongo

def main():
    # params retunrns a dict with our info
    params = get_secrets()

    db = get_database()
    comments = db.comments

    print(params)
    r = connect_to_reddit(params)
    r.login()

    main_loop(r, db)

def main_loop(r, db):
    while True:
        subreddit = r.subreddit('overwatch')
        for comment in subreddit.stream.comments(r):
            if matches_response(comment):
                insert_comment(db.comment, comment)
                print("Added response")


def matches_response(comment):
    return False

def get_secrets():
    f = open("secrets.yaml")
    params = yaml.load(f)
    return params

def connect_to_reddit(params):
    return praw.Reddit(
            user_agent=params['user_agent'],
            client_id=params['client_id'],
            client_secret=params['client_secret'],
            username=params['username'],
            password=params['password']
            )

def get_database():
    return pymongo.MongoClient()['reddit-bot']



def insert_comment(db_collection, comment):
    db_collection.insert_one(comment)

def comment_exists(db_collection, query):
    return db_collection.find(query);


if __name__ == '__main__':
    main()
