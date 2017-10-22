from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:95vtec@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'asdfasfasfd'
#create db object
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(230))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/newpost')
def index():
    return render_template('newpost.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user'] = user.username
                flash('welcome back, '+user.username)
                return redirect("/newpost")
        flash('bad username or password')
        return redirect("/login")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        #if not is_email(email):
           # flash('zoiks! "' + email + '" does not seem like an email address')
           # return redirect('/signup')
        username_db_count = User.query.filter_by(username=username).count() #checks to see if username exists
        if username_db_count > 0:
            flash('yikes! "' + username + '" is already taken and password reminders are not implemented')
            return redirect('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        user = User(username=username, password=password) #assigns the fields data that has been input from the register form
        db.session.add(user) #adds user to db
        db.session.commit()
        session['user'] = user.username
        return redirect("/newpost")
    else:
        return render_template('signup.html')

@app.route('/blog', methods=['POST', 'GET'])
def entry():
    if request.method == 'POST':
        title = request.form['blog_title']  #pull title from form
        body = request.form['blog_entry']   #pull body from form

        if title == '':
            flash("Please fill out all fields!", 'error')
            return redirect ('/newpost')
        if body == '':
            flash("Please fill out all fields!", 'error')
            return redirect ('/newpost')

        new_blog = Blog(title,body)  #create new blog object- TODO - will need to add "owner" once I can filter user
        db.session.add(new_blog)
        db.session.flush()
        blogsId = new_blog.id  #assigns id to new blog
        db.session.commit()  #commits blog to db
        return redirect ('/blog?id={0}'.format(blogsId))

    x = request.args.get('id')
    # checks if there are query parameters
    if x:
        blogId = Blog.query.get(request.args.get('id'))
        return render_template('soloblog.html', blogId=blogId)
    blogs = Blog.query.all()
    return render_template('blog.html', titles="Build-a-blog", blogs=blogs)

if __name__== "__main__":
    app.run()