from flask import Flask,render_template,request
from models.model import OnegaiContent
from config.database import db_session
from datetime import datetime

app = Flask(__name__)

from views.batch import batch_app
app.register_blueprint(batch_app, url_prefix='/batch')

@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("name")
    all_onegai = OnegaiContent.query.all()
    return render_template("index.html",name=name,all_onegai=all_onegai)

@app.route("/index",methods=["post"])
def post():
    name = request.form["name"]
    all_onegai = OnegaiContent.query.all()
    return render_template("index.html",name=name,all_onegai=all_onegai)

@app.route("/add",methods=["post"])
def add():
    title = request.form["title"]
    body = request.form["body"]
    content = OnegaiContent(title,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return index()

@app.route("/update",methods=["post"])
def update():
    content = OnegaiContent.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.commit()
    return index()

#おまじない
if __name__ == "__main__":
    app.run(debug=True)