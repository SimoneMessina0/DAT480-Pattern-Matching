#ifndef KRNL_PROJ_H
#define KRNL_PROJ_H

#include <hls_stream.h>
#include <ap_int.h>
#include "ap_axi_sdata.h"
#include "patterns.h"

#define DWIDTH 32
#define TDWIDTH 16


// Parametric dimensions of variables in design
constexpr int clog2(int x) { return (x<=1) ? 1 : 1 + clog2((x+1)>>1); }

constexpr int BYTES_PER_BEAT = DWIDTH/8;
constexpr int MATCH_ID_W = clog2(TOTAL_NUM_PATTERNS + 1);


typedef ap_axiu<DWIDTH, 1, 1, TDWIDTH> pkt;

// struct udp_app2nl {
//     ap_uint<DWIDTH> data;
//     ap_uint<64> keep;
//     ap_uint<16> dest;
//     ap_uint<1> last;
// };

 struct udp_nl2app {
     ap_uint<DWIDTH> data;
     ap_uint<64> keep;
     ap_uint<16> dest;
     ap_uint<1> last;
 };

#ifdef __cplusplus
extern "C" {
#endif

// void krnl_proj(
//     hls::stream<udp_nl2app> &in_stream, 
//     hls::stream<udp_app2nl> &out_stream  
// );
void krnl_proj(
    hls::stream<pkt> &in_stream, 
    hls::stream<pkt> &out_stream  
);

#ifdef __cplusplus
} // close extern "C"
#endif

#endif
