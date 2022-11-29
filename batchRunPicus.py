import glob
from pathlib import Path
import subprocess
import picusConfig
#markdownOutput = """\n| Circuit | Tool | Sound Constraints? |
#| -------- | ---- | ---- | """

# instantiate dictionary
picusCircuitToStatus = {}

for r1csFile in glob.glob('generated/O0/*.r1cs', recursive=True): # PROD 
#for r1csFile in glob.glob('generated/O0/B*.r1cs', recursive=True): # DEV
#for r1csFile in glob.glob('benchmarks/circomlib/*.r1cs', recursive=True): # DEV
    #print("r1csFile", r1csFile)
    rFilePath = Path(r1csFile)
    rFileWithoutExtensionJustName = rFilePath.with_suffix('').name
    #if rFileWithoutExtensionJustName in picusConfig.picusVerifiedList or rFileWithoutExtensionJustName in picusConfig.picusExcludeList:
        #continue
    #print (rFilePath)
    #print (r1csFile)
    #rFileWithSymExtension = rFilePath.with_suffix('.sym')
    try:
        output = subprocess.run(["racket", "Picus/test-v3-uniqueness.rkt","--r1cs", r1csFile, "--weak", "--timeout", "5000"], timeout=300, capture_output=True) # prod
        #output = subprocess.run(["racket", "../Picus/test-v3-uniqueness.rkt","--r1cs", r1csFile, "--weak", "--timeout", "5000"], timeout=600, capture_output=True) # dev
        #print (output.stdout.decode('utf-8'))
       # subprocess.run(["racket", "test-v3-uniqueness.rkt","--r1cs", r1csFile, "--weak", "--timeout", "3000"], timeout=600)
        if output.stdout.decode('utf-8').find('weak uniqueness: safe') != -1:
            #put this in the map
            picusCircuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Picus v3/z3", "result" : "Weakly Verified"}
            #print (rFileWithoutExtensionJustName + ' verified')
            #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :white_check_mark: |')
        elif output.stdout.decode('utf-8').find('weak uniqueness: unsafe') != -1:
            #put this in the map
            picusCircuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Picus v3/z3", "result" : "Unsound"}
            #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :x: |')

        else:
            #print (rFileWithoutExtensionJustName + ' not verified')
            #put this in the map
            picusCircuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Picus v3/z3", "result" : "Unverified"}
            #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :x: |')
    
    except subprocess.TimeoutExpired:
         #print("Timeout!!!!!!!!!", rFileWithoutExtensionJustName)
         #put this in the map
         picusCircuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Picus v3/z3", "result" : "Timeout"}
         #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :alarm_clock: |')
#print(markdownOutput)
print (picusCircuitToStatus)
