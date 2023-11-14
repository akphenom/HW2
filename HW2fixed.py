import os
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__,template_folder='templates')

UPLOAD_FOLDER = 'templates'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret_key"

@app.route("/")
def index():
    if len(session) == 0:
        return render_template("login.html")
    else:
        return redirect(url_for("homepage"))

@app.route("/homepage_action", methods = ["POST","GET"])
def homepage_action():
    if request.method == "POST":
        inputtext = request.form["inputtext"]
        blogfile = open("blog.txt","a") # append mode
        blogfile.write(inputtext+"\n")
        blogfile.close()
    return homepage()

@app.route("/homepage")
def homepage():
    webpage = '''
    <html>
    <head>
    <title>Home</title>
    </head>
    <body>
    <p style='text-align:left;'>
    <h1>Welcome to the TECH 136 Blog
    <span style='float:right;'>
    Username:
    ''' + session["username"] + " <a href='" + url_for("logout") + "'>Logout</a></hi></span></p>"

    webpage += '''
    <form action = 'homepage_action' method = 'POST'>
    Enter your comment here:
    <br>
    <textarea id='inputtext' name='inputtext' rows='2' cols='100'></textarea>
    <br>
    <input type = 'Submit' />
    <br>
    '''
    webpage += "<a href='/upload_file'>OR Upload image</a>"
    with open("blog.txt", "r") as blogfile:
        blog = blogfile.read().rstrip()
    blogfile.close()
    bloglist = blog.split("\n")

    for i in range(len(bloglist)-1,-1,-1):
        webpage += \
        "<br><textarea id='blogtext"+str(i)+"' name='blogtext"+str(i)+"' rows='2' cols='100'>"+bloglist [i]+"</textarea>"

    return webpage

@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the POST request contains file
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('upload_file', filename=file.filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new FIle</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''

@app.route("/login_action",methods = ['POST','GET'])
def login_action():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Dummy Validation
        if username == "guest" and password == "password":
            session["username"] = username
            return redirect(url_for("homepage"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("login.html")

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=50075)
