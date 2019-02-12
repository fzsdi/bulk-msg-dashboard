import functools
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import json
import requests
from bulkDashboard.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

url = "http://vas.rpg.ir/api/send/sendSms"

base_dir = os.path.dirname(os.path.realpath(__file__))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/bulkform', methods=('GET', 'POST'))
def bulkform():
    if request.method == 'POST':

        jobId = request.form['jobId']
        m1 = request.form['m1']
        m2 = request.files['m2']
        m3 = request.form['m3']
        l1 = request.files['l1']
        # l2 = request.files['l2']
        db = get_db()
        error = None
        if db.execute(
                'SELECT id FROM jobs WHERE jobName = ?', (jobId,)
        ).fetchone() is not None:
            error = 'Job {} exists.'.format(jobId)

        if error is None:
            db.execute('INSERT INTO jobs (jobName) VALUES (?)', (jobId,))
            db.commit()

            session['namefinal'] = 'numbers' + jobId + '.txt'
            session['namefinalm'] = 'messages' + jobId + '.txt'
            session['nameUrl'] = base_dir + "/" + session['namefinal']
            session['nameUrlm'] = base_dir + "/" + session['namefinalm']

            l1.save(os.path.join(base_dir, session['namefinal']))
            m2.save(os.path.join(base_dir, session['namefinalm']))
            m = open(session['nameUrlm'], 'r')

            # session['messageFinal'] = m1 + " " + m2 + " " + m3

            message = 't'

            payloads = '''------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"sid\"\r\n\r\n39d34a36-ab50-11e8-8129-00505696ce21\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"request\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'''
            replace = []
            dictionary = {'mobileNumber': '9106808434', 'message': message, 'shortCode': '308240'}
            replace.append(dictionary)
            pyas = payloads % json.dumps(replace)
            headers = {
                'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                'authorization': "key=dc8c8671-ab4f-11e8-8129-00505696ce21",
                'cache-control': "no-cache",
                'postman-token': "d395258e-19d1-ec97-fe4b-65eca1ff59cc"
            }
            fullArray = []
            f = open(session['nameUrl'], 'r')
            p = open('logs1.txt', 'w')  # Have to ask
            messageLog = open('MessageLog.txt', 'w')  # Have to ask
            log = open('logTest.txt', 'a')  # Have to ask
            for i, line in enumerate(f):
                    if line is not '\n':
                        dictionary['mobileNumber'] = line.rstrip()
                        session['messageFinal'] = m1 + " " + m[i] + " " + m3
                        dictionary['message'] = session['messageFinal']
                        log.write(json.dumps(dictionary))
                        fullArray.append(dict(dictionary))
                        if len(fullArray) is 100:
                            pyas = payloads % json.dumps(fullArray)
                            response = requests.request("POST", url, data=pyas, headers=headers)
                            p.write(response.text)
                            p.write('\n')
                            messageLog.write(pyas)
                            fullArray = []
            # print(pyas)
            pyas = payloads % json.dumps(fullArray)
            log.close()
            response = requests.request("POST", url, data=pyas, headers=headers)
            # print(response.text)
            p.write(response.text)
            messageLog.write(pyas)

            session.clear()
            return redirect(url_for('auth.bulkform'))

        flash(error)

    return render_template('bulkform.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.bulkform'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
