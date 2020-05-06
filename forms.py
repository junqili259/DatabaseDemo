from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, IntegerField, RadioField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class PersonForm(FlaskForm):
    #   Personal Information
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    id_num = IntegerField('ID number', validators=[DataRequired()])
    sex = RadioField('Sex', choices = [('M','Male'),('F','Female')])
    dob = DateField('Date of Birth',format='%Y-%m-%d',validators=[DataRequired()])
    #dob = StringField('Date of Birth', validators=[DataRequired()])
    phone = StringField('Phone Number')
    ethnicity = RadioField('Ethnicity',choices=[('American Indian/Alaskan Native','American Indian/Alaskan Native'),('Asian/Pacific Islander','Asian/Pacific Islander'),('Black/African American','Black/African American'),('Hispanic','Hispanic'),('White','White')], validators=[DataRequired()])
    marital_status = RadioField('Marital Status',choices = [('Single','Single'),('Married','Married'),('Widowed','Widowed'),('Divorced','Divorced')], validators=[DataRequired()])


    #   Verifier Information
    v_fname = StringField('Verifier First Name', validators=[DataRequired()])
    v_lname = StringField('Verifier Last Name', validators=[DataRequired()])
    v_phone = StringField('Verifier Phone Number', validators=[DataRequired()])
    v_address = StringField('Verifier Address', validators=[DataRequired()])
    v_city = StringField('Verifier City', validators=[DataRequired()])
    v_state = StringField('Verifier State', validators=[DataRequired()])
    v_zipcode = IntegerField('Verifier Zipcode', validators=[DataRequired()])
    submit = SubmitField('submit')


class VerifierForm(FlaskForm):
    v_fname = StringField('First Name', validators=[DataRequired()])
    v_lname = StringField('Last Name', validators=[DataRequired()])
    v_phone = StringField('Phone Number', validators=[DataRequired()])
    v_address = StringField('Address', validators=[DataRequired()])
    v_city = StringField('City', validators=[DataRequired()])
    v_zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    submit = SubmitField('submit')




                