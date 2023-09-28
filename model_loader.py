from llama_cpp import Llama
import json
import time

with open("./config.json", 'r') as j:
    config = json.loads(j.read())


class Model_Loader:
    def __init__(self):
        print("Loading model...")
        self.llm = Llama(model_path="./models/wizardcoder-python-13b-v1.0.Q5_K_M.gguf",
                         n_ctx=config["context_size"])
        print("Model is loaded..")
        self.result = ""
        self.max_token = config["max_token"]
        self.temp = config["temp"]
        self.echo = config["echo"]
    
    def convert_code(self, lang_from, lang_to, text):
        # prompt_info = f"Below is an instruction that describes a task. Write a response that appropriately completes the request without explanation, comment, doc string and information."
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
        self.result = res_text
        return self
   
    def save_code(self,file_location="./",file_name="",file_ext=".txt"):
        if not file_name:
            file_name = str(time.time())
        
        file = file_location + file_name + file_ext
        with open(file,"w") as f:
            f.write(self.result)
        print(f"File is saved on location:{file}")