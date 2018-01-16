from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
import string, cgi
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.completed = False

#use this part to add new blog list
@app.route('/')
def index():
    return redirect(url_for('blog'))

#use this part to add new blog list
@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    if blog_id != None:
        tasks = Blog.query.filter_by(id = blog_id).all()
        #return '404 - hI Template not found'
        #url_text = urlencode("/blogcontent.html?blogid=")
        if tasks != None:
            return render_template('/blogcontent.html', tasks=tasks)
        else:
            return '<h1>Blog doesnt exist for the ID </h>'

    else:
        tasks = Blog.query.filter_by(completed=False).all()
        #completed_tasks = Blog.query.filter_by(completed=True).all()
        return render_template('blog.html', tasks=tasks)

@app.route('/new_blog', methods=['POST', 'GET'])
def new_blog():
    
    title_name = "" 
    title_name = cgi.escape(title_name, quote=True)
    add_error=""
    add_error = cgi.escape(add_error, quote=True)
    blog_content=""
    blog_content = cgi.escape(blog_content, quote=True)
    if request.method == 'POST':
        title_name = request.form['title']
        blog_content = request.form['blog-content']
        if title_name and blog_content:
            new_blog = Blog(title_name, blog_content)
            db.session.add(new_blog )
            db.session.commit()

            tasks = Blog.query.filter_by(completed=False).all()
            completed_tasks = Blog.query.filter_by(completed=True).all()
            
            #return render_template('blog-listing.html', tasks=tasks)
            #form_value = request.form['param_name']
            obj = Blog.query.order_by(Blog.id.desc()).first()
        
            most_recent_idx=obj.id
            return redirect(url_for('blog',id=most_recent_idx))
        else:
            if(title_name):
                add_error = 'Body cannot be blank'
            else:
                add_error = 'Title cannot be blank'
            return render_template('new_post.html', title=request.form['title'], blog=request.form['blog-content'], error=add_error)

    if request.method == 'GET':
        
        #completed_tasks = Blog.query.filter_by(completed=True).all()
        return render_template('new_post.html')
        
#step2(gets username/user id from the link)    
@app.route('/blog1')
def blog1():
    #handles id part
    blog_id = request.args.get('id')
    tasks = Blog.query.filter_by(id = blog_id).all()
    #return '404 - hI Template not found'
    #url_text = urlencode("/blogcontent.html?blogid=")
    return render_template('/blogcontent.html', tasks=tasks)

@app.route('/blogcontent')
def blogcontent():
        blog_id=request.args.get('id','')
        tasks = Blog.query.filter_by(id = blog_id).all()
        #return '404 - hI Template not found'
        return render_template('/blogcontent.html', tasks=tasks)





if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run() 