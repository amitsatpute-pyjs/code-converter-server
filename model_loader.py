import os
from llama_cpp import Llama
import json
import time
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
load_dotenv()

with open("./config.json", 'r') as j:
    config = json.loads(j.read())


class Model_Loader:
    def __init__(self):
        self.platform = config["platform"]
        print("Loading model...")
        if config["platform"] =="local" :
            self.llm = Llama(model_path=config["model_path"],
                            n_ctx=config["context_size"])
        elif config["platform"]== "openai":           
            self.llm = AzureChatOpenAI(
                        openai_api_version=config["openai_api_version"],
                        azure_deployment=config["azure_deployment"]                       
                    )
        else:
            raise "Please select platform either local or openai eg. Model_Loader('local')"          
            
        print("Model is loaded..")
        self.result = ""
        self.max_token = config["max_token"]
        self.temp = config["temp"]
        self.echo = config["echo"]
    
    def convert_code(self, lang_from, lang_to, text):
        # prompt_info = f"Below is an instruction that describes a task. Write a response that appropriately completes the request without explanation, comment, doc string and information."
        res_text = ''
        if self.platform=="local":
            prompt_instruction = f"### Instruction:Convert the following {lang_from} code to {lang_to} without any explanation or additional information:"
            promt_input = f"### Input:{text}"
            prompt_result = f"### Response:"

            main_prompt = prompt_instruction + promt_input + prompt_result
            print("temp:",self.temp)
            print("echo:",self.echo)
            print("max:",self.max_token)

            output = self.llm(
                main_prompt, max_tokens=self.max_token, echo=self.echo, temperature=self.temp)

            res_text = output["choices"][0]["text"].split('### Response:')[-1]
            if "### Output:" in res_text:
                res_text = output["choices"][0]["text"].split('### Output:')[-1]
        elif self.platform=="openai":
            prompt = f'''Convert the following {lang_from} code to {lang_to} without any explanation or additional information:
                {text}
            '''          
            message = HumanMessage(
                content=prompt
            )
            data = self.llm([message])
            res_text = data.content
        else:
            pass
        self.result = res_text
        return res_text
    
    def create_dockerfile(self,file_name, lang_to, text):
        # prompt_info = f"Below is an instruction that describes a task. Write a response that appropriately completes the request without explanation, comment, doc string and information."
        res_text = ''
        if self.platform=="local":
            prompt_instruction = f'''### Instruction:Create dockerfile for the following {lang_to} code without any explanation or additional information. Also consider following conditions :
                a. Use file name as {file_name}
                b. Install all required libraries or packages which is used in code.
                c. Expose a port            
            '''
            promt_input = f"### Input:{text}"
            prompt_result = f"### Response:"

            main_prompt = prompt_instruction + promt_input + prompt_result
            
            output = self.llm(
                main_prompt, max_tokens=self.max_token, echo=self.echo, temperature=self.temp)

            res_text = output["choices"][0]["text"].split('### Response:')[-1]
            if "### Output:" in res_text:
                res_text = output["choices"][0]["text"].split('### Output:')[-1]
        elif self.platform=="openai":
            prompt = f'''Create dockerfile for following {lang_to} code without any explanation or additional information:
                {text}
            '''          
            message = HumanMessage(
                content=prompt
            )
            data = self.llm([message])
            res_text = data.content
        else:
            pass
        self.result = res_text
        return res_text
   
    def save_code(self,file_location="./",file_name="",file_ext=".txt"):
        if not file_name:
            file_name = str(time.time())
        
        file = file_location + file_name + file_ext
        with open(file,"w") as f:
            f.write(self.result)
        print(f"File is saved on location:{file}")