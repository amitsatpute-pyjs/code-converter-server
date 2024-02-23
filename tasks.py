from celery import Celery
import requests
import redis
import json
import time
import os
from model_loader import Model_Loader
from dotenv import load_dotenv

load_dotenv()

app = Celery("tasks", backend=f'redis://{os.getenv("REDIS_HOST")}:{ os.getenv("REDIS_PORT")}/0',
             broker=f'redis://{os.getenv("REDIS_HOST")}:{ os.getenv("REDIS_PORT")}/0')
app.conf.broker_connection_retry_on_startup = True
rds = redis.Redis(host=os.getenv("REDIS_HOST"),
                  port=int(os.getenv("REDIS_PORT")), db=1)
headers = {'Content-Type': 'application/json'}



llm = Model_Loader()


@app.task()
def llm_convert_code(data, callback_api, rds_task_id):  
    obj = llm.convert_code(lang_from=data["lang_from"], lang_to=data["lang_to"],text=data["code"])   
    task_id = rds.get(rds_task_id).decode("utf-8")   
    print("Resutl88::", obj.result)  
    # result = json.loads(obj.result)   
    # print("Resutl::", result)
    response_data = {
        "task_id": task_id,        
        "task_result": obj.result
    }
    requests.post(callback_api, data=json.dumps(response_data), headers=headers)
    return  obj.result

