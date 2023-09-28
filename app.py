from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from celery_setup import make_celery
from celery.result import AsyncResult
from model_loader import Model_Loader
import time

llm = Model_Loader()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    result_backend='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task(name='app.llm')
def get_llm(lang_from,lang_to,code):
    obj = llm.convert_code(lang_from=lang_from, lang_to=lang_to,text=code)    
    return obj.result

@app.route('/convert', methods = ['POST'])
@cross_origin()
def convert():
    body = request.json
    s1 = time.time()   
    task = get_llm.delay(lang_from=body["lang_from"], lang_to=body["lang_to"],code=body["code"])
    exe_time = time.time()-s1 
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
  
    app.run(debug = True)