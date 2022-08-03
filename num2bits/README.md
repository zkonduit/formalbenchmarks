# Num2Bits

This directory contains various Num2Bits circuits. These take an input field element and decompose it into bits, or more generally legs, or the inverse operation of combining legs into a field element.  For example, the constraint $ a = a_0  + a_1 d + a_2 d^2$ is part of decomposing a field element $a$ into its ones place, its $d$s place, and its $d^2$ place.  It has three legs, each of size $d$.  If $d=2$, this is a bit decomposition, and if $d=2^64$, it is a decomposition into three 64-bit legs.  This constraint is not enough to enforce the decomposition, since we also must constrain $a_0,a_1,$ and $a_2$.  This operation is important for several applications including range checks, non-prime-field arithmetic, and packing and unpacking smaller integer formats into field elements. 

Aliasing


The naming scheme for the examples is as follows. 


