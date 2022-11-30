import glob
from pathlib import Path
import subprocess
import picusConfig

#markdownOutput = """\n| Circuit | Tool | Sound Constraints? |
#| -------- | ---- | ---- | """

# instantiate dictionary
circuitToStatus = {}

#for r1csFile in glob.glob('generated/O0/*.r1cs', recursive=True): # PROD 
for r1csFile in glob.glob('../formalbenchmarks/generated/O0/*.r1cs', recursive=True): # DEV
#for r1csFile in glob.glob('benchmarks/circomlib/*.r1cs', recursive=True): # DEV
    #print("Polynomial Solver", r1csFile)
    rFilePath = Path(r1csFile)
    rFileWithoutExtensionJustName = rFilePath.with_suffix('').name
    #if rFileWithoutExtensionJustName in picusConfig.picusVerifiedList or rFileWithoutExtensionJustName in picusConfig.picusExcludeList:
        #continue
    #print (rFilePath)
    #print (r1csFile)
    #rFileWithSymExtension = rFilePath.with_suffix('.sym')
    try:
        output = subprocess.run(["./PolynomialSolver/target/release/check-determinism", r1csFile], timeout=100, capture_output=True, check=True) # prod
        #output = subprocess.run(["./target/release/check-determinism", r1csFile], timeout=400, capture_output=True) # dev

        if output.stdout.decode('utf-8').find('DETERMINISTIC') != -1:
            #put this in the map
            circuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Polynomial Solver", "result" : "Weakly Verified"}
            #print (rFileWithoutExtensionJustName + ' verified')
            #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Polynomial Solver | :white_check_mark: |')
        else:
            #print (rFileWithoutExtensionJustName + ' not verified')
            #put this in the map
            circuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Polynomial Solver", "result" : "Unverified"}
            #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Polynomial Solver | :x: |')
    
    except subprocess.TimeoutExpired:
         #print("Timeout!!!!!!!!!", rFileWithoutExtensionJustName)
         #put this in the map
         circuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Polynomial Solver", "result" : "Timeout"}
         #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Polynomial Solver | :alarm_clock: |')
    except subprocess.CalledProcessError:
        #print("CalledProcessError", rFileWithoutExtensionJustName)
        #put this in the map
        circuitToStatus[rFileWithoutExtensionJustName] = { "tool" : "Polynomial Solver", "result" : "OtherError"}
        #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Polynomial Solver | :x: |')
        
#print(markdownOutput)
print (circuitToStatus)
