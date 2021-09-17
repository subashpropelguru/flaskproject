from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#create table for user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#login route and function
@app.route("/", methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            if check_password_hash(user.password,request.form['password']):
                login_user(user)
                return redirect('/dashboard')
        error = "Invalid Email-Id or Password"        
        return render_template('index.html', error = error)
    return render_template('index.html', error = error)

#register route and function
@app.route("/register")
def register():
    passw = "admin123" 
    register = User(username="admin",email="admin@mailinator.com",password=generate_password_hash(passw,method='sha256'))
    db.session.add(register)
    db.session.commit()
    return "<h1>Register Successfully!</h1>"

#dashboard route and function
@app.route("/dashboard")
@login_required
def dashboard():
    username = current_user.username
    return render_template("admin/dashboard.html",username=username)

#contact route and function
@app.route("/contact")
@login_required
def contact():
    username = current_user.username
    return render_template("admin/contact/contact.html",username=username)

#logout route and function
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, port=8000)    