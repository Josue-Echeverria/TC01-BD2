import json
import os

from app_service import AppService
from db import Database
from flask import Flask, session, request, render_template


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")



db = Database(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

app = Flask(__name__)
appService = AppService(db)
#For the use of the session feauture
app.secret_key = 'any random string'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    response = appService.login({"name": username, "contraseña":password}) 
    if response["code"][0] == 1:
        session['USER_NAME']  = username
        session['USER_PASS'] = password
        return render_template("logged.html")
    
    elif response["code"][0] == 5001:
        return (f"{username} and {password} do not coincide with any user an password")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop('USER_NAME', None)
    session.pop('USER_PASS', None)
    return render_template("index.html")


@app.route("/api/tasks", methods=['GET'])
def tasks():
    if ('USER_NAME' in session):
        return appService.get_tasks()
    return {"error": "You have to log in at: http://localhost:5002/"}
    


@app.route("/api/tasks/<int:id>", methods=['GET'])
def get_task_byId(id):
    if ('USER_NAME' in session):
        return appService.get_task_byId(str(id))
    return {"error": "You have to log in at: http://localhost:5002/"}



@app.route("/api/tasks", methods=["POST"])
def create_task():
    
    if ('USER_NAME' in session):
        request_data = request.get_json()
        task = request_data
        task["username"] = session['USER_NAME']
        task["userpass"] = session['USER_PASS']
        return appService.create_task(task)
    
    return {"error": "You have to log in at: http://localhost:5002/"}
    

@app.route("/api/tasks", methods=["PUT"])
def update_task():
    request_data = request.get_json(force=True)
    return appService.update_task(request_data)


@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    return appService.delete_task(str(id))


#delete ruta cambiada
@app.route("/api/tasks/id=<int:id>", methods=["DELETE"])
def delete_task(id):
    if ('USER_NAME' in session):
        return appService.delete_task(str(id))
    return {"error": "You have to log in at: http://localhost:5002/"}




