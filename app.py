from myproject import app,db, mail
from flask import render_template,redirect,request,url_for,flash,abort,send_file
from flask_login import login_user,login_required,logout_user, current_user
from flask_user import roles_required
from flask_mail import Message
from werkzeug.security import generate_password_hash
from myproject.models import User, Role, UserRoles, Content, News, Youtube, ResearchResult, NewsResult
from myproject.forms import LoginForm, RegistrationForm, AdminForm, ContentForm,NewsForm,YoutubeForm,DelForm, RequestResetForm, RequestPasswordForm
from io import BytesIO
from base64 import b64encode
from datetime import datetime

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home')
def home():
    content = Content.query.all()
    news = News.query.all()
    youtube = Youtube.query.all()

    research_image_1 = content[-1].imgfile
    research_image_2 = content[-2].imgfile
    research_image_3 = content[-3].imgfile
    research_image_4 = content[-4].imgfile

    image_research_1 = b64encode(research_image_1).decode('ascii')
    image_research_2 = b64encode(research_image_2).decode('ascii')
    image_research_3 = b64encode(research_image_3).decode('ascii')
    image_research_4 = b64encode(research_image_4).decode('ascii')

    news_image_1 = news[-1].imgfile
    news_image_2 = news[-2].imgfile
    news_image_3 = news[-3].imgfile
    news_image_4 = news[-4].imgfile

    image_news_1 = b64encode(news_image_1).decode('ascii')
    image_news_2 = b64encode(news_image_2).decode('ascii')
    image_news_3 = b64encode(news_image_3).decode('ascii')
    image_news_4 = b64encode(news_image_4).decode('ascii')

    youtube_image_1 = youtube[-1].imgfile
    youtube_image_2 = youtube[-2].imgfile
    youtube_image_3 = youtube[-3].imgfile

    image_youtube_1 = b64encode(youtube_image_1).decode('ascii')
    image_youtube_2 = b64encode(youtube_image_2).decode('ascii')
    image_youtube_3 = b64encode(youtube_image_3).decode('ascii')

    return render_template('home.html', content=content, news=news, youtube=youtube, 
    image_research_1=image_research_1, image_research_2=image_research_2, image_research_3=image_research_3, image_research_4=image_research_4,
    image_news_1=image_news_1, image_news_2=image_news_2, image_news_3=image_news_3, image_news_4=image_news_4,
    image_youtube_1=image_youtube_1, image_youtube_2=image_youtube_2, image_youtube_3=image_youtube_3)

@app.route('/about-us')
@login_required
def about_us():
    return render_template('about_us.html')

@app.route('/subscription')
@login_required
def subscription():
    return render_template('subscription.html')

@app.route('/policy')
@login_required
def policy():
    return render_template('policy.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

################## User Login ##################
@app.route('/welcome')
@login_required
def welcome_user():
    flash('Logged in Successfully!')
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('unconfirmed')

            return redirect(next)
            
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data,confirmed=False)
        user.roles.append(Role(name='Normal'))
        

        db.session.add(user)
        db.session.commit()

        send_mail_confirmation(user)
        flash('Thanks for registering!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

 #################### Confirm Email ############################ 

def send_mail_confirmation(user):
    token = user.get_mail_confirm_token()
    msg = Message('Please Confirm Your Email', sender='vektoresearch@gmail.com', recipients=[user.email])
    msg.body = f'''Dear Client,

To complete your registration, please visit the following link:
{url_for('confirm_email',token=token, _external=True)}

If you did not make this request, please ignore it.
'''
    mail.send(msg)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    email = User.verify_mail_confirm_token(token)
    if email:
        user = db.session.query(User).filter(User.email == email).one_or_none()
        user.confirmed = True

        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    return redirect(url_for('login'))

@app.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('welcome_user'))
    flash('Please confirm your account!')
    return render_template('unconfirmed.html')

@app.route('/resend')
def resend_confirmation():
    token = current_user.get_mail_confirm_token()
    msg = Message('Please Confirm Your Email', sender='vektoresearch@gmail.com', recipients=[current_user.email])
    msg.body = f'''Dear Client,

To complete your registration, please visit the following link:
{url_for('confirm_email',token=token, _external=True)}
'''
    mail.send(msg)
    send_mail_confirmation(current_user)
    flash('A new confirmation has been sent')
    return redirect(url_for('unconfirmed'))

 #################### Reset Password #############################
    
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='vektoresearch@gmail.com', recipients=[user.email])
    msg.body = f'''Dear Client, 
    
To reset your password, please visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, please ignore it.
'''
    mail.send(msg) 

@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title='Reset Password',form=form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token')
        return redirect(url_for('reset_request'))

    form = RequestPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()

        flash('Your password has been updated')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset Password',form=form)

################## Admin Login ##################

@app.route('/admin/content-management')
@login_required
@roles_required('Admin')
def content_management():
    return render_template('content_management.html')

@app.route('/admin/admin-role',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def update_admin_role():

    form = AdminForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(id=form.id.data).first()
        role.id = form.id.data
        role.name = form.name.data
        db.session.commit()
        flash('Your admin role has been updated!')
        return redirect(url_for('home'))
    return render_template('admin_role.html',form=form)

@app.route('/admin/delete/user-database',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def delete_user_database():

    form = AdminForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        user.id = form.id.data
        db.session.delete(user)
        db.session.commit()
        flash('User has been deleted!','success')
        return redirect(url_for('delete_role_database'))
    return render_template('user_database.html',form=form)

@app.route('/admin/delete/role-database',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def delete_role_database():

    form = AdminForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(id=form.id.data).first()
        role.id = form.id.data
        db.session.delete(role)
        db.session.commit()
        flash('Role has been deleted!')
        return redirect(url_for('delete_user_database'))
    return render_template('role_database.html',form=form)

################## Let us write the input for Research! ##################

# Let there be all links of research here!
@app.route('/research/allresearch/<int:pagenum>')
def research_content(pagenum):
    content = Content.query.all()
    return render_template('all_research_content.html', content=content, listing = ResearchResult(content, pagenum))

# Let us redirect the file into one single page
@app.route('/research/<int:page_id>')
def research_page(page_id):
    content = Content.query.get_or_404(page_id)
    return render_template('research_page.html', content=content)   

# Let us see the PDF!
@app.route('/research/upload/<int:page_id>')
def upload_research(page_id):
    content = Content.query.filter_by(id=page_id).first()
    return send_file(BytesIO(content.pdffile), attachment_filename='download.pdf',as_attachment=True) 

# Let us write new research!
@app.route('/research/new',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def new_content_research():

    form = ContentForm()
    if form.validate_on_submit():
        content = Content(title=form.title.data,firstpagetext=form.firstpagetext.data,summary=form.summary.data,date_submit=datetime.now(),pdffile=form.pdffile.data.read(),imgfile=form.imgfile.data.read())

        db.session.add(content)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('input_research.html',form=form) 

# This is for updating the post   
@app.route('/research/update',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def update_research():

    form = ContentForm()
    if form.validate_on_submit():
        content = Content.query.filter_by(id=form.id.data).first()
        content.id = form.id.data
        content.title = form.title.data
        content.firstpagetext = form.firstpagetext.data
        content.summary = form.summary.data
        content.pdffile = form.pdffile.data.read()
        content.imgfile = form.imgfile.data.read()
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update_research.html',form=form)

# This is for deleting the post
@app.route('/research/delete',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def delete_research():
    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        content = Content.query.get(id)
        db.session.delete(content)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('delete_research.html',form=form)

################## Let us write the input for News! ##################

# Let there be all links of news here!
@app.route('/news/allnews/<int:pagenum>')
def news_content(pagenum):
    news = News.query.all()
    return render_template('all_news_content.html', news=news, listing = NewsResult(news, pagenum))

# Let us redirect the file into one single page
@app.route('/news/<int:page_id>')
def news_page(page_id):
    news = News.query.get_or_404(page_id)
    return render_template('news_page.html', news=news)   

# Let us see the PDF!
@app.route('/news/upload/<int:page_id>')
def upload_news(page_id):
    news = News.query.filter_by(id=page_id).first()
    return send_file(BytesIO(news.pdffile), attachment_filename='download.pdf',as_attachment=True) 

# Let us write new news!
@app.route('/news/new',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def new_content_news():

    form = NewsForm()
    if form.validate_on_submit():
        news = News(title=form.title.data,firstpagetext=form.firstpagetext.data,summary=form.summary.data,date_submit=datetime.now(),pdffile=form.pdffile.data.read(),imgfile=form.imgfile.data.read())

        db.session.add(news)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('input_news.html',form=form)

# This is for updating the post   
@app.route('/news/update',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def update_news():

    form = NewsForm()
    if form.validate_on_submit():
        news = News.query.filter_by(id=form.id.data).first()
        news.id = form.id.data
        news.title = form.title.data
        news.firstpagetext = form.firstpagetext.data
        news.summary = form.summary.data
        news.pdffile = form.pdffile.data.read()
        news.imgfile = form.imgfile.data.read()
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update_news.html',form=form)

# This is for deleting the post
@app.route('/news/delete',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def delete_news():
    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        news = News.query.get(id)
        db.session.delete(news)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('delete_news.html',form=form)

################## Let us write the input for Youtube! ##################
# Let us write new youtube!
@app.route('/youtube/new',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def new_content_youtube():

    form = YoutubeForm()
    if form.validate_on_submit():
        youtube = Youtube(title=form.title.data,firstpagetext=form.firstpagetext.data,imgfile=form.imgfile.data.read(),link=form.link.data)

        db.session.add(youtube)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('input_youtube.html',form=form)

# This is for updating the post   
@app.route('/youtube/update',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def update_youtube():

    form = YoutubeForm()
    if form.validate_on_submit():
        youtube = Youtube.query.filter_by(id=form.id.data).first()
        youtube.id = form.id.data
        youtube.title = form.title.data
        youtube.firstpagetext = form.firstpagetext.data
        youtube.imgfile = form.imgfile.data.read()
        youtube.link = form.link.data
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('update_youtube.html',form=form)

# This is for deleting the post
@app.route('/youtube/delete',methods=['GET','POST'])
@login_required
@roles_required('Admin')
def delete_youtube():
    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        youtube = Youtube.query.get(id)
        db.session.delete(youtube)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('delete_youtube.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)