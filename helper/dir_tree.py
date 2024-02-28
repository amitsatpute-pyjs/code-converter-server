import os



class Project_handler:
    def __init__(self,source_path, destination_path, project_name):
        self.source_path = source_path
        self.destination_path = destination_path
        self.project_name =project_name        

    def get_all_folders(self):    
        folder_paths = []    
        for root, directories, files in os.walk(self.source_path):       
            for directory_name in directories:          
                folder_paths.append(os.path.relpath(os.path.join(root, directory_name), self.source_path))

        return folder_paths

    def get_all_file_paths(self):  
        file_paths = []        
        for root, directories, files in os.walk(self.source_path):            
            for filename in files:           
                file_path = os.path.join(root, filename)           
                file_paths.append(file_path)

        return file_paths

    def create_folders(self):        
        try:
            os.mkdir(f'{self.destination_path}/{self.project_name}')
        except Exception as e:           
            print(e)

        for folder in self.get_all_folders(): 
            try:
                os.mkdir(f'{self.destination_path}/{self.project_name}/{folder}')
            except Exception as e:
                print("Error:",e)


