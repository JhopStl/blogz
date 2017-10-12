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

    def __init__(self, title):
        self.title = title

@app.route('/blog', methods=['POST'])
def index():
    
    blogs = Blog.query.all()
    return render_template('blog.html',title="Build-a-blog", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def entry():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_entry = request.form['blog_entry']
        
        new_blog = Blog(blog_title)
        db.session.add(new_blog)
        db.session.commit()

    return render_template('newpost.html', blog_title=blog_title, blog_entry=blog_entry)

if __name__== "__main__":
    app.run()