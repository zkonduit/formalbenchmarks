# Formal Benchmarks
Circuit benchmarks (test cases) for formal verification of zk circuits.

This repository contains a number of circuits (mainly in circom and r1cs), organized as test cases for formal validation tools such as [Ecne](https://github.com/franklynwang/EcneProject).  These tools check that the circuit defines a unique witness for a given set of public and private inputs. 

Circuits are grouped roughly by complexity and difficulty, and include multiple formats (circom code, r1cs, symbolic), and each circuit has several variations. Variations include parameters (e.g. number of bits or inputs), compilation flags (which take the same input program and produce different arithmetizations). We also include some metadata describing what the circuit should do.

In addition we collect both positive examples and negative examples. Positive examples are circuits believed to be correct, and which generally have a unique output for a given input, or a unique witness (including output) for a given input.  Negative examples have a mistake that the formal validator should uncover, for example a missing constraint.

We are interested in formal validator accuracy, speed, and memory usage.


# Algebraicization and arithmetization





# Licence
Many of the circom circuits reproduced or modified here (including circomlib and 0xPARC/circom-ecdsa) are GPL-3.0, so this repository is also GPL-3.0. 
