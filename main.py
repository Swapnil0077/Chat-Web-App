from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, send
import os


class SignUpForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Submit', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Submit', validators=[DataRequired()])


app = Flask(__name__)
# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")


# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)
    if message != "User connected!":
        send(message, broadcast=True)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

bootstrap = Bootstrap5(app)

app.secret_key = "secretkey"


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))


with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("username")
        password = request.form.get("password")

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login_page'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login_page'))
        else:
            login_user(user)
            return redirect(url_for('welcome_page'))

    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    form = SignUpForm()
    if form.validate_on_submit():
        if request.method == "POST":
            hash_and_salted_password = generate_password_hash(
                request.form.get('password'),
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                username=request.form.get('name'),
                email=request.form.get('email'),
                password=hash_and_salted_password,
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
    return render_template("register.html", form=form)


@app.route('/welcome', methods=["GET", "POST"])
@login_required
def welcome_page():
    return render_template("chat_page.html", name=current_user.username)


if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug=True, debug=False, host="192.168.1.8")

# IPv4 Address. . . . . . . . . . . : 192.168.1.8
