from flask import Flask, request, redirect, render_template, flash
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

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost')
def index():
    return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def entry():
    if request.method == 'POST':
        title = request.form['blog_title']  #pull title from form
        body = request.form['blog_entry']   #pull body from from

        if title == '':
            flash("Please fill out all fields!", 'error')
            return redirect ('/newpost')
        if body == '':
            flash("Please fill out all fields!", 'error')
            return redirect ('/newpost')

        new_blog = Blog(title,body)  #create new blog object
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