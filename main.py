import os
import logging

from flask import Flask, render_template, url_for, redirect, request, Response
from forms import PersonForm, SearchForm
from datetime import date,timedelta
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

#   General entry form for user information
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
        medical = request.form.get('medical')


        #   Verifier info
        v_fname = request.form.get('v_fname')
        v_lname = request.form.get('v_lname')
        v_id = request.form.get('v_id')
        v_phone = request.form.get('v_phone')
        v_address = request.form.get('v_address')
        v_city = request.form.get('v_city')
        v_state = request.form.get('v_state')
        v_zipcode = request.form.get('v_zipcode')


        #   Shelter History Info
        shelter = request.form.get('shelter')
        date_in = request.form.get('date_in')
        date_out = request.form.get('date_out')

        plan = request.form.get('plan')

        #   Create the SQL statement

        #   Person info
        stmt = sqlalchemy.text("INSERT INTO Person(Fname,Lname,id,sex,dob,phone,ethnicity,admission_id,marital_status,med_id,verifier_id,history_id)" "VALUES(:Fname,:Lname,:id,:sex,:dob,:phone,:ethnicity,:admission_id,:marital_status,:med_id,:verifier_id,:history_id)")

        #   Verifier Info
        stmt2 = sqlalchemy.text("INSERT INTO Verifier(verifier_id,Fname,Lname,phone,Vaddress_id)" "VALUES(:verifier_id,:Fname,:Lname,:phone,:Vaddress_id)")
        
        #   Verifier Address
        stmt3 = sqlalchemy.text("INSERT INTO VerifierAddress(Vaddress_id, address, state, city, zipcode)" "VALUES(:Vaddress_id, :address, :state, :city, :zipcode)")
        
        #   Shelter History for Person
        stmt4 = sqlalchemy.text("INSERT INTO ShelterHistory(history_id,shelterID,date_in,date_out)" "VALUES(:history_id,:shelterID,:date_in,:date_out)")

        #   Person's medical details
        stmt5 = sqlalchemy.text("INSERT INTO Medical(med_id,allergy)" "VALUES(:med_id,:allergy)")

        #   Free trial or subscription plan
        stmt6 = sqlalchemy.text("INSERT INTO FreeTrial(trial_id,trial_start,trial_end)" "VALUES(:trial_id,:trial_start,:trial_end)")
        stmt7 = sqlalchemy.text("INSERT INTO Subscription(subscription_id, start, end)" "VALUES(:subscription_id, :start, :end)")

        stmt8 = sqlalchemy.text("INSERT INTO Admission(admission_id,trial_id,subscription_id)" "VALUES(:admission_id,:trial_id,:subscription_id)")

        #   To check if verifier data already exist or not
        stmt9 = sqlalchemy.text("SELECT verifier_id FROM Verifier where verifier_id=:verifier_id")

        try:
            with db.connect() as conn:
                conn.execute(stmt,Fname=fname,Lname=lname,id=id_num,sex=sex,dob=dob,phone=phone,ethnicity=ethnicity,admission_id=id_num,marital_status=marital_status,med_id=id_num,verifier_id=v_id,history_id=id_num)
                conn.execute(stmt8,admission_id=id_num,trial_id=id_num,subscription_id=id_num)



                #   Check if Verifier already exists or not
                #   If verifier doesn't exist, enter verifier data into table
                #   else ignore if exists
                verifier_check = conn.execute(stmt9, verifier_id=v_id)
                if verifier_check[0] != '':
                    conn.execute(stmt2,verifier_id=v_id, Fname=v_fname, Lname=v_lname, phone=v_phone, Vaddress_id=v_id)
                    conn.execute(stmt3, Vaddress_id=v_id, address=v_address, state=v_state, city=v_city, zipcode=v_zipcode)

                #   If there are medical details, insert data into table
                if medical != '':
                    conn.execute(stmt5, med_id=id_num,allergy=medical)

                #   If there is shelter history, insert data into table
                if shelter != '0':
                    conn.execute(stmt4, history_id=id_num, shelterID=shelter, date_in=date_in, date_out=date_out)

                #   Add to Free Trial
                if plan == 'F':
                    start_date = date.today()
                    end_date = date.today() + timedelta(7)
                    conn.execute(stmt6,trial_id=id_num, trial_start=start_date, trial_end=end_date)

                #   Add to Subscription
                if plan == 'S':
                    start_date = date.today()
                    end_date = date.today() + timedelta(30)
                    conn.execute(stmt7,subscription_id=id_num, start=start_date, end=end_date)
        
        except Exception as e:
            logger.exception(e)


        return redirect(url_for('success'))
    return render_template('home.html',form=form)




@app.route('/success',methods=['GET'])
def success():
    return Response(response="Successfully added to database", status=200)




#   Get information about person with a certain id
@app.route('/searchid',methods=['GET','POST'])
def search():
    form=SearchForm()
    if form.validate_on_submit():
        med = ''

        # Get User input
        id_num = request.form.get('id_num')

        stmt_person = sqlalchemy.text("SELECT Fname,Lname,sex,dob,ethnicity,marital_status FROM Person where id=:id")
        stmt_medical = sqlalchemy.text("SELECT allergy from Medical where med_id=:med_id")

        try:
            with db.connect() as conn:
                result = conn.execute(stmt_person, id=id_num).fetchone()
                fname = result[0]
                lname = result[1]
                sex = result[2]
                dob = result[3]
                ethnicity = result[4]
                marital = result[5]
                medical_details = conn.execute(stmt_medical,med_id=id_num)
                if medical_details[0] == '':
                    med = "No allergies"
                else:
                    med = medical_details[0]

        except Exception as e:
            logger.exception(e)

        return render_template('result.html', fname=fname,lname=lname,sex=sex,dob=dob,ethnicity=ethnicity,marital=marital,med=med)
    return render_template('searchid.html',form=form)