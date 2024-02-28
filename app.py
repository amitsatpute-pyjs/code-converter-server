import json
from server import Server
from flask import jsonify, request
from flask_cors import cross_origin
from celery.result import AsyncResult
import os
import uuid
from dotenv import load_dotenv
from helper.dir_tree import Project_handler

load_dotenv()


server = Server(__name__)

rds = server.redis
celery = server.celery
app = server.app
socket = server.socketio
callback_api = f"http://{os.getenv('SERVER_HOST')}:{os.getenv('SERVER_PORT')}/api/callback_result"

@app.route('/api/callback_result', methods=['POST'])
def callback_result():
    print("call back called")
    data = request.get_json()
    socket.emit(str(data["task_id"]), data)
    return jsonify("done")


@app.route('/convert', methods = ['POST'])
@cross_origin()
def convert():
    rds_task_id = str(uuid.uuid4())
    body = request.json    
    kwargs = {"data": body, "callback_api": callback_api,
              "rds_task_id": rds_task_id}
    task = celery.send_task("tasks.llm_convert_code", kwargs=kwargs)
    rds.set(rds_task_id, task.id)
    return jsonify({"task_id":task.id})  


@app.route('/convertporject', methods = ['POST'])
@cross_origin()
def convert_project():    
    req_data = request.json 
    p = Project_handler(req_data["source"],req_data["destination"],req_data["project_name"])
    p.create_folders()
    paths = p.get_all_file_paths()
    dirs = p.get_all_folders()      
    tasks = []
    for path in paths:       
        body=req_data
        body["file_path"]= path
        kwargs = {"data": body}
        task = celery.send_task("tasks.llm_direct_convert_code", kwargs=kwargs)
        tasks.append(task.id)
        
    return jsonify({"task_id":tasks})  

@app.route('/dockerfile', methods = ['POST'])
@cross_origin()
def create_dockerfile():    
    req_data = request.json    
    tasks = []
    
    body=req_data       
    kwargs = {"data": body}
    task = celery.send_task("tasks.llm_create_dockerfile", kwargs=kwargs)
    tasks.append(task.id)
        
    return jsonify({"task_id":tasks})  

@app.route("/convert/<task_id>", methods=["GET"])
@cross_origin()
def get_status(task_id):
    result = AsyncResult(task_id,app=celery)   
    response_data = {
        "task_id": task_id,
        "task_status": result.status,
        "task_result": result.result
    }

    return jsonify(response_data)
    


if __name__ == '__main__':
    server.run()