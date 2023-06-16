from flask_mail import Mail, Message
from . import mail
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector
from webappfiles import dbconnect
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route("/signup/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        password1 = request.form['txtpwd']
        password2 = request.form['txtcpwd']

        cur, con = dbconnect.get_connection()
        sql = "select EMAIL from tblhousekeeper where EMAIL= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        if (count > 0):
            flash('User already exists.', category='error')
        if (len(email) < 5):
            flash('Email must be greater than 4 characters.', category = 'error')
        elif (len(first_name) < 3):
            flash('First name must be greater than 2 characters.', category = 'error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category = 'error')
        elif (len(password1) < 3):
            flash('Password must be at least 3 characters.', category = 'error')
        else:
            passw = generate_password_hash(password1, method='sha256')
            sql2 = "INSERT into tblhousekeeper (EMAIL, FNAME, LNAME, PASSWORD) values (%s,%s,%s,%s)"
            val2 = (email, first_name, last_name, passw)
            cur.execute(sql2, val2)
            con.commit()
            msg = str(cur.rowcount) + " record added, "

            msg1 = Message('Mohandyman store', sender ='yelenamarion@gmail.com', recipients = [email])
            msg1.body = "Welcome to mohandyman store " + first_name + "\r\n"
            msg1.body += "You are now a member and may access the website \r\n "
            msg1.body += "@ http://localhost:5000/"
            mail.send(msg1)

            flash(msg + ' account created!', category='success')
        return redirect(url_for('auth.login'))
    return render_template("signup.html")

@auth.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['txtemail']
        pwd = request.form['txtpwd']
        cur, con = dbconnect.get_connection()
        sql = "select PASSWORD, EMAIL, ID, FNAME from tblhousekeeper where EMAIL= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount
        for row in rows:
            passw = row[0]

        if (count > 0):
            if check_password_hash(passw, pwd):
                session['ID'] = rows[0][2]
                session['FNAME'] = rows[0][3]
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.profile'))
        else:
            flash('Incorrect password, pls try again.', category='error')
    else:
        flash('Email does not exist.', category='error')
    return render_template("login.html")

@auth.route("/loginho/", methods=['GET', 'POST'])
def loginho():
    if request.method == 'POST':
        email = request.form['txtemail']
        pwd = request.form['txtpwd']

        cur, con = dbconnect.get_connection()
        sql = "select PASSWORD, EMAIL, ID, FNAME from tblhouseowner where EMAIL= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount
        for row in rows:
            passw = row[0]

        if (count > 0):
            if check_password_hash(passw, pwd):
                session['ID'] = rows[0][0]
                session['FNAME'] = rows[0][1]
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.adminhome'))
        else:
            flash('Incorrect password, pls try again.', category='error')
    else:
        flash('Email does not exist.', category='error')
    return render_template("loginho.html")

@auth.route("/housekeeper/", methods=['GET', 'POST'])
def housekeeper():
    if request.method == 'POST':
        title= request.form['txttitle']
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        password1 = request.form['txtpwd']
        password2 = request.form['txtcpwd']
        dob= request.form['txtpdate']
        postadd= request.form['txtpostaladd']
        contactnum= request.form['txtcontactnum']
        hqua= request.form['txthqua']
        filecv= request.form['filecv']
        skills= request.form['txtskills']
      

        cur, con = dbconnect.get_connection()
        sql = "select EMAIL from tblhousekeeper where EMAIL= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        if (count > 0):
            flash('User already exists.', category='error')
        if (len(email) < 5):
            flash('Email must be greater than 4 characters.', category = 'error')
        elif (len(first_name) < 3):
            flash('First name must be greater than 2 characters.', category = 'error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category = 'error')
        elif (len(password1) < 3):
            flash('Password must be at least 3 characters.', category = 'error')
        else:
            passw = generate_password_hash(password1, method='sha256')
            sql2 = "INSERT into tblhousekeeper (TITLE, LNAME, FNAME, EMAIL, PASSWORD, DOB, POSTAL_ADDRESS, CONTACT_NUMBER, HIGHEST_QUALIFICATION,  CV_UPLOAD, SKILL_ID) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val2 = (title, first_name, last_name, email, passw, dob, postadd, contactnum, hqua, filecv, skills)
            cur.execute(sql2, val2)
            con.commit()
            msg = str(cur.rowcount) + " record added, "

            msg1 = Message('Mohandyman store', sender ='yelenamarion@gmail.com', recipients = [email])
            msg1.body = "Welcome to mohandyman store " + first_name + "\r\n"
            msg1.body += "You are now a member and may access the website \r\n "
            msg1.body += "@ http://localhost:5000/"
            mail.send(msg1)

            flash(msg + ' account created!', category='success')
        return redirect(url_for('auth.login'))
    return render_template("housekeeper.html")


@auth.route("/houseowner/", methods=['GET', 'POST'])
def houseowner():
    if request.method == 'POST':
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        password1 = request.form['txtpwd']
        password2 = request.form['txtcpwd']
        postadd= request.form['txtpostaladd']
        district= request.form["txtdistrict"]

        cur, con = dbconnect.get_connection()
        sql = "select EMAIL from tblhouseowner where EMAIL= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        if (count > 0):
            flash('User already exists.', category='error')
        if (len(email) < 5):
            flash('Email must be greater than 4 characters.', category = 'error')
        elif (len(first_name) < 3):
            flash('First name must be greater than 2 characters.', category = 'error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category = 'error')
        elif (len(password1) < 3):
            flash('Password must be at least 3 characters.', category = 'error')
        else:
            passw = generate_password_hash(password1, method='sha256')
            sql2 = "INSERT into tblhouseowner (LNAME, FNAME, EMAIL, PASSWORD, POSTAL_ADDRESS, DISTRICT ) values (%s,%s,%s,%s,%s,%s)"
            val2 = (first_name, last_name, email, passw, postadd, district )
            cur.execute(sql2, val2)
            con.commit()
            msg = str(cur.rowcount) + " record added, "

            msg1 = Message('Mohandyman store', sender ='yelenamarion@gmail.com', recipients = [email])
            msg1.body = "Welcome to mohandyman store " + first_name + "\r\n"
            msg1.body += "You are now a member and may access the website \r\n "
            msg1.body += "@ http://localhost:5000/"
            mail.send(msg1)

            flash(msg + ' account created!', category='success')
        return redirect(url_for('auth.loginho'))
    return render_template("houseowner.html")


@auth.route('/logout/')
def logout():
    session.pop('ID')
    return redirect('/')