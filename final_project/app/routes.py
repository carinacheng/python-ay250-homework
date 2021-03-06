from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import SignUpForm
from app.models import User
from app import db
import datetime
import numpy as np
import collections

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
            date = items[ind]['date'] # date that's the closest to now
            date_signup = datetime.date(int(date.split('/')[2]), int(date.split('/')[0]), int(date.split('/')[1])) # in datetime format
            items[ind]['flag'] = True # set flag to True to mark this upcoming date
            if date_signup == now: # if same day, check if it's past noon or not
                if datetime.datetime.now().time().hour >= 12: items[ind]['flag'] = False # it's after noon
    return items


def parse_counts(items):
    """
    Counts up the number of times each person has hosted lunch.
    Input: list of items from parse_db function
    Output: dictionary with keys "names" and values "counts"
    """
    names_in_db = [item['name'] for item in items] # people who have signed up in the database
    counts = {}
    for name in names_in_db: # loop through database entries and match them to the table
        name_entry = name.split(' ') # split up name into first and last, if entered that way
        try: counts[name] += 1 # increase count
        except: counts[name] = 1 # if newcomer isn't in the original list, add them and give a count of 1
    counts = collections.OrderedDict(sorted(counts.items())) # order alphabetically
    return counts


def format_name(name):
    """
    Formats a user-entered name (assuming first and last, separated by a space) in the same standardized way.
    Input: name entry
    Output: name entry with all lower-case except for first letters
    """
    name_entry = name.split(' ') # split first and last name
    ns = [] 
    for n in name_entry:
        n = n.lower() # all lower-case
        n = n.title() # capitalize first letter
        ns.append(n)
    name = ' '.join(ns) # join first and last names back together
    return name


# Main webpage
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SignUpForm() # sign-up form
    items = parse_db(db) # database information
    counts = parse_counts(items) # count information
    if form.validate_on_submit(): # add user to database
        info = User(name=format_name(str(form.name.data)), email=str(form.email.data), date=form.date.data.strftime("%m/%d/%Y"))
        dates = [user.date for user in User.query.all()] # dates already in database
        if info.date in dates: # date already claimed
            flash('This date is already claimed. Please pick another date.') # flash message
            return redirect(url_for('index'))
        db.session.add(info)
        db.session.commit() # add information that's submitted into database
        flash('{}, you are now signed-up to provide lab Friday lunch!'.format(format_name(str(form.name.data)))) # flash a message on the screen
        return redirect(url_for('index')) # return home
    return render_template('index.html', form=form, items=items, counts=counts) # render page

# Instructions page
@app.route('/instructions', methods=['GET'])
def instructions():
    return render_template('instructions.html') # render page
