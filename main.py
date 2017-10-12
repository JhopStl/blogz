from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:95vtec@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
#create db object
db = SQLAlchemy(app)

class Blog(db.Model):

    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(230))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost')
def index():
    return render_template('newpost.html')

@app.route('/blog', methods=['POST'])
def entry():

    #blog_id = int(request.form['blog-id'])
    title = request.form['blog_title']
    body = request.form['blog_entry']

    blogs = Blog.query.all()
    #blogs.body = body
    new_blog = Blog(title,body)
    db.session.add(new_blog)
    db.session.commit()

    return render_template('blog.html', titles="Build-a-blog", title=title, body=body, blogs=blogs)

if __name__== "__main__":
    app.run()