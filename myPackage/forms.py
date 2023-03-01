from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,validators,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from myPackage.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    
    def validate_username(self,username):
        user = User.query.filter_by(name=username.data).first()
        if User:
            raise ValidationError('Username already exists')
			

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Username already exists')
			


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    # user_id = StringField('User ID', validators=[DataRequired()])
    privacy = SelectField('Privacy', choices=[('Public', 'Public'), ('Friends Only', 'Friends Only'), ('Only Me', 'Only Me')], validators=[DataRequired()])

    submit = SubmitField('Add Post')