from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ResumeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    objective = TextAreaField('Objective', validators=[DataRequired()])
    education = TextAreaField('Education', validators=[DataRequired()])
    experience = TextAreaField('Experience', validators=[DataRequired()])
    skills = TextAreaField('Skills', validators=[DataRequired()])
    submit = SubmitField('Submit')