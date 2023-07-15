from flask import Flask, render_template, redirect, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
import os


app = Flask(__name__)
Bootstrap(app)


db = yaml.safe_load(open("settings.yaml"))
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["SECRET_KEY"] = os.urandom(24)
mysql = MySQL(app)


@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM posts")
    if result > 0:
        posts = cursor.fetchall()
        print(f"fetch posts: {posts}")
        cursor.close()
        return render_template("index.html", blogs=posts)
    return render_template("index.html", blogs=None)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/posts/<int:id>")
def posts(id):
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    if result > 0:
        post = cursor.fetchone()  
        print(f"fetch post: {post}")
        cursor.close()
        return render_template("posts.html", post=post)
    return render_template("posts.html", post=id)


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_details = request.form      

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (user_details['username'],))
        if cursor.fetchone():
            flash("Username already taken. Please choose a different username.", "danger")
            cursor.close()
            return render_template("register.html")

        cursor.execute("SELECT * FROM users WHERE email = %s", (user_details['email'],))
        if cursor.fetchone():
            flash("Email already registered. Please use a different email address.", "danger")
            cursor.close()
            return render_template("register.html")

        if not all(user_details.values()):
            flash("Please fill in all fields.", "danger")
            cursor.close()
            return render_template("register.html")

        if user_details["password"] != user_details["confirmPassword"]:
            flash("Passwords do not match.", "danger")
            cursor.close()
            return render_template("register.html")

        cursor.execute("INSERT INTO users(id, first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s, %s)",
                       ("", user_details['first_name'], user_details['last_name'], user_details['username'], user_details['email'], generate_password_hash(user_details['password'])))

        cursor.connection.commit()
        cursor.close()

        flash("User successfully registered", "success")
        return redirect("/login")

    return render_template("register.html")



@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_details = request.form
        username = user_details["username"]
        cursor = mysql.connection.cursor()
        result = cursor.execute(
            "SELECT * FROM users WHERE username = %s ", ([username]))
        if result > 0:
            user = cursor.fetchone()
            if check_password_hash(user['password'], user_details['password']):
                session['login'] = True
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                flash("Welcome " + session['first_name'] + "!")
            else:
                cursor.close()
                flash("Login or password incorreect.", "danger")
                return render_template("login.html")
        cursor.close()
        return redirect("/")
    return render_template("login.html")





@app.route("/new-blog/", methods=["GET", "POST"])
def new_blog():
    return render_template("new_blog.html")



@app.route("/my-blogs/")
def my_blogs():
    return render_template("my_blogs.html")


@app.route("/edit-blog/<int:id>/")
def edit_blog(id):
    return render_template("edit_blog.html", blog=id)


@app.route("/delete-blog/<int:id>/")
def delete_blog(id):
    return redirect("/my-blogs/")


@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out!", "info")
    return redirect("/")


# @app.route("/write-blog/")
# def write_blog():
#     return render_template("write_blog.html")





@app.route("/write-blog/", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        post_details = request.form
        cursor = mysql.connection.cursor()
     
        if not post_details["title"]: flash("Enter title!", "danger")
        elif not post_details["deskription"]: flash("Enter description!", "danger")
        elif not post_details["text"]: flash("Enter text!", "danger")
        else:
            cursor.execute("INSERT INTO posts(id, title, deskription, text) VALUES (%s, %s, %s, %s)",("", post_details['title'], post_details['deskription'], post_details['text']))
            cursor.connection.commit()
            cursor.close()
            flash("You successefully created a new post", "success")
            return redirect("/")

    return render_template("new_post.html")
@app.route("/edit-post/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    return render_template("edit_post.html", post=id)


if __name__ == "__main__":
    app.run(debug=True)
