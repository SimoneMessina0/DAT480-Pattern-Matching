# DAT480 Pattern Matching Project

[![University](https://img.shields.io/badge/University-Chalmers%20University%20of%20Technology-blue)](https://www.chalmers.se/en/)
![Course](https://img.shields.io/badge/Course-DAT480-informational)
[![HLS](https://img.shields.io/badge/Language-HLS-red)](https://github.com/SimoneMessina0/DAT480-Pattern-Matching)

This repository contains the implementation and resources for the **DAT480 Pattern Matching** project.
The project builds on an existing FPGA network design and extends it with custom **pattern matching functionality implemented using High-Level Synthesis (HLS)** targeting Xilinx Alveo platforms.

> ⚠️ **Note**
> An older README from the original upstream project existed previously.
> This file replaces it with updated, project-specific documentation.

---

## 📁 Repository Structure

The repository is organized as follows:

* `Basic_kernels/` – Basic kernel implementations
* `Benchmark_kernel/` – Benchmarking and performance-evaluation kernels
* `Ethernet/` – Ethernet and network interface logic
* `NetLayers/` – Network layer implementations
* `Notebooks/` – Jupyter notebooks for testing and experimentation
* `Project_kernels_HLS/` – High-Level Synthesis (HLS) kernels
* `Stream_throughput_kernel/` – Throughput measurement kernels
* `config_files/` – Build and configuration files
* `img/` – Images, diagrams, and visual resources
* `xrt_host_api/` – Host-side code using the Xilinx Runtime (XRT) API

---

## 🚀 Getting Started

### Prerequisites

To build and run this project, you need:

* Xilinx **Vivado** and **Vitis**
* Xilinx **XRT**
* A supported **Xilinx Alveo** FPGA board
* Linux host system (recommended)

---

## 🔨 Build Instructions

Clone the repository (including submodules):

```bash
git clone --recursive https://github.com/SimoneMessina0/DAT480-Pattern-Matching.git
cd DAT480-Pattern-Matching
```

Build the project:

```bash
make all DESIGN=project
```

This will generate the required HLS kernel objects and prepare the project for deployment.

---

## 🧠 Project Overview

The design integrates **HLS-based pattern matching kernels** into a high-performance FPGA network pipeline.
Data is streamed via AXI4-Stream interfaces, processed by network layers, and analyzed by custom pattern matching logic.

The focus of this project is on:

* Designing efficient **streaming HLS kernels**
* Exploring performance trade-offs in FPGA-based pattern matching
* Integrating custom logic into an existing network-oriented FPGA framework

Each major subdirectory contains self-descriptive code and auxiliary documentation.

---

## ▶️ Usage

### Jupyter Notebooks

The `Notebooks/` directory includes Python notebooks that demonstrate:

* Kernel interaction via XRT
* Data streaming and processing
* Performance evaluation and benchmarking

Start Jupyter with:

```bash
jupyter notebook
```

Then open the desired notebook and follow the instructions inside.

---

## 🛠️ Development Notes

When extending or modifying the project:

1. Keep kernel interfaces consistent with AXI4-Stream conventions
2. Validate functionality using C simulation before synthesis
3. Analyze resource usage and throughput after implementation

This repository currently focuses on **HLS-based development**.

---

## 📄 License

This project is released under an open-source license.
See the `LICENSE` file for full license information.

---

## 🎓 Academic Context

This project was developed by **Simone Francesco Messina** as part of the course **DAT480 – Reconfigurable Computing** at **Chalmers University of Technology**.

* **Course Examiner:** Ioannis Sourdis
* **Teaching Assistant:** Magnus Östgren

The work was carried out for educational and research purposes within the DAT480 course framework.
