import glob
from pathlib import Path
import subprocess

for r1csFile in glob.glob('generated/O0/*.r1cs', recursive=True):
    #print(r1csFile)
    rFilePath = Path(r1csFile)
    #rFileWithoutExtensionJustName = rFilePath.with_suffix('').name
    #rFileWithSymExtension = rFilePath.with_suffix('.sym')
    subprocess.run(["racket", "Picus/test-inc-uniqueness.rkt","--r1cs", rFilePath])