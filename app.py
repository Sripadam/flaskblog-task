
from flask import *
from flask_mail import Mail,Message
import mysql.connector




mydb=mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Bulliyya@97",
    database = "mydatabase"
)
mycursor = mydb.cursor()


app=Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'flaskexample123@gmail.com'
app.config['MAIL_PASSWORD'] = 'kpsupjqwrkbcytxl'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

@app.route('/lists',methods=["GET"])
def lists():
    mycursor.execute("SELECT * FROM subscribers")
    all_subscribers = mycursor.fetchall()
           
    return render_template('lists.html',posts=all_subscribers)

@app.route("/posts/subscribe",methods=["GET","POST"])
def subscriber():
    try:
        if request.method == "POST":
            name = request.form['username']
            email=request.form['Email']
            if not  name or not email:
                return render_template("subscribe.html",message="Enter all the field")
            mycursor.execute("INSERT INTO subscribers (username,Email) VALUES(?,?)",(name,email)) 
            Msg = Message('New flaskBlog',sender="sample123@gmail.com",recipients=[f'{email}'])
            Msg.body = f'thank you {name}.you will get  the notification when new post is uploaded'
            mail.send(Msg)
            mydb.commit()
            return redirect(url_for('home'))
        return render_template("subscribers.html",message=" ") 
    except Exception as e:
        print(e)  

@app.route('/posts',  methods=['GET', 'POST'])
def posts():
    try:
        if request.method == 'POST':
            post_title = request.form['title']
            post_content = request.form['post']
            post_author = request.form['author']
            mycursor.execute("INSERT INTO posts (title,content,posted_by) VALUES (%s,%s,%s)",(post_title,post_content,post_author))
        
            mydb.commit()
            return redirect('/posts')
        else:
            mycursor.execute("SELECT * FROM posts")
            all_posts = mycursor.fetchall()
            print(type(all_posts))
            return render_template('posts.html',posts=all_posts)
    except Exception as e:
        print(e)        

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    try:
        if request.method == 'POST':
            post_title = request.form['title']
            post_content = request.form['post']
            post_author = request.form['author']
            mycursor.execute("INSERT INTO posts (title,content,posted_by) VALUES (%s,%s,%s)",(post_title,post_content,post_author))
            
            mydb.commit()
        
            return redirect('/posts')
        else:
            return render_template('new_post.html')
    except Exception as e:
        print(e) 


def get_post(id):
    p = mycursor.execute(
        'SELECT *'
        ' FROM posts '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if p is None:
        abort(404, f"Post id {id} doesn't exist.")
    return p


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    try:
        post=get_post(id)
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['post']
            author= request.form['author']
            mycursor.execute("UPDATE posts SET (title,content,posted_by) VALUES (%s,%s.%s)  WHERE= %s",(title,content,author,id))
            
            mydb.commit()
            
            return redirect('/posts')
        
        else:
            return render_template('edit.html',post=post)
        
    except Exception as e:
        return render_template('edit.html')

@app.route('/posts/delete/<int:id>',methods=["POST"])
def delete(id):
    try:
        get_post(id)
        if request.method == "POST":
            mycursor.execute("DELETE from posts where id=%s",(id,))
            mycursor.commit()
            return redirect('/posts')  
    except Exception as e:
        print(e)
        return redirect('/posts') 
@app.route('/login' ,methods=['GET','POST'])
def index():
    error=''
    try:
        if request.method == 'POST':
            attempted_username=request.form["Username"]
            attempted_password=request.form["Password"]
            
            if attempted_username == "admin" and attempted_password == "password":
                return redirect('/home')
            else:
                error= "Invalid credentials"    
        return render_template("login.html",error=error)
    except Exception as e:
        print(e)
        return render_template("login.html",error=error) 

@app.route('/home')
def home():
    return render_template("index.html")
if __name__=="__main__":
    app.run(debug=True)