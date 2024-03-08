import json
import os

from app_service import AppService
from db import Database
from flask import Flask, request, render_template


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

USER_NAME = ""
USER_PASS = ""

db = Database(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

app = Flask(__name__)
appService = AppService(db)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    response = appService.login({"name": username, "contraseña":password}) 
    if response["code"][0] == 1:
        global USER_NAME
        USER_NAME = username
        global USER_PASS
        USER_PASS = password
        return render_template("logged.html")
    
    elif response["code"][0] == 5001:
        return (f"{username} and {password} do not coincide with any user an password")


@app.route("/logout", methods=["POST"])
def logout():
    global USER_NAME
    USER_NAME = ""
    global USER_PASS
    USER_PASS = ""
    return render_template("index.html")

@app.route("/api/tasks")
def tasks():
    return appService.get_tasks()


@app.route("/api/tasks/<int:id>")
def task_by_id(id):
    return appService.get_task_by_id(id)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    if (USER_NAME == "" or USER_PASS== ""):
        return {"error": "You have to log in at: http://localhost:5002/"}
    else:
        request_data = request.get_json()
        task = request_data
        task["username"] = USER_NAME
        task["userpass"] = USER_PASS
        return appService.create_task(task)


@app.route("/api/tasks", methods=["PUT"])
def update_task():
    request_data = request.get_json()
    return appService.update_task(request_data)


@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    return appService.delete_task(str(id))

#delete ruta cambiada
'''@app.route("/api/tasks/id=<int:id>", methods=["DELETE"])
def delete_task(id):
    return appService.delete_task(str(id))
'''


