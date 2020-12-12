from flask import Flask,render_template,url_for,request,redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug=True
Bootstrap(app)



import flaskr.routes
