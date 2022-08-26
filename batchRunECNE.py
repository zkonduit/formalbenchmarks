import glob
from pathlib import Path
import subprocess

for r1csFile in glob.glob('generated/**/*.r1cs', recursive=True):
    #print(r1csFile)
    rFilePath = Path(r1csFile)
    rFileWithoutExtensionJustName = rFilePath.with_suffix('').name
    rFileWithSymExtension = rFilePath.with_suffix('.sym')
    subprocess.run(["julia", "--project=EcneProject/.", "EcneProject/src/Ecne.jl", "--name", rFileWithoutExtensionJustName ,"--r1cs", rFilePath, "--sym", rFileWithSymExtension])