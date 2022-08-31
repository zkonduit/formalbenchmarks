import glob
from pathlib import Path
import subprocess
from collections import Counter


# Create a map 
circuitToStatus = {}

markdownOutput = """\n| Circuit | Tool | Sound Constraints? |
| -------- | ---- | ---- | """

for r1csFile in glob.glob('generated/O0/*.r1cs', recursive=True):
    #print(r1csFile)
    rFilePath = Path(r1csFile)
    rFileWithoutExtensionJustName = rFilePath.with_suffix('').name
    rFileWithSymExtension = rFilePath.with_suffix('.sym')

    output = subprocess.run(["julia", "--project=EcneProject/.", "EcneProject/src/Ecne.jl", "--name", rFileWithoutExtensionJustName ,"--r1cs", rFilePath, "--sym", rFileWithSymExtension],  capture_output=True)
    #subprocess.run(["julia", "--project=EcneProject/.", "EcneProject/src/Ecne.jl", "--name", rFileWithoutExtensionJustName ,"--r1cs", rFilePath, "--sym", rFileWithSymExtension])
    # search for a string in the output
    if output.stdout.decode('utf-8').find('has sound constraints') != -1:
        #put this in the map
        circuitToStatus[rFileWithoutExtensionJustName] = 'sound constraints'
        markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | ECNE | :white_check_mark: |')
    else:
        circuitToStatus[rFileWithoutExtensionJustName] = 'potentially unsound constraints'
        markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | ECNE | :x: |')

# use Counter to count the number of each status
statusCount = Counter(circuitToStatus.values())
# print the results
print(markdownOutput)