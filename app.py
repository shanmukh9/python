from flask import *  
import secrets
token=secrets.token_hex(20)
print(token)
  
app = Flask(__name__)  
 
@app.route('/error')  
def error():  
    return "<p><strong>Enter correct password and token</strong></p>"  
 
@app.route('/')  
def login():  
    return render_template("home.html")  
 
@app.route('/success',methods = ['POST'])  
def success():  
    if request.method == "POST":  
        email = request.form['email']  
        password = request.form['pass']  
        Token=request.form['token']
      
    if Token==token and password=='admin':  
        resp = make_response(render_template('action.html'))  
        resp.set_cookie('email',email)  
        return resp  
    else:  
        return redirect(url_for('error'))  
 
@app.route('/viewprofile')  
def profile():  
    email = request.cookies.get('email')  
    resp = make_response(render_template('profile.html',name = email))  
    return resp  
  
if __name__ == "__main__":  
    app.run(debug = True)  