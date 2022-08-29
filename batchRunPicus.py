import glob
from pathlib import Path
import subprocess

for r1csFile in glob.glob('../main/generated/O0/*.r1cs', recursive=True):
    #print(r1csFile)
    rFilePath = Path(r1csFile)
    #rFileWithSymExtension = rFilePath.with_suffix('.sym')
    subprocess.run(["racket", "test-uniqueness.rkt","--r1cs", rFilePath, "--timeout", "10000"])