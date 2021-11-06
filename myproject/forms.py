from flask_wtf import FlaskForm
from myproject.models import User, Content, News, Youtube
from wtforms import StringField,PasswordField,SubmitField, FileField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from wtforms import ValidationError
from wtforms import TextAreaField
from wtforms.widgets import TextArea

##################### User Form #####################
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Login")

    def see_email(self, email):
        if User.query.filter_by(email!=self.email.data).first():
            raise ValidationError('Wrong email!')

    def see_password(self, password):
        if User.query.filter_by(password!=self.password.data).first():
            raise ValidationError('Wrong Password')

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Password must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Sorry, that username is taken!')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email!')

class RequestPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Password must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Reset Password')

##################### Admin Form #####################      
       
class AdminForm(FlaskForm):
    id = StringField('ID Number')
    name = StringField('Name')
    submit = SubmitField('Submit')

##################### Content Management Form #####################
class ContentForm(FlaskForm):
    id = StringField('ID Number')
    title = StringField('Title', widget=TextArea())
    firstpagetext = StringField('First page of the text', widget=TextArea())
    summary = StringField('Summary', widget=TextArea(), id="summernote")
    pdffile = FileField('Upload File')
    imgfile = FileField('Upload Image')
    submit = SubmitField('Submit')

class NewsForm(FlaskForm):
    id = StringField('ID Number')
    title = StringField('Title', widget=TextArea())
    firstpagetext = StringField('First page of the text', widget=TextArea())
    summary = StringField('Summary', widget=TextArea(),id="summernote")
    pdffile = FileField('Upload File')
    imgfile = FileField('Upload Image')
    submit = SubmitField('Submit')

class YoutubeForm(FlaskForm):
    id = StringField('ID Number')
    title = StringField('Title', widget=TextArea())
    firstpagetext = StringField('First page of the text', widget=TextArea())
    imgfile = FileField('Upload Image')
    link = StringField('Youtube Link', widget=TextArea())
    submit = SubmitField('Submit')

class DelForm(FlaskForm):
    id = StringField('ID Number')
    submit = SubmitField('Submit')