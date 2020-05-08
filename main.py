import os
import logging

from flask import Flask, render_template, url_for, redirect, request, Response
from forms import PersonForm, SearchForm
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
        medical = request.form.get('medical')


        #   Verifier info
        v_fname = request.form.get('v_fname')
        v_lname = request.form.get('v_lname')
        v_phone = request.form.get('v_phone')
        v_address = request.form.get('v_address')
        v_city = request.form.get('v_city')
        v_state = request.form.get('v_state')
        v_zipcode = request.form.get('v_zipcode')


        #   Shelter History Info
        shelter = request.form.get('shelter')
        date_in = request.form.get('date_in')
        date_out = request.form.get('date_out')

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

        try:
            with db.connect() as conn:
                conn.execute(stmt,Fname=fname,Lname=lname,id=id_num,sex=sex,dob=dob,phone=phone,ethnicity=ethnicity,admission_id=id_num,marital_status=marital_status,med_id=id_num,verifier_id=id_num,history_id=id_num)
                conn.execute(stmt2,verifier_id=id_num, Fname=v_fname, Lname=v_lname, phone=v_phone, Vaddress_id=id_num)
                conn.execute(stmt3, Vaddress_id=id_num, address=v_address, state=v_state, city=v_city, zipcode=v_zipcode)
                if medical != '':
                    conn.execute(stmt5, med_id=id_num,allergy=medical)
                if shelter != '0':
                    conn.execute(stmt4, history_id=id_num, shelterID=shelter, date_in=date_in, date_out=date_out)
        
        except Exception as e:
            logger.exception(e)


        return redirect(url_for('success'))
    return render_template('home.html',form=form)




@app.route('/success',methods=['GET'])
def success():
    return Response(response="Successfully added to database", status=200)





@app.route('/searchid',methods=['GET','POST'])
def search():
    form=SearchForm()
    if form.validate_on_submit():
        id_num = request.form.get('id_num')

        stmt_person = sqlalchemy.text("SELECT * FROM PERSON where id=:id")

        try:
            with db.connect() as conn:
                result = conn.execute(stmt_person, id=id_num).fetchone()

        except Exception as e:
            logger.exception(e)

            return Response(reponse=result, status=200)
    return render_template('searchid./html',form=form)