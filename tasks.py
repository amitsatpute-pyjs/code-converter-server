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
    result = llm.convert_code(lang_from=data["lang_from"], lang_to=data["lang_to"],text=data["code"])   
    task_id = rds.get(rds_task_id).decode("utf-8")   
    # print("Resutl88::", obj.result)  
    # result = json.loads(obj.result)   
    # print("Resutl::", result)
    response_data = {
        "task_id": task_id,        
        "task_result": result
    }
    requests.post(callback_api, data=json.dumps(response_data), headers=headers)
    return  result

@app.task()
def llm_direct_convert_code(data):
    source_file_path = data["source"]
    file_path = data["file_path"]    
    desination_path = data["destination"]
    project_name = data["project_name"]
    
    with open(file_path, "r") as rf:
        code = rf.read()

    result = llm.convert_code(lang_from=data["lang_from"], lang_to=data["lang_to"],text=code)
    print("++++++++++++++++++++++++++++++++++++++++++")
    print("=====>",result)

    new_path = file_path.replace(source_file_path,f"{desination_path}/{project_name}")   
    file_exe = new_path.split(".")[-1]
    new_path = new_path.replace(file_exe,"py")        
    with open(f"{new_path}","w") as f:
        f.write(result)
  
    return  result

@app.task()
def llm_create_dockerfile(data):   
    file_for_docker = data["app_file_path"]
    desination_path = data["destination"]
    project_name = data["project_name"]
    file_path = f'{desination_path}/{project_name}/{file_for_docker}'
    with open(file_path, "r") as rf:
        code = rf.read()
    file_name = file_for_docker.split("/")[-1]
    result = llm.create_dockerfile(file_name=file_name,lang_to=data["lang"],text=code)
    print("*******************************")
    print("=====>",result)
    
    with open(f"{desination_path}/{project_name}/Dockerfile","w") as f:
        f.write(result)
  
    return  result

