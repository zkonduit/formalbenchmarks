import glob
from pathlib import Path
import subprocess

markdownOutput = """\n| Circuit | Tool | Sound Constraints? |
| -------- | ---- | ---- | """

for r1csFile in glob.glob('generated/O0/*.r1cs', recursive=True): # PROD 
# for r1csFile in glob.glob('../formalbenchmarks/generated/O0/*.r1cs', recursive=True): # DEV
#for r1csFile in glob.glob('benchmarks/circomlib/*.r1cs', recursive=True): # DEV
    #print(r1csFile)
    rFilePath = Path(r1csFile)
    rFileWithoutExtensionJustName = rFilePath.with_suffix('').name

    #rFileWithSymExtension = rFilePath.with_suffix('.sym')
    try:
        output = subprocess.run(["racket", "Picus/test-uniqueness.rkt","--r1cs", rFilePath, "--timeout", "10000"], timeout=600, capture_output=True)
    
        if output.stdout.decode('utf-8').find('verified') != -1:
            #put this in the map
            markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :white_check_mark: |')
        else:
            markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :x: |')
    
    except subprocess.TimeoutExpired:
        # print("Timeout!!!!!!!!!", rFileWithoutExtensionJustName)
        markdownOutput+=('\n| '+ rFileWithoutExtensionJustName + ' | Picus | :alarm_clock: |')
print(markdownOutput)
