
from flask import render_template,request, redirect, flash, url_for
from .forms import RegistrationForm , LoginForm,PostForm
from myPackage import app,db
from .models import User, Post
from flask_bcrypt import Bcrypt
from flask_login import login_user ,current_user,logout_user,login_required


bcrypt = Bcrypt()




@app.route("/nav")
def nav():
    
    return render_template("layout.html", )

@app.route("/")
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts)

@app.route('/profile')
@login_required
def profile():
    posts = Post.query.filter_by(user=current_user).all()
    return render_template('Profile.html', title='Profile', posts=posts, username=current_user.name)



@app.route("/register", methods=["GET", "POST"])
def register():
    registrationForm = RegistrationForm()
    if request.method == 'POST':
        # get form data
        name = request.form.get('name')
        email = request.form.get('email')
        
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')

        # create a new User object and add it to the database
        with app.app_context():
            user = User(name=name, email=email, password=password)
            db.session.add(user)
            db.session.commit()

        # display success message and redirect to home page
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    # if the request method is GET, display the registration form
    return render_template('register.html')


   



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(name=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
             login_user(user)
             flash('Login successful!', 'success')
             return redirect(url_for('home'))
            
        else:
            flash('Invalid name or password', 'danger')
            return redirect(url_for('login'))

   
       
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create_db')
def create_db():
    db.create_all()
    return 'Database created successfully!'


@app.route('/post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            
            title = form.title.data
            user_id = current_user.id
            content = form.content.data
            privacy = form.privacy.data

            user = User.query.get(user_id)
            if not user:
                flash(f"No User with id {user_id} found", 'danger')
                return redirect(url_for('add_post'))


            post = Post(title=title, user_id=user_id, content=content, privacy=privacy)

            db.session.add(post)
            db.session.commit()
            flash('Subject added successfully!', 'success')
            return redirect(url_for('home'))

    return render_template('add_post.html', form=form)



