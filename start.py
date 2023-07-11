from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml, os


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

@app.route("/blogs/<int:id>/")
def blog(id):
    return render_template("blog.html", blog=id)

@app.route("/register/", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
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
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

