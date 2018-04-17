from app import db

# When a person signs up, their information is saved in the database as a "User" class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False) # names and e-mails can repeat, but dates cannot
    email = db.Column(db.String(120), index=True, unique=False)
    date = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self): # helpful print function
        return '<Name {}>'.format(self.name)

