import json
from server import Server
from flask import jsonify, request
from flask_cors import cross_origin
from celery.result import AsyncResult
import os
import uuid
from dotenv import load_dotenv

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