import unittest
import json  # Agregar la importación del módulo json
from app import app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.USER_TEST = 'Kevin'
        self.PASS_TEST = 'holamundo'
        self.ERROR_NO_LOGIN = "{\"error\":\"You have to log in at: http://localhost:5002/\"}\n"
        self.ERROR_LESS_FIELDS = "{\"error\":\"Not the required fields\"}\n"


    # ----- UPDATE TESTS
    def testUnauthorizedUpdate(self):
        with self.app as client:
            
            response = client.put('/api/tasks', json={"task_id":1,"name":"Task prueba", "description":"hola mundo test", "due_date":'10-10-2010', "estado":1, "usuario":1})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_LOGIN, response.get_data(as_text=True))

    def testLessFieldsUpdate(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['USER_NAME'] = self.USER_TEST
                sess['USER_PASS'] = self.PASS_TEST

            payload = {"task_id": 1, "name": "UpdatedTask"} 
            response = self.app.put('/api/tasks', json=payload)  

            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS, response.get_data(as_text=True))


    def testCorrectUpdate(self):        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['USER_NAME'] = self.USER_TEST
                sess['USER_PASS'] = self.PASS_TEST
            
            response = client.put('/api/tasks', json={"task_id":1,"name":"Task prueba", "description":"hola mundo test", "due_date":'10-10-2010', "estado":1, "usuario":1})
            
            self.assertEqual(response.status_code, 200)



    


        

if __name__ == '__main__':
    unittest.main()
