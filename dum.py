from flask import Flask
from flask import *
from flask import g


from functools import wraps
import secrets

MAIN = Flask(__name__)



# Hard-coded permissions - these tokens should be longer, this is an exmaple
# This says the token "b5c4dd9eacde6dcc09e6" is allowed to run both do_something_post and
#   another_function_post functions
#   where 0164daeeb3d9d8de0ada is only allowed do_something_post
#   and 7e1c68083ddc49a436fb is only allowed another_function_post
permissions = {
    "do_something_post": [
        secrets.token_hex(64),
        "b5c4dd9eacde6dcc09e6"
    ],
    "another_function_post": [
        secrets.token_hex(64),
        "b5c4dd9eacde6dcc09e6"
    ],
    #"report_get": ["dummy"]
}

# defining the decorator
def secured(func):
    @wraps(func)
    def secured__func(*args, **kwargs):
        #assert('Auth-Token' in request.headers), abort(401, 'Missing Auth Header')
        # This is assigning the Auth-Token HTTP Header to a variable
        auth_token = request.headers.get('Auth-Token')

    # Do some test to validate auth_token is allowed, maybe a hard-coded dictionary like permissions above 
        # maybe if func._name_ is in permissions and then the key is defined under that
        if func.__name__ in permissions.keys(): # This is checking there is an entry in the permissions table
            if auth_token not in permissions[func.__name__]:
                return'Auth-Token Unauthorized'
        else:
            return  'Function missing from permissions table' # if the function name is missing from permissions
    # the else would be allowed?

        return func(*args, **kwargs)

    secured__func.__name__ = func.__name__

    return secured__func

@MAIN.route('/error')  
def error():  
    return "<p><strong>Enter correct details</strong></p>"  

@MAIN.route('/',methods=['POST','GET'])
def demo():
    
    return render_template('login.html')

@MAIN.route('/success',methods = ['POST'])  
def success():  
    if request.method == "POST":  
        g.server = request.form['servername']  
        g.action = request.form['action']  
      
      
    return render_template('success.html')

@MAIN.route('/route1', methods=['POST','GET'])
@secured  # this is a decorator that will run secured and pass the function name
def do_something_post():
    
    
    
    #print(g.server)
    # load JSON data into variable
    #inbound = request.form['server']
    return redirect(url_for('success'))
    # ... continue here


@MAIN.route('/route2', methods=['POST'])
@secured  # this is a decorator that will run secured and pass the function name
def another_function_post():
    # load JSON data into variable
    inbound = request.get_json()
    if inbound is None:
        return " nothing "
    else:
        return inbound
    # ... continue here
    

    # ... continue here



@MAIN.route('/route3', methods=['GET'])
#@secured  # this is a decorator that will run secured and pass the function name
def report_get():
    Key=request.args.get('key')
    

    return Key
    # ... continue here
if __name__=='__main__':
    MAIN.run(debug=True)
