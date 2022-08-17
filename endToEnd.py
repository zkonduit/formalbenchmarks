import glob
import os
import re
import subprocess
from pathlib import Path


def lookup_benchmark_parameters(parameter):
    return 1 # replace with lookup once we have the values. Still need to figure out the case with multiple benchmarks to test.

def create_instantiated_template(filePath, projectName, toplevelName, templateName, params = None):
    currentDir = os.getcwd()
    if params == None:
        filename = templateName + '@'+ toplevelName+'@'+projectName+'.circom'

        file_text = f"""pragma circom 2.0.0;
include \"../{filePath}\";
component main = {templateName}();
        """
        #print (file_text)
        with open(currentDir+'/generated/'+filename, "w") as f:
            f.write(file_text)

    else:
        paramStringMap = map(str, map(lookup_benchmark_parameters, params))
        filename = templateName + '@'+ toplevelName+'@'+projectName+'_'+'_'.join(map(str, map(lookup_benchmark_parameters, params)))+'.circom'
        #print (filename)
        
        file_text = f"""pragma circom 2.0.0;
include \"../{filePath}\";

component main = {templateName}({','.join(map(str, map(lookup_benchmark_parameters, params)))});
         """
        #print (file_text)
        with open(currentDir+'/generated/'+filename, "w") as f:
            f.write(file_text)

def generateCircomFiles():
    templateSet = set()
    templateDups = set()
    for file in glob.glob("circomlibscratch/**/*.circom", recursive=True):
        #print(file) # This is the full path of the file that is currently being processed
        cName = os.path.basename(file).split(".")[0]    # Name of the circom file, no path, no extension. This is composed of templates.
        with open(file, 'r') as f:
            for line in f:
                if "template" in line: # We have found a template that we need to process
                    # print (line)
                    templateNameWithParams = re.search(r'template (.*\))', line)
                    if templateNameWithParams is None: continue
                    templateNameWithParams = templateNameWithParams.group(1)
                    #if templateName not in templateSet:
                        #print (templateName)            
                        #print (len (templateSet))
                    if templateNameWithParams in templateSet:
                        templateDups.add(templateNameWithParams)
                        #print (templateName)
                    templateSet.add(templateNameWithParams)
    #print(templateDups)
                    templateNameWithoutParams = templateNameWithParams.split('(')[0]
                    #print (templateNameWithoutParams)

                    params = re.search(r'\(.*\)', line).group(0)
                    #print (params)
                    strippedParams = "".join(params.split())
                    numParams = 0
                    if strippedParams == "()": # No params
                        #print("No Params")
                        create_instantiated_template(file, "circomlib", cName, templateNameWithoutParams)
                    else:
                        #print("some params")
                        splitAndStrippedParams = strippedParams[1:-1].split(',') # remove the ()
                        numParams = len(splitAndStrippedParams)
                        #print(splitAndStrippedParams)
                        create_instantiated_template(file, "circomlib", cName, templateNameWithoutParams, splitAndStrippedParams)

# Grab the top level circom file that may have multiple templates
# for each of the templates, create a new circom file 
# write all the necessary parts of the circom file

def generateR1CSFiles():
    # 0. For each instantiated circom file
    # 1. Run command line circom for compiler output o0
    # 2. Run command line circom for compiler output o1
    # 3. Run command line circom for compiler output o2

    for circomFile in glob.glob('generated/*.circom'):
        print(circomFile)
        subprocess.run(["circom", circomFile, "--r1cs", "--sym", "--O0", "-o", "generated/O0"])
        subprocess.run(["circom", circomFile, "--r1cs", "--sym", "--O1", "-o", "generated/O1"])
        subprocess.run(["circom", circomFile, "--r1cs", "--sym", "--O2", "-o", "generated/O2"])



def main():
    #generateCircomFiles()
    generateR1CSFiles()                
    # 1. Split apart the params
    # 2. Instantiate some default to start, like 0
    # 3. In the future, this will do a lookup from somewhere
    # 4. Create the r1cs files by running circom on the 3 compiler flags
                

if __name__ == "__main__":
    main()