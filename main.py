import os
import logging

from flask import Flask, render_template, url_for, redirect, request, Response
from forms import PersonForm, VerifierForm
import requests, random
import sqlalchemy

#   Cloud SQL database 
db_user = os.environ.get("CLOUD_SQL_USERNAME")
db_pass = os.environ.get("CLOUD_SQL_PASSWORD")
db_name = os.environ.get("CLOUD_SQL_DATABASE_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")


app = Flask(__name__)
app.config.from_object('config.Config')

#   Connect to database
db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        database=db_name,
        query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
)

#   For exception handling 
logger = logging.getLogger()


@app.route('/', methods=['GET','POST'])
def home():
    form = PersonForm()
    if form.validate_on_submit():

        #   Get User input
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        id_num = request.form.get('id_num')
        sex = request.form.get('sex')
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        ethnicity = request.form.get('ethnicity')
        marital_status = request.form.get('marital_status')

        #   Create the SQL statement
        stmt = sqlalchemy.text("INSERT INTO Person(Fname,Lname,id,sex,dob,phone,ethnicity,admission_id,marital_status,med_id,verifier_id,history_id)" "VALUES(:Fname,:Lname,:id,:sex,:dob,:phone,:ethnicity,:admission_id,:marital_status,:med_id,:verifier_id,:history_id)")

        try:
            with db.connect() as conn:
                conn.execute(stmt,Fname=fname,Lname=lname,id=id_num,sex=sex,dob=dob,phone=phone,ethnicity=ethnicity,admission_id=id_num,marital_status=marital_status,med_id=id_num,verifier_id=id_num,history_id=id_num)
        
        except Exception as e:
            logger.exception(e)


        return redirect(url_for('verifier'))
    return render_template('home.html',form=form)




@app.route('/verifier',methods=['GET','POST'])
def verifier():
    form = VerifierForm()
    return render_template('verifier.html',form=form)