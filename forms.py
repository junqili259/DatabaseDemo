from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, IntegerField, RadioField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

states = [('AL','AL'),('AK','AK'),('AZ','AZ'),('AR','AR'),('CA','CA'),('CO','CO'),('CT','CT'),
('DE','DE'),('DC','DC'),('FL','FL'),('GA','GA'),('HI','HI'),('ID','ID'),('IL','IL'),('IN','IN'),
('IA','IA'),('KS','KS'),('KY','KY'),('LA','LA'),('ME','ME'),('MD','MD'),('MA','MA'),('MI','MI'),
('MN','MN'),('MS','MS'),('MO','MO'),('MT','MT'),('NE','NE'),('NV','NV'),('NH','NH'),('NJ','NJ'),
('NM','NM'),('NY','NY'),('NC','NC'),('ND','ND'),('OH','OH'),('OK','OK'),('OR','OR'),('PA','PA'),
('RI','RI'),('SC','SC'),('SD','SD'),('TN','TN'),('TX','TX'),('UT','UT'),('VT','VT'),('VA','VA'),
('WA','WA'),('WV','WV'),('WI','WI'),('WY','WY'),('PR','PR')]


shelter_choices = [('0','None'),('1','Shelter One'),('2','Shelter Two'),('3','Shelter Three'),('4','Shelter Four'),('5','Shelter Five'),('6','Shelter Six'),('7','Shelter Seven'),('8','Shelter Eight'),('9','Shelter Nine'),('10','Shelter Ten'),
('11','Shelter Eleven'),('12','Shelter Twelve'),('13','Shelter Thirteen'),('14','Shelter Fourteen'),('15','Shelter Fifteen'),('16','Shelter Sixteen'),('17','Shelter Seventeen'),('18','Shelter Eighteen'),('19','Shelter Nineteen'),('20','Shelter Twenty')]

class PersonForm(FlaskForm):
    #   Personal Information
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    id_num = IntegerField('ID number', validators=[DataRequired()])
    sex = RadioField('Sex', choices = [('M','Male'),('F','Female')], validators=[DataRequired()])
    dob = DateField('Date of Birth, format: yyyy-mm-dd, Example: 2000-01-01',format='%Y-%m-%d',validators=[DataRequired()])
    phone = StringField('Phone Number',validators=[Optional()])
    ethnicity = RadioField('Ethnicity',choices=[('American Indian/Alaskan Native','American Indian/Alaskan Native'),('Asian/Pacific Islander','Asian/Pacific Islander'),('Black/African American','Black/African American'),('Hispanic','Hispanic'),('White','White')], validators=[DataRequired()])
    marital_status = RadioField('Marital Status',choices = [('Single','Single'),('Married','Married'),('Widowed','Widowed'),('Divorced','Divorced')], validators=[DataRequired()])

    #   Medical Details
    medical = StringField('Medical Details', validators=[Optional()])


    #   Verifier Information
    v_fname = StringField('Verifier First Name', validators=[DataRequired()])
    v_lname = StringField('Verifier Last Name', validators=[DataRequired()])
    v_phone = StringField('Verifier Phone Number', validators=[DataRequired()])
    v_address = StringField('Verifier Address', validators=[DataRequired()])
    v_city = StringField('Verifier City', validators=[DataRequired()])
    v_state = SelectField('Verifier State', choices=states, validators=[DataRequired()])
    v_zipcode = IntegerField('Verifier Zipcode', validators=[DataRequired()])


    #   Shelter History
    
    shelter = SelectField('Shelter Name', choices=shelter_choices,validators=[DataRequired()])
    date_in = DateField('Date In, format: yyyy-mm-dd, Example: 2000-01-01',format='%Y-%m-%d',validators=[Optional()])
    date_out = DateField('Date Out, format: yyyy-mm-dd, Example: 2000-01-01', format='%Y-%m-%d',validators=[Optional()])
    
    submit = SubmitField('submit')

#   Search data by ID
class SearchForm(FlaskForm):
    id_num = IntegerField('Enter ID', validators=[DataRequired()])
    submit = SubmitField('submit')




                