from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("user_id"):
        return "User %s is logged in!"%session['user_id']
    else:    
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)

    if user_id != None:
        flash("User authenticated")
        session['user_id'] = user_id
    else:
        flash("Password incorrect, there may be dragons.")

    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))   

@app.route("/user/<username>")
def view_user(username):
    logged_in = False
    user_id = model.get_user_by_name(username)[0]
    if session.get("user_id"):
        logged_in = True

    if user_id != None:        
        wall_posts = model.get_wall_posts(user_id)
        if not wall_posts:
            return render_template("wall.html", message="This user has no posts.",
                                                logged_in=logged_in)
        else:
            return render_template("wall.html", posts=wall_posts,
                                                logged_in=logged_in)
            print wall_posts
    else:
        return render_template("wall.html", message="Not a valid user.")


if __name__ == "__main__":
    app.run(debug = True)
