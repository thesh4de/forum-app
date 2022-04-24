from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import json

# This file contains all the databases.
def createDb(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/data.db"
    app.config["SECRET_KEY"] = "hard to guess thing"
    db = SQLAlchemy(app)

    # Create the tables
    class Topic(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.Text)
        content = db.Column(db.Text)
        filname = db.Column(db.Text)
        fil = db.Column(db.LargeBinary)
        date = db.Column(db.Text)
        lastActivity = db.Column(db.Text)
        author = db.Column(db.Text)
        category = db.Column(db.Text)
        private = db.Column(db.Boolean)
        likes = db.Column(db.Text)
        replies = db.Column(db.Text)

        # Numbers
        likesNum = db.Column(db.Integer)
        repliesNum = db.Column(db.Integer)
        views = db.Column(db.Integer)

        def __init__(self, title, content, date, author, category, filname, fil, private=False):
            self.title = title
            self.content = content
            self.filname = filname
            self.fil = fil
            self.date = date
            self.author = author
            self.category = category
            self.private = private
            self.likesNum = 0
            self.repliesNum = 0
            self.views = 0
            self.likes = "[]"
            self.lastActivity = date

        # Create like and other def for this thing
        def like(self, username):
            l = json.loads(self.likes)
            if username in l:
                l.remove(username)
                self.likesNum -= 1
                self.likes = json.dumps(l)
            else:
                l.append(username)
                self.likesNum += 1
                self.likes = json.dumps(l)

        def reply(self, date):
            self.lastActivity = date
            self.repliesNum += 1

    class Reply(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.Text)
        filname = db.Column(db.Text)
        fil = db.Column(db.LargeBinary)
        date = db.Column(db.Text)
        author = db.Column(db.Text)
        inReplyTo = db.Column(db.Integer)
        likes = db.Column(db.Text)

        # Adding the numbers
        likesNum = db.Column(db.Integer)

        def __init__(self, content, date, author, inReplyTo, filname, fil):
            self.content = content
            self.date = date
            self.filname = filname
            self.fil = fil
            self.author = author
            self.inReplyTo = inReplyTo
            self.likesNum = 0
            self.likes = "[]"

        def like(self, username):
            l = json.loads(self.likes)
            if username in l:
                l.remove(username)
                self.likesNum -= 1
                self.likes = json.dumps(l)
            else:
                l.append(username)
                self.likesNum += 1
                self.likes = json.dumps(l)

    # Return the data
    return {"db": db, "Topic": Topic, "Reply": Reply}
