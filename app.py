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


#Some common responses
NO_LOGGED_RES = {"error": "You have to log in at: http://localhost:5002/"}
LESS_FIELDS_RES = {"error": "Not the required fields"}

@app.route("/")
def home():
    return "The app is running, visit postman"


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    response = appService.login({"name": username, "contraseña":password}) 
    
    if response["code"][0] == 1:
        session['USER_NAME']  = username
        session['USER_PASS'] = password

        return "You have logged in succesfully"
    
    elif response["code"][0] == 5001:
        return (f"{username} and {password} do not coincide with any user an password")

#LOGIN
@app.route("/logout", methods=["POST"])
def logout():
    session.pop('USER_NAME', None)
    session.pop('USER_PASS', None)
    return render_template("index.html")

#GET
@app.route("/api/tasks", methods=['GET'])
def tasks():
    print("The session you are looking for is: ")
    print(session)
    if ('USER_NAME' in session):
        return appService.get_tasks()
    return NO_LOGGED_RES
    

#GET
@app.route("/api/tasks/<int:id>", methods=['GET'])
def get_task_byId(id):
    if ('USER_NAME' in session):
        return appService.get_task_byId(str(id))
    return NO_LOGGED_RES


#POST
@app.route("/api/tasks", methods=["POST"])
def create_task():    
    expected_fields = ['name', 'description', 'due_date', 'Idestado']
    if ('USER_NAME' in session):
        request_data = request.get_json()
        if all(field in request_data for field in expected_fields):
            task = request_data
            task["username"] = session['USER_NAME']
            task["userpass"] = session['USER_PASS']
            return appService.create_task(task)
        else:
            return LESS_FIELDS_RES
    return NO_LOGGED_RES
    
#PUT
@app.route("/api/tasks", methods=["PUT"])
def update_task():
    
    expected_fields = ['task_id', 'name', 'description', 'due_date', 'estado', 'usuario']
    request_data = request.get_json(force=True)
    
    if ('USER_NAME' in session):
            
            # Verificamos que se reciban todos los campos esperados
            if all(field in request_data for field in expected_fields):
                request_data = request.get_json(force=True)
                return appService.update_task(request_data)
            
            return LESS_FIELDS_RES
    
    return NO_LOGGED_RES



#DELETE
@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    if ('USER_NAME' in session):
        return appService.delete_task(str(id))
    return NO_LOGGED_RES




