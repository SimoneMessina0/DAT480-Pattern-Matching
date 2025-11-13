.PHONY: help

help:
	@echo "Makefile Usage:"
	@echo "  make all DEVICE=<FPGA platform>"
	@echo "      Command to generate the xo for specified device."
	@echo "      By default, DEVICE=xilinx_u55c_gen3x16_xdma_3_202210_1"
	@echo ""
	@echo "  make clean "
	@echo "      Command to remove the generated non-hardware files."
	@echo ""
	@echo "  make distclean"
	@echo "      Command to remove all the generated files."
	@echo "  make distcleanall"
	@echo "      Command to remove all the generated in the current directory and one level down"	
	@echo ""


DEVICE ?= xilinx_u55c_gen3x16_xdma_3_202210_1
kernel_list ?= example


XSA := $(strip $(patsubst %.xpfm, % , $(shell basename $(DEVICE))))
TEMP_DIR := _x.$(XSA)
VIVADO := $(XILINX_VIVADO)/bin/vivado
VITIS_HLS := $(XILINX_HLS)/bin/vitis_hls
VPP := $(XILINX_VITIS)/bin/v++
CLFLAGS += -t hw --platform $(DEVICE) --save-temps

BINARY_OBJS = $(addprefix $(TEMP_DIR)/, $(addsuffix .xo, $(kernel_list)))

.PHONY: all clean distclean 
all: check-devices check-vivado check-vitis check-xrt $(BINARY_OBJS)  


# Cleaning stuff
clean:
	rm -rf *v++* *.log *.jou _regs

distclean: clean
	rm -rf build_dir*
	rm -rf ./tmp_$(KRNL_NAME)* ./packaged_kernel* 
	rm -rf _x.* *.str
	rm -rf _x* .Xil


$(TEMP_DIR)/example.xo: package.tcl src/*.vhd
	mkdir -p $(TEMP_DIR)
	$(VIVADO) -mode batch -source package.tcl -notrace -tclargs $@ example $(XSA) example

check-devices:
ifndef DEVICE
	$(error DEVICE not set. Please set the DEVICE properly and rerun. Run "make help" for more details.)
endif

#Checks for XILINX_VIVADO
check-vivado:
ifndef XILINX_VIVADO
	$(error XILINX_VIVADO variable is not set, please set correctly and rerun)
endif

#Checks for XILINX_VITIS
check-vitis:
ifndef XILINX_VITIS
	$(error XILINX_VITIS variable is not set, please set correctly and rerun)
endif

#Checks for VITIS_HLS
check-vitis-hls:
ifndef VITIS_HLS
	$(error VITIS_HLS variable is not set, please set correctly and rerun)
endif

#Checks for XILINX_XRT
check-xrt:
ifndef XILINX_XRT
	$(error XILINX_XRT variable is not set, please set correctly and rerun)
endif