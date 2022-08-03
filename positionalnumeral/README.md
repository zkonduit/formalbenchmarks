# Positional numeral circuits

This directory contains various circuits for positional numerals (place-value encodings according to a radix or base). The encoding of a number in its bit representation is often called num2bits and the inverse bits2num. These circuits take an input field element and decompose it into bits, or more generally legs, or perform the inverse operation of combining legs into a field element.  
For example, the constraint $a = a_0  + a_1 d + a_2 d^2$ is part of decomposing a field element $a$ into its ones place, its $d$s place, and its $d^2$ place.  
The example has three legs, each of size $d$.  If $d=2$, this is a bit decomposition, and if $d=2^{64}$, it is a decomposition into three 64-bit legs.  This constraint is not enough to enforce the decomposition, since we also must constrain $a_0,a_1,$ and $a_2$ to be in $\{0,\dots, d-1\}$.  This operation is important for several applications including range checks, non-prime-field arithmetic, and packing and unpacking smaller integer formats into field elements. 

Aliasing

Signed vs unsigned


The naming scheme for the examples is as follows. 



encode(d,l)

decode(d,l)
