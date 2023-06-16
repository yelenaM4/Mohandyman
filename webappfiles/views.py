from turtle import title
from flask import Blueprint, render_template, request, session, redirect, flash

import mysql.connector
from webappfiles import dbconnect

from datetime import datetime
import os

views = Blueprint('views', __name__)

cur, con = dbconnect.get_connection()
#referring to the default page via the “/” route
@views.route("/")
def home():
    return render_template("index.html")

@views.route("/houseowner/")
def houseowner():
    return render_template("houseowner.html")



@views.route("/login/")
def login():
    return render_template("login.html")

@views.route("/loginho/")
def loginho():
    return render_template("loginho.html")

@views.route("/signup/")
def signup():
    return render_template("signup.html")

@views.route("/viewjobs/")
def viewjobs():
    cur.execute("SELECT * FROM tbljob")
    rows = cur.fetchall()
    return render_template("viewjobs.html", rows = rows)

@views.route("/adminhome/")
def adminhome():
    return render_template("adminhome.html")



@views.route("/addjob/")
def add_job():

    cur.execute("select* from tbldistrict")
    rows1=cur.fetchall()
    return render_template("addjob.html",rows1=rows1)




@views.route("/savedetails", methods = ["POST"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            # add codes to retrieve the form values
            title = request.form["txttitle"]
            salary = request.form["txtsal"]
            ref = request.form["txtref"]
            desr = request.form["txtdesc"]
            dt = request.form["txtcdate"]
            ho= request.form["txtho"]
            f = request.files["filecover"]
            f.save(os.path.join("./webappfiles/static/images" , f.filename))
            full_filename = os.path.join("/static/images" , f.filename)
            sql = "INSERT into tbljob (JOB_TITLE, SALARY, JOB_REFERENCE, JOD_DESCRIPTION, CLOSING_DATE, HOUSEOWNER, JOB_COVER) values (%s,%s,%s,%s,%s,%s,%s)"
            # add the form variables for each column
            val = (title,salary,ref,desr,dt, ho,full_filename)
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " job added"
        except Exception as e:
            con.rollback()
            msg = "Job cannot be added " + str(e)
        finally:
            #pass the msg variable to the return statement
            return render_template("addjob.html",msg=msg, title=title)
            con.close()


@views.route("/joblisting/")
def job_listing():
    cur, con = dbconnect.get_connection()
    cur.execute("SELECT * FROM tbljob")
    rows = cur.fetchall()
    return render_template('joblisting.html', rows=rows)

@views.route("/searchjob/")
def search_job():
    return render_template("search.html")

@views.route("/searchjb/", methods = ["GET"])
def searchjob():
    #retrieve the querystring txtlang from the URL
    title = request.args.get("txtjob")
    try:
        sql = "select * from tbljob  WHERE JOB_TITLE = %s "
        val = (title,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        msg = str(cur.rowcount) + " record found!"
    except:
        msg = "There was an issue while searching!"
    finally:
        return render_template("search.html", rows=rows,msg = msg, title=title) 


@views.route("/updatejob/")
def update_job():
    return render_template("updatejob.html")


@views.route("/updaterecord/", methods = ["POST"])
def updaterecord():
    #retrieve the form values
    salary = request.form["txtsalary"]
    title = request.form["txttitle"]
    try:
        sql = "UPDATE tbljob SET SALARY = %s where JOB_TITLE = %s"
        val = (salary, title)
        cur.execute(sql, val)
        con.commit()
        msg = str(cur.rowcount) + " record successfully updated"
    except:
        msg = "Cannot be updated"
    finally:
        return render_template("updatejob.html", msg = msg)



@views.route("/profile/")
def profile():
    if 'ID' in session:
        cur, con = dbconnect.get_connection()
        sql = "SELECT * FROM tblhousekeeper where ID = %s"
        val = (session.get('ID'),)
        cur.execute(sql, val)
        rows = cur.fetchall()
        return render_template('profile.html', rows=rows)
    else:
        return redirect('/')


@views.route("/profileho/")
def profileho():
    if 'ID' in session:
        cur, con = dbconnect.get_connection()
        sql = "SELECT * FROM tblhouseowner where ID = %s"
        val = (session.get('ID'),)
        cur.execute(sql, val)
        rows = cur.fetchall()
        return render_template('profileho.html', rows=rows)
    else:
        return redirect('/')

@views.route("/updateprofile/", methods=["GET", "POST"])
def update_profile():
    if request.method == "POST":
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        contactnum = request.form['txtcontactnum']
        try:
            cur, con = dbconnect.get_connection()
            sql = "UPDATE tblhousekeeper SET EMAIL = %s, FNAME = %s, LNAME = %s , CONTACT_NUMBER = %s where ID = %s"
            val = (email, first_name, last_name, contactnum, session['ID'])
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " record successfully updated"
            flash(msg, category='success')
        except:
            msg = "Cannot be updated"
            flash(msg, category='error')
        finally:
            return redirect('/profile/')
    else:
        return redirect('/login/')


@views.route("/updateprofileho/", methods=["GET", "POST"])
def update_profileho():
    if request.method == "POST":
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
     
        try:
            cur, con = dbconnect.get_connection()
            sql = "UPDATE tblhouseowner SET EMAIL = %s, FNAME = %s, LNAME = %s  where ID = %s"
            val = (email, first_name, last_name, session.get('ID'),)
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " record successfully updated"
            flash(msg, category='success')
        except:
            msg = "Cannot be updated"
            flash(msg, category='error')
        finally:
            return redirect('/profileho/')
    else:
        return redirect('/adminhome/')


@views.route("/housekeeper/")
def housekeeper():
    cur, con = dbconnect.get_connection()
    cur.execute("SELECT * FROM tblskills")
    rows = cur.fetchall()
    return render_template('housekeeper.html', rows=rows)



@views.route("/application/")
def application():
    cur.execute("SELECT * FROM tbljob jb INNER JOIN tblhouseowner ho on (jb.HOUSEOWNER=ho.ID)")
    rows1 = cur.fetchall()
    return render_template("application.html", rows1 = rows1)

@views.route("/submit_app/", methods=['GET', 'POST'])
def submit_app():
    if request.method == 'POST':
        job = request.form['txtjob']
        date = request.form['txtdate']
        sql = "INSERT into tblapplication (DATE_OF_APPLICATION, JOB, HOUSEKEEPER) values (%s,%s,%s)"
        val = (date, job, session.get('ID'))
        cur.execute(sql, val)
        con.commit()
    return render_template("application.html")

@views.route("/searchskill/")
def searchskill():
    return render_template("searchskill.html")

@views.route("/searchsk/", methods = ["GET"])
def searchsk():
#retrieve the querystring txtlang from the URL
    title = request.args.get("txtsk")
    try:
        sql = "select * from tblhousekeeper hk INNER JOIN tblskills sk ON (hk.ID=sk.ID) where SKILL_TYPE = %s"
        val = (title,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        msg = str(cur.rowcount) + " record found!"
    except:
        msg = "There was an issue while searching!"
    finally:
        return render_template("searchskill.html", msg = msg, rows=rows, title = title)