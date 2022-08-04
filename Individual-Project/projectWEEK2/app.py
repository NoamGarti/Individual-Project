from flask import Flask, redirect, request, render_template, url_for
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyDn7hQzO0fQal2HH_hZT8Hv4HULEBONqlU",
  "authDomain": "websiteeditors-w2-proj.firebaseapp.com",
  "projectId": "websiteeditors-w2-proj",
  "storageBucket": "websiteeditors-w2-proj.appspot.com",
  "messagingSenderId": "85947415138",
  "appId": "1:85947415138:web:de7dcddf08b03ed38d2f3b",
  "databaseURL": "https://websiteeditors-w2-proj-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)
app.config['SECRET_KEY'] = 'pinetwork314159265'

# Your code should be below
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        user = {
        "email" : email,
        "password" : password
        }
        db.child('Users').child(login_session['user']['localId']).set(user)

        return redirect(url_for('signin'))
    else:
        return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)           
            return redirect(url_for('index'))
        except:
            error = "Authentication failed"
    else:
        return render_template("signin.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/editors')
def editors():
    return render_template("editors.html")


@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/')
def index():
        # Gets the current user’s information from the database
    user = db.child("Users").child(login_session['user']['localId']).get().val()
    print(user)
    # email=user["email"]
    return render_template('index.html',email = user['email'])

@app.route('/about')
def about():
    return render_template('about.html')



# Your code should be above

if __name__ == "__main__":  # Makes sure this is the main process
    app.run(debug=True)