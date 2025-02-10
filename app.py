import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ✅ Database-configuratie voor zowel lokale als online hosting
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")  
if DATABASE_URL.startswith("postgres://"):  # Render gebruikt soms een oude PostgreSQL-indeling
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "supersecretkey")
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)  # WebSockets voor realtime chat
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ✅ Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Vacature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(100), nullable=False)
    beschrijving = db.Column(db.Text, nullable=False)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Routes
@app.route('/')
def index():
    vacatures = Vacature.query.all()
    return render_template('index.html', vacatures=vacatures)

@app.route('/vacatures')
def vacatures():
    vacatures = Vacature.query.all()
    return render_template('vacatures.html', vacatures=vacatures)

@app.route('/vacature/<int:id>')
def vacature_details(id):
    vacature = Vacature.query.get_or_404(id)
    return render_template('vacature_details.html', vacature=vacature)

@app.route('/solliciteren/<int:id>', methods=['GET', 'POST'])
@login_required
def solliciteren(id):
    vacature = Vacature.query.get_or_404(id)
    if request.method == 'POST':
        motivatie = request.form['motivatie']
        flash(f"Sollicitatie voor {vacature.titel} succesvol ingediend!", "success")
        return redirect(url_for('dashboard'))
    return render_template('solliciteren.html', vacature=vacature)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/chat')
@login_required
def chat():
    messages = ChatMessage.query.all()
    return render_template('chat.html', messages=messages, username=current_user.username)

@socketio.on('message')
def handle_message(msg):
    if msg != "User connected!":
        new_message = ChatMessage(sender=current_user.username, message=msg)
        db.session.add(new_message)
        db.session.commit()
        send(f"{current_user.username}: {msg}", broadcast=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam bestaat al!", "danger")
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registratie succesvol! Log nu in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Succesvol ingelogd!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Ongeldige inloggegevens!", "danger")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Succesvol uitgelogd!", "info")
    return redirect(url_for('index'))

# ✅ Database aanmaken als deze nog niet bestaat
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
=======
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ✅ Database-configuratie voor zowel lokale als online hosting
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")  
if DATABASE_URL.startswith("postgres://"):  # Render gebruikt soms een oude PostgreSQL-indeling
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "supersecretkey")
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)  # WebSockets voor realtime chat
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ✅ Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Vacature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(100), nullable=False)
    beschrijving = db.Column(db.Text, nullable=False)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Routes
@app.route('/')
def index():
    vacatures = Vacature.query.all()
    return render_template('index.html', vacatures=vacatures)

@app.route('/vacatures')
def vacatures():
    vacatures = Vacature.query.all()
    return render_template('vacatures.html', vacatures=vacatures)

@app.route('/vacature/<int:id>')
def vacature_details(id):
    vacature = Vacature.query.get_or_404(id)
    return render_template('vacature_details.html', vacature=vacature)

@app.route('/solliciteren/<int:id>', methods=['GET', 'POST'])
@login_required
def solliciteren(id):
    vacature = Vacature.query.get_or_404(id)
    if request.method == 'POST':
        motivatie = request.form['motivatie']
        flash(f"Sollicitatie voor {vacature.titel} succesvol ingediend!", "success")
        return redirect(url_for('dashboard'))
    return render_template('solliciteren.html', vacature=vacature)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/chat')
@login_required
def chat():
    messages = ChatMessage.query.all()
    return render_template('chat.html', messages=messages, username=current_user.username)

@socketio.on('message')
def handle_message(msg):
    if msg != "User connected!":
        new_message = ChatMessage(sender=current_user.username, message=msg)
        db.session.add(new_message)
        db.session.commit()
        send(f"{current_user.username}: {msg}", broadcast=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam bestaat al!", "danger")
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registratie succesvol! Log nu in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Succesvol ingelogd!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Ongeldige inloggegevens!", "danger")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Succesvol uitgelogd!", "info")
    return redirect(url_for('index'))

# ✅ Database aanmaken als deze nog niet bestaat
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
