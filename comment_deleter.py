#This time only with half the regexes!
#Recursively deletes all the comments in .py and .qml files that are not hidden (.*) or start with _
import os, re
#-------------------------------------------------------------------------------
def replace_in_file(folder_path, filename):
    #print("x" + filename + filetype)
    if filename.endswith(".py") or filename.endswith(".qml"):
        print(filename)
        with open(folder_path + "/" + filename, "r") as file:
            read_data = file.readlines()
            output_data = []
            for line in read_data:
                #Python files
                if filename.endswith(".py"):
                    if "#" in line:
                        #appends only the part before #
                        output_data.append(line[:line.find("#")] + '\n')
                    else:
                        output_data.append(line)
                #C files
                elif filename.endswith(".qml"):
                    #appends only the part before //
                    if "//" in line:
                        output_data.append(line[:line.find("//")] + '\n')
                    else:
                        output_data.append(line)
        #Joins the data together to allow parsing with regexes
        output_data = ''.join(output_data)
        if filename.endswith(".py"):
            output_data = re.sub(re.compile(r"\"\"\".*?\"\"\"",re.DOTALL), "", output_data)
        elif filename.endswith(".qml"):
            output_data = re.sub(r"\/\*.*?\*\/", "", output_data)
        #Writes the data to the file
        with open(folder_path + "/" + filename, "w") as output_file:
            output_file.write(output_data)

def search_and_copy(folder_path):
    for filename in os.listdir(folder_path):
        #Folder files
        if os.path.isdir(folder_path + "/" + filename) and not filename.startswith(".") and not filename.startswith("_"):
            #print(filename)
            search_and_copy(folder_path + "/" + filename)
        #Non folder files that don't start with a dot (.) or underline (_)
        elif not filename == "comment_deleter.py" and not filename.startswith(".") and not filename.startswith("_"):
            replace_in_file(folder_path, filename)

if __name__=="__main__":
    search_and_copy(os.getcwd())
