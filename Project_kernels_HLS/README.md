# Project Kernel - HLS

The provided sources here are basically empty. You should still be able to generate a Vitis project, by running:
```sh
make all
```
But `C Synthesis` will fail. There is no function at all in [src/krnl_proj.cpp](src/krnl_proj.cpp) and Vitis is looking for one specifically named *krnl_proj*.

The tb [tb/tb_proj.cpp](tb/tb_proj.cpp) is similarly empty. You need to implement this to run the simulation. The testbenches from the tutorials can be used as inspiration.