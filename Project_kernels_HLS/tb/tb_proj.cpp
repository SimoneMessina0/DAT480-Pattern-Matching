#include "tb_krnl_proj.h"
#include "hls_stream.h"
#include <iostream>
#include <fstream>
#include <string>

int main() {
    hls::stream<pkt> in_stream;
    hls::stream<pkt> out_stream;

    // Load input string from file
    std::ifstream infile("/home/t2_3/dat480_project_base/Project_kernels_HLS/tb/input.txt");
    if (!infile.is_open()) {
        std::cerr << "Failed to open input file!\n";
        return 1;
    }

    std::string line;
    std::getline(infile, line);
    infile.close();

    unsigned int size = line.size();
    unsigned int beats = (size + BYTES_PER_BEAT - 1) / BYTES_PER_BEAT;  // Correct calculation
    std::cout << "Input size: " << size << "\n";
    std::cout << "Number of beats: " << beats << "\n";

    // Feed input packets into the kernel
    for (unsigned int b = 0; b < beats; b++) {
        pkt pkt;
        pkt.data = 0;
        pkt.keep = 0;
        pkt.dest = 0;
        pkt.last = 0;

        // pack 64 bytes into AXI stream beat
        for (unsigned int i = 0; i < BYTES_PER_BEAT; i++) {
            unsigned int idx = b * BYTES_PER_BEAT + i;
            if (idx < line.size()) {
              pkt.data.range((i+1)*8-1, i*8) = line[idx];
              pkt.keep.range(i, i) = 1;
            }
        }

        if (b == beats - 1)
            pkt.last = 1;

        in_stream.write(pkt);
    }

    // Call kernel for each beat
    //for (unsigned int i = 0; i < beats; i++) {
    while (!in_stream.empty()) {
        krnl_proj(in_stream, out_stream);
    }
    
    // Read and print output
    std::cout << " Detected pattern IDs:\n";
    int max_ids_per_packet = DWIDTH / MATCH_ID_W;

    while (!out_stream.empty()) {
        pkt out = out_stream.read();
        // UNPACK LOGIC: Iterate through the 512-bit bus
        for (int i = 0; i < max_ids_per_packet; i++) {
            
            // Extract specific bit range for one ID
            ap_uint<MATCH_ID_W> packed_id = out.data.range((i + 1) * MATCH_ID_W - 1, i * MATCH_ID_W);
            
            // If the ID is non-zero, it is a valid match
            if (packed_id != 0) {
                std::cout << "ID " << packed_id << "\n";
            }
        }
    }

    return 0;
}