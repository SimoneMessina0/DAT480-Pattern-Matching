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

// Width for byte indexing
constexpr int BYTES_I_W = clog2(BYTES_PER_BEAT + 1);
// Width for History Buffer Indexing
constexpr int BUF_IDX_W  = clog2(MAX_PATTERN_LEN_TOTAL + BYTES_PER_BEAT);
// Width for Pattern Lengths
constexpr int K_W        = clog2(MAX_PATTERN_LEN_TOTAL);
// Width for Pattern Offset within a Partition
constexpr int PAT_OFFSET_W = clog2(MAX_PATTERNS_PER_PART);
// Width for Global Match IDs
constexpr int MATCH_ID_W = clog2(TOTAL_NUM_PATTERNS + 1);
// Width for Partition Indexing
constexpr int PART_IDX_W   = clog2(NUM_OF_PARTITIONS);


// type aliases
using byte_i_t    = ap_uint<BYTES_I_W>;
using buf_idx_t     = ap_uint<BUF_IDX_W>;
using k_t         = ap_uint<K_W>;
using pat_offset_t  = ap_uint<PAT_OFFSET_W>;
using match_id_t  = ap_uint<MATCH_ID_W>;
using part_idx_t    = ap_uint<PART_IDX_W>;


typedef ap_axiu<DWIDTH, 1, 1, TDWIDTH> pkt;

#ifdef __cplusplus
extern "C" {
#endif

void krnl_proj(
    hls::stream<pkt> &in_stream, 
    hls::stream<pkt> &out_stream  
);

#ifdef __cplusplus
} 
#endif

#endif
