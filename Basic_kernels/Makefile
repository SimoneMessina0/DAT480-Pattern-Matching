.PHONY: help

help:
	@echo "Makefile Usage:"
	@echo "  make all DEVICE=<FPGA platform> kernel_list=\"<list of kernels>"\"
	@echo "      Command to generate the xo for specified device and Interface."
	@echo "      By default, DEVICE=xilinx_u55c_gen3x16_xdma_3_202210_1 and kernel_list=\"krnl_s2mm krnl_mm2s\""
	@echo ""
	@echo "  make clean "
	@echo "      Command to remove the generated non-hardware files."
	@echo ""
	@echo "  make distclean"
	@echo "      Command to remove all the generated files."
	@echo ""


DEVICE ?= xilinx_u55c_gen3x16_xdma_3_202210_1
kernel_list ?= krnl_s2mm krnl_mm2s

FREQ ?= 300000000
XSA := $(strip $(patsubst %.xpfm, % , $(shell basename $(DEVICE))))
TEMP_DIR := _x.$(XSA)
VPP := $(XILINX_VITIS)/bin/v++
CLFLAGS += --platform $(DEVICE)
BINARY_OBJS = $(addprefix $(TEMP_DIR)/, $(addsuffix .xo, $(kernel_list)))


.PHONY: all clean distclean
all: check-devices check-vitis check-xrt $(BINARY_OBJS)


# Cleaning stuff
clean:
	rm -rf *v++* *.log *.jou

distclean: clean
	rm -rf _x* .Xil

$(TEMP_DIR)/krnl_mm2s.xo: src/krnl_mm2s.cpp
	$(eval kernel := $(subst $(TEMP_DIR)/,,$(subst .xo,,$@)))
	mkdir -p $(TEMP_DIR)/$(kernel)/$(kernel)
	echo "freqhz=$(FREQ)" > $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "[hls]" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "flow_target=vitis" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "syn.output.format=xo" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "syn.top=$(kernel)" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "syn.file=../../$^" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	$(VPP) --compile --mode hls --work_dir $(TEMP_DIR)/$(kernel)/$(kernel) --config $(TEMP_DIR)/$(kernel)/$(kernel).cfg $(CLFLAGS) $^
	ln -srnf $(TEMP_DIR)/$(kernel)/$(kernel)/$(kernel).xo $@

$(TEMP_DIR)/krnl_s2mm.xo: src/krnl_s2mm.cpp
	$(eval kernel := $(subst $(TEMP_DIR)/,,$(subst .xo,,$@)))
	mkdir -p $(TEMP_DIR)/$(kernel)/$(kernel)
	echo "freqhz=$(FREQ)" > $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "[hls]" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "flow_target=vitis" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "syn.output.format=xo" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "syn.top=$(kernel)" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "syn.file=../../$^" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	$(VPP) --compile --mode hls --work_dir $(TEMP_DIR)/$(kernel)/$(kernel) --config $(TEMP_DIR)/$(kernel)/$(kernel).cfg $(CLFLAGS) $^
	ln -srnf $(TEMP_DIR)/$(kernel)/$(kernel)/$(kernel).xo $@

$(TEMP_DIR)/krnl_counters.xo: src/krnl_counters.cpp
	$(eval kernel := $(subst $(TEMP_DIR)/,,$(subst .xo,,$@)))
	mkdir -p $(TEMP_DIR)/$(kernel)/$(kernel)
	echo "freqhz=$(FREQ)" > $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "[hls]" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "flow_target=vitis" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "syn.output.format=xo" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "syn.top=$(kernel)" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	echo "syn.file=../../$^" >> $(TEMP_DIR)/$(kernel)/$(kernel).cfg
	$(VPP) --compile --mode hls --work_dir $(TEMP_DIR)/$(kernel)/$(kernel) --config $(TEMP_DIR)/$(kernel)/$(kernel).cfg $(CLFLAGS) $^
	ln -srnf $(TEMP_DIR)/$(kernel)/$(kernel)/$(kernel).xo $@

check-devices:
ifndef DEVICE
	$(error DEVICE not set. Please set the DEVICE properly and rerun. Run "make help" for more details.)
endif

#Checks for XILINX_VITIS
check-vitis:
ifndef XILINX_VITIS
	$(error XILINX_VITIS variable is not set, please set correctly and rerun)
endif

#Checks for XILINX_XRT
check-xrt:
ifndef XILINX_XRT
	$(error XILINX_XRT variable is not set, please set correctly and rerun)
endif