import json
from flask import url_for, render_template, redirect, make_response, request, session, Response
from flask import current_app as app
from .forms import ContactForm, SignupForm, StatusReport, HiddenButton
from .interactive_fields import Status, ContributeMore, MoreInfo, KeepInTouch, QuestioningEverything
from datetime import datetime as dt
from .utils import get_data_from_json
from .visualization import create_plot
from .openbis import (establish_db_connection, get_all_cases, register_new_case, update_case)

# @app.route('/')
# def home():
#     return render_template('index.html',
#                            template='home-template')

#ID = dt.now().strftime('%c')
#ID = session['_id']
ID = 0000



@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('success.html',
                           template='success-template')


def create_infofile(ID):
    f = open("app/static/{}.json".format(ID),"w+")
    f.write('{}')


def save_info(ID, key, value):
    with open("app/static/{}.json".format(ID), 'r') as file:
        comments = json.load(file)
    comments[key] = value
    with open("app/static/{}.json".format(ID), 'w+') as outfile:
        json.dump(comments, outfile)


@app.route('/status', methods=('GET', 'POST'))
def status():

    form = QuestioningEverything()
    #if form.proof.validate(form):
    if 'proof-proceed' in request.form:
            create_infofile(ID)
            save_info(ID=ID, key="testid", value=form.proof.data['proof'])
            return render_template('status.html',
                                   form=form,
                                   template='form-template',
                                   p="proof_submitted")

    #if form.infection_status.validate(form):
    if 'infection_status-infected' in request.form:
            status = 1
            save_info(ID=ID, key="diagnostic", value=status)
            return render_template('status.html',
                                   form=form,
                                   template='base',
                                   p="proof_submitted",
                                   s="status_registered")
    elif 'infection_status-immune' in request.form:
            status = 2
            save_info(ID=ID, key="diagnostic", value=status)
            return render_template('status.html',
                                   form=form,
                                   template='base',
                                   p="proof_submitted",
                                   s="status_registered")
    elif 'infection_status-non_infected' in request.form:
            status = 0
            save_info(ID=ID, key="diagnostic", value=status)
            return render_template('status.html',
                                   form=form,
                                   template='base',
                                   p="proof_submitted",
                                   s="status_registered")

    #if form.contribution.validate(form):
    if 'contribution-yes' in request.form:
            return render_template('status.html',
                                   form=form,
                                   template='base',
                                   p="proof_submitted",
                                   s="status_registered",
                                   c="contribution_y")
    if 'contribution-no' in request.form:
            return redirect(url_for('success'))

    if 'additional_info-submit' in request.form:
        save_info(ID=ID, key="job", value=form.additional_info.data['job'])
        save_info(ID=ID, key="age", value=int(form.additional_info.data['age']))
        save_info(ID=ID, key="country", value=form.additional_info.data['country'])
        if form.additional_info.data['postcode']:
            save_info(ID=ID, key="zip", value=int(form.additional_info.data['postcode']))
        # return redirect(url_for('success'), perm_id=get_data(ID))
        permID = get_data(ID)
        return redirect(url_for('success', permID=permID))

    return render_template('status.html',
                           form=form,
                           template='base',
                           s="status_not_registered")

@app.route('/geojson-features', methods=['GET'])
def get_all_points():

    d, df = get_data_from_json()
    return Response(d, mimetype='application/json')


@app.route('/visuals')
def visuals():
    _, df = get_data_from_json()
    print(df)
    graphJSON = create_plot(df)
    return render_template('visuals.html',
                           template='signup-template', plot=graphJSON)

@app.route('/%')
def main():
    return render_template('status.html', template='base')

@app.route('/index')
def index():
    return render_template('status.html', template='base')

@app.route('/terms')
def terms():
    return render_template('terms.html', template='base')

@app.route('/faq')
def faq():
    return render_template('faq.html', template='base')


def get_data(ID):
    with open("app/static/{}.json".format(ID), 'r') as file:
        comments = json.load(file)
    o = establish_db_connection()
    perm_id = register_new_case(o=o, data=comments)
    return perm_id



