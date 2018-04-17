from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import SignUpForm
from app.models import User
from app import db
import datetime
import numpy as np

# Function to parse database information
def parse_db(db):
    """ 
    Parses database information into a list that can be read and printed using html.
    Input: database
    Output: list of items (each item is a dictionary containing name, email, date, flag), where flag marks the most recent upcoming lab lunch date
    """
    users = User.query.all()
    items = []
    for u in users:
        item = dict(name=u.name, email=u.email, date=u.date, flag=False)
        items.append(item)

    # Find most recent upcoming lab lunch date
    if len(items) > 0: # loop if there are items
        dates = [item['date'] for item in items] # list of all dates
        now = datetime.date.today() # current date
        diffs = [] # will hold all date differences from current date
        for date in dates: # loop over dates
            date_compare = datetime.date(int(date.split('/')[2]), int(date.split('/')[0]), int(date.split('/')[1])) # date in list
            diffs.append((date_compare-now).days) # difference between date and current date in days
        diffs = np.array(diffs)
        diffs = np.ma.masked_where(diffs < 0, diffs) # mask negative differences (i.e. ignore previous dates)
        if diffs.mask.all() == False: # if there exists a future date 
            ind = np.argmin(diffs) # index of minimum difference - this is the closest upcoming date 
            items[ind]['flag'] = True # set flag to True to mark this upcoming date

    return items


# Main webpage
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SignUpForm() # sign-up form
    items = parse_db(db) # database information
    if form.validate_on_submit(): # add user to database
        info = User(name=str(form.name.data), email=str(form.email.data), date=form.date.data.strftime("%m/%d/%Y"))
        dates = [user.date for user in User.query.all()] # dates already in database
        if info.date in dates: # date already claimed
            flash('This date is already claimed. Please pick another date.') # flash message
            return redirect(url_for('index'))
        db.session.add(info)
        db.session.commit() # add information that's submitted into database
        flash('{}, you are now signed-up to provide lab Friday lunch!'.format(form.name.data)) # flash a message on the screen
        return redirect(url_for('index')) # return home
    return render_template('index.html', form=form, items=items) # render page

# Instructions page
@app.route('/instructions', methods=['GET'])
def instructions():
    return render_template('instructions.html') # render page
