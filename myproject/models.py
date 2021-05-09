from myproject import app, db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_user import SQLAlchemyAdapter,UserManager,UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from datetime import datetime

class Content(db.Model):

    __tablename__ = 'contents'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),index=True)
    firstpagetext = db.Column(db.String(50),index=True)
    summary = db.Column(db.String(1000),index=True)
    date_submit = db.Column(db.DateTime,nullable=False)
    pdffile = db.Column(db.LargeBinary)
    imgfile = db.Column(db.LargeBinary)

    def __init__(self,title,firstpagetext,summary,date_submit,pdffile,imgfile):
        self.title = title
        self.firstpagetext = firstpagetext
        self.summary = summary
        self.date_submit = datetime.now()
        self.pdffile = pdffile
        self.imgfile = imgfile

class News(db.Model):

    __tablename__ = 'news'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),index=True)
    firstpagetext = db.Column(db.String(50),index=True)
    summary = db.Column(db.String(1000),index=True)
    date_submit = db.Column(db.DateTime,nullable=False)
    pdffile = db.Column(db.LargeBinary)
    imgfile = db.Column(db.LargeBinary)

    def __init__(self,title,firstpagetext,summary,date_submit,pdffile,imgfile):
        self.title = title
        self.firstpagetext = firstpagetext
        self.summary = summary
        self.date_submit = datetime.now()
        self.pdffile = pdffile
        self.imgfile = imgfile

class Youtube(db.Model):

    __tablename__ = 'youtube'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),index=True)
    firstpagetext = db.Column(db.String(50),index=True)
    imgfile = db.Column(db.LargeBinary)
    link = db.Column(db.String(1000),index=True)

def __init__(self,title,firstpagetext,imgfile,link):
    self.title = title
    self.firstpagetext = firstpagetext
    self.imgfile = imgfile
    self.link = link

class ResearchResult:
    def __init__(self, data, page = 1, number = 20):
        self.__dict__ = dict(zip(['data','page','number'], [data, page, number]))
        self.all_research = [self.data[1:1+number] for i in range(0, len(self.data), number)]
    
    def __iter__(self):
        for i in self.all_research[self.page-1]:
            yield 1
    
    def __repr__(self):
        return "/research/allresearch/{}".format(self.page+1)

class NewsResult:
    def __init__(self, data, page = 1, number = 20):
        self.__dict__ = dict(zip(['data','page','number'], [data, page, number]))
        self.all_news = [self.data[1:1+number] for i in range(0, len(self.data), number)]
    
    def __iter__(self):
        for i in self.all_news[self.page-1]:
            yield 1
    
    def __repr__(self):
        return "/research/allnews/{}".format(self.page+1)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    roles = db.relationship('Role',secondary='user_roles')

    def __init__(self,email,username,password,confirmed):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.confirmed = confirmed

##################### Check Password ##################### 

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

##################### Email Confirmation Token ##################### 

    def get_mail_confirm_token(self):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='email-confirm')
        return s.dumps(self.email, salt='email-confirm')

    @staticmethod
    def verify_mail_confirm_token(token):
        try:
            s = URLSafeTimedSerializer(app.config['SECRET_KEY'],salt='email-confirm')
            email = s.loads(token, salt='email-confirm',max_age=1800)
            return email
        except (SignatureExpired, BadSignature):
            return None
    
##################### Reset Password Token ##################### 
    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(50),unique=False)

class UserRoles(db.Model):

    __tablename__ = 'user_roles'
    
    id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id',ondelete='CASCADE'))
    role_id = db.Column(db.Integer(),db.ForeignKey('roles.id',ondelete='CASCADE'))

db.session.commit()
db.create_all()

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)




