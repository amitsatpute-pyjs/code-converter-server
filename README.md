# Code-Converter-Server

Code converter server, it is run on CPU. If you want to run it on GPU install `llama_cpp_cuda`.
And change import `llama_cpp` to `llama_cpp_cuda` in  `model_loader.py` file

# How to run

1.  Clone the repository.
2.  Then enter command : `cd code-converter-server`
3.  Then install all required dependencies: `sh setup.sh`
       a. It will install all dependencies and create virtual environment for python
       b. Also it create models folder:
		       - Download [model](https://huggingface.co/TheBloke/WizardCoder-Python-13B-V1.0-GGUF/resolve/main/wizardcoder-python-13b-v1.0.Q5_K_M.gguf) 
		       - Add downloaded model in to models folder.
		       - For other models refer https://huggingface.co
4.  First start the celery worker, run command : `sh run_celery_worker.sh`
5.  After step 4 , run the flask app (API server) : `sh run_server.sh`
6.  For API reference, check api.rest file

# Information
Celery is used for handling multiple requests.

