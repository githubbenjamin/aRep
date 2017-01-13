from flask import *
app = Flask(__name__)
app.secret_key = 'any random string’

@app.route("/")
def hello():
    return '<html><body><h1>Hello World</h1></body><html>'

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        print("POST method")
        user=request.form['nm']
        if 'username' in session:
            username=session['username']
#        return render_template('hello.html', name=user)
        return redirect(url_for('success',name=user))
    else:
        print("GET method")
        t_args = request.args
        print type(t_args)
        user=request.args.get('nm')
        return render_template('hello.html', name=user)
#        return redirect(url_for('success',name=user))
@app.route('/logout')
def logout():
    # remove the username from the session if it is there session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method=='POST':
        user= request.form['nm']
        resp = make_response('''<html><body><a href="/getcookie">click to read the cookie</a></body></html>''')
        resp.set_cookie('userID', user)
        return resp
@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    return '<h1>welcome '+name+'</h1>'

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8088, debug=False)
