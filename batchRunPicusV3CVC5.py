import glob
from pathlib import Path
import subprocess
import picusConfig

#markdownOutput = """\n| Circuit | Tool | Sound Constraints? |
#| -------- | ---- | ---- | """

# instantiate dictionary
picusCircuitToStatus = {}

for r1csFile in glob.glob('generated/O0/*.r1cs', recursive=True): # PROD 
#for r1csFile in glob.glob('../formalbenchmarks/generated/O0/*.r1cs', recursive=True): # DEV
#for r1csFile in glob.glob('benchmarks/circomlib/*.r1cs', recursive=True): # DEV
    #print("picus", r1csFile)
    rFilePath = Path(r1csFile)
    rFileWithoutExtensionJustName = rFilePath.with_suffix('').name
    #if rFileWithoutExtensionJustName in picusConfig.picusVerifiedList or rFileWithoutExtensionJustName in picusConfig.picusExcludeList:
        #continue
    #print (rFilePath)
    #print (r1csFile)
    #rFileWithSymExtension = rFilePath.with_suffix('.sym')
    try:
        output = subprocess.run(["racket", "Picus/test-v3-uniqueness.rkt","--r1cs", r1csFile, "--weak", "--solver", "cvc5", "--timeout", "5000"], timeout=100, capture_output=True, check=True) # prod
       # output = subprocess.run(["racket", "test-pp-uniqueness.rkt","--r1cs", r1csFile, "--weak", "--timeout", "5000"], timeout=600, capture_output=True) # dev

       # subprocess.run(["racket", "test-v3-uniqueness.rkt","--r1cs", r1csFile, "--weak", "--timeout", "3000"], timeout=600)
        if output.stdout.decode('utf-8').find('weak uniqueness: safe') != -1:
            #put this in the map
            picusCircuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Picus v3/cvc5", "result" : "Weakly Verified"}
            #print (rFileWithoutExtensionJustName + ' verified')
            #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :white_check_mark: |')
        elif output.stdout.decode('utf-8').find('weak uniqueness: unsafe') != -1:
            picusCircuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Picus v3/cvc5", "result" : "Unsound"}
            #print (rFileWithoutExtensionJustName + ' not verified')
            #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :x: |')
        else:
            #print (rFileWithoutExtensionJustName + ' not verified')
            #put this in the map
            picusCircuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Picus v3/cvc5", "result" : "Unverified"}
            #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :x: |')
    
    except subprocess.TimeoutExpired:
         #print("Timeout!!!!!!!!!", rFileWithoutExtensionJustName)
         #put this in the map
         picusCircuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Picus v3/cvc5", "result" : "Timeout"}
         #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :alarm_clock: |')
    except subprocess.CalledProcessError:
        #print("CalledProcessError", rFileWithoutExtensionJustName)
        #put this in the map
        picusCircuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Picus v3/cvc5", "result" : "OtherError"}
        #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus v3/cvc5 | :x: |')
    
#print(markdownOutput)
print (picusCircuitToStatus)
