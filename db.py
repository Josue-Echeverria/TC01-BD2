import psycopg2


class Database:
    def __init__(
        self, database="db_name", host="db_host", user="db_user", password="db_pass", port="db_port"
    ):
        self.conn = psycopg2.connect(
            database=database, host=host, user=user, password=password, port=port
        )

    def login(self, user):
        cursor = self.conn.cursor()
        query = "SELECT login(%s, %s);"
        parametros = (user['name'],user['contraseña'])
        cursor.execute(query, parametros)
        result = cursor.fetchone()#Lo que retorno la funcion de postgres
        cursor.close()
        return {"name": user["name"],"pass": user["contraseña"], "code": result}


    def get_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT public.get_tasks();")
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_task_byId(self, task_id):
        cursor = self.conn.cursor()
        query = "SELECT get_task_byId(%s);"
        cursor.execute(query, (task_id,))
        data = cursor.fetchall()
        cursor.close()
        return data

    def create_task(self, task):
        cursor = self.conn.cursor()
        query = "SELECT create_task(%s, %s, %s, %s, %s, %s);"
        parametros = (task['name'],task['description'], task['due_date'], task['Idestado'], task['username'], task["userpass"])
        cursor.execute(query, parametros)
        result = cursor.fetchone()#Lo que retorno la funcion de postgres
        retursStatement = {}
        if(result == 1):
            retursStatement = task
        elif(result == 5001):
            retursStatement = {"error": "User not recognized by the database"}
        cursor.close()
        return retursStatement


    def update_task(self, task_data):
        cursor = self.conn.cursor()
        query = "SELECT public.update_task(%(task_id)s,%(name)s,%(description)s,%(due_date)s,%(estado)s,%(usuario)s);"
        cursor.execute(query, task_data)
        result = cursor.fetchone()
        returnStatement = {}
        if(result == 1):
            returnStatement = {'success': "Task updated"}
        else:
            returnStatement = {"error": "Update failed"}
        cursor.close()
        return returnStatement


    def delete_task(self, request_task_id):
        cursor = self.conn.cursor()
        query = "SELECT delete_task(%s);"  # funcion sql
        cursor.execute(query, (request_task_id,))
        result = cursor.fetchone()
        return_statement = {}
        if result == 1:
            return_statement =  {"message":"Se elimino la tarea"}
        elif result== 5001:
            return_statement = {"message":"No se encontró el id"}
        cursor.close()
        return return_statement