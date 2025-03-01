from flask import Flask, render_template, request, redirect, session, g, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret'  # Required for session handling


# Makes login vunerable due to cookies
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True

DATABASE = 'vulnerable_social.db'

# Connect to SQLite
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Allows fetching columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Register/Login Page
@app.route("/", methods=["GET", "POST"])
def register_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        action = request.form["action"]
        cur = get_db().cursor()
        
        if action == "register":
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = cur.fetchone()

            if existing_user:
                return '''
                <script>
                    alert("Username already exists! Try a different one.");
                    window.history.back(); 
                </script>
                '''
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return '''
            <script>
                alert("Registration successful! You can now log in.");
                window.history.back()"; 
            </script>
            '''
        
        elif action == "login":
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            cur.execute(query)
            user = cur.fetchone()

            
            if user:
                session["user"] = user["username"]  # Ensure correct username is stored
                return redirect(url_for("following_feed"))
            else:
                return '''
                <script>
                    alert("Invalid credentials. Please try again.");
                    window.history.back();
                </script>
                '''

    return render_template("register_login.html")

# Global Feed (Shows All Posts)
@app.route("/global_feed")
def global_feed():
    cur = get_db().cursor()
    cur.execute("""
        SELECT posts.id, users.username, posts.content, posts.likes 
        FROM posts 
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.id DESC
    """)
    posts = cur.fetchall()
    return render_template("global_feed.html", posts=posts)

# Following Feed (Shows Only Followed Users' Posts)
@app.route("/following_feed")
def following_feed():
    if "user" not in session:
        return redirect(url_for("register_login"))
    
    cur = get_db().cursor()
    cur.execute("""
        SELECT posts.id, users.username, posts.content, posts.likes 
        FROM posts 
        JOIN users ON posts.user_id = users.id 
        WHERE users.id IN (
            SELECT followed_id FROM follows WHERE follower_id = (SELECT id FROM users WHERE username = ?)
        )
        ORDER BY posts.id DESC
    """, (session["user"],))
    
    posts = cur.fetchall()
    return render_template("following_feed.html", posts=posts)

# Create Post
@app.route("/post", methods=["GET", "POST"])
def post():
    if "user" not in session:
        return redirect(url_for("register_login"))
    
    if request.method == "POST":
        content = request.form["content"]
        cur = get_db().cursor()
        cur.execute(
            "INSERT INTO posts (user_id, content, likes) VALUES ((SELECT id FROM users WHERE username = ?), ?, 0)", 
            (session["user"], content)
        )
        get_db().commit()
        return redirect(url_for("following_feed"))
    
    return render_template("post.html")

@app.route("/follow/<int:user_id>", methods=["GET", "POST"])
def follow(user_id):
    # Ensure user is logged in
    if "user" not in session:
        return redirect(url_for("register_login"))
    
    cur = get_db().cursor()
    cur.execute(
        "INSERT INTO follows (follower_id, followed_id) VALUES ((SELECT id FROM users WHERE username = ?), ?)", 
        (session["user"], user_id)
    )
    get_db().commit()
    return redirect(url_for("users"))



# List All Users
@app.route("/users")
def users():
    if "user" not in session:
        return redirect(url_for("register_login"))
    
    cur = get_db().cursor()
    cur.execute("SELECT id, username FROM users WHERE username != ?", (session["user"],))
    users = cur.fetchall()
    return render_template("users.html", users=users)

# Like Post
@app.route("/like/<int:post_id>", methods=["GET"])
def like(post_id):
    cur = get_db().cursor()
    cur.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    get_db().commit()
    return redirect(url_for("following_feed"))

# User Profile Page
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("register_login"))
    
    cur = get_db().cursor()
    
    # Get user's own posts
    cur.execute("""
        SELECT posts.id, users.username, posts.content, posts.likes 
        FROM posts 
        JOIN users ON posts.user_id = users.id
        WHERE users.username = ?
        ORDER BY posts.id DESC
    """, (session["user"],))
    posts = cur.fetchall()

    # Get list of users they are following
    cur.execute("""
        SELECT users.id, users.username FROM users
        JOIN follows ON users.id = follows.followed_id
        WHERE follows.follower_id = (SELECT id FROM users WHERE username = ?)
    """, (session["user"],))
    following = cur.fetchall()

    # Get list of followers
    cur.execute("""
        SELECT users.id, users.username FROM users
        JOIN follows ON users.id = follows.follower_id
        WHERE follows.followed_id = (SELECT id FROM users WHERE username = ?)
    """, (session["user"],))
    followers = cur.fetchall()

    return render_template("profile.html", username=session["user"], posts=posts, following=following, followers=followers)

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("register_login"))

if __name__ == "__main__":
    app.run(debug=True)
