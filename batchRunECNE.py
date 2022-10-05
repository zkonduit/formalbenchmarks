import glob
from pathlib import Path
import subprocess
from collections import Counter


# Create a map 
ECNECircuitToStatus = {}

#markdownOutput = """\n| Circuit | Tool | Sound Constraints? |
#| -------- | ---- | ---- | """

for r1csFile in glob.glob('generated/O0/B*.r1cs', recursive=True):
    #print("ecne", r1csFile)
    rFilePath = Path(r1csFile)
    rFileWithoutExtensionJustName = rFilePath.with_suffix('').name
    rFileWithSymExtension = rFilePath.with_suffix('.sym')

    output = subprocess.run(["julia", "--project=EcneProject/.", "EcneProject/src/Ecne.jl", "--name", rFileWithoutExtensionJustName ,"--r1cs", rFilePath, "--sym", rFileWithSymExtension],  capture_output=True)
    #subprocess.run(["julia", "--project=EcneProject/.", "EcneProject/src/Ecne.jl", "--name", rFileWithoutExtensionJustName ,"--r1cs", rFilePath, "--sym", rFileWithSymExtension])
    # search for a string in the output
    if output.stdout.decode('utf-8').find('has sound constraints') != -1:
        #put this in the map
        ECNECircuitToStatus[rFileWithoutExtensionJustName] = {"tool" : "ECNE", "result" : "Weakly Verified"} 
        #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | ECNE | :white_check_mark: |')
    else:
        ECNECircuitToStatus[rFileWithoutExtensionJustName] = {"tool" : "ECNE", "result" : "Not Verified"}
        #markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | ECNE | :x: |')

# use Counter to count the number of each status
# print the results
#print(markdownOutput)
# print the map
print (ECNECircuitToStatus)