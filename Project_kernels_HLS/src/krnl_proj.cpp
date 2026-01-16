#include "krnl_proj.h"
#include "hls_stream.h"
#include "patterns.h"

extern "C"
{
  void krnl_proj(hls::stream<pkt> &in_stream, hls::stream<pkt> &out_stream)
  {
    #pragma HLS INTERFACE axis port = in_stream
    #pragma HLS INTERFACE axis port = out_stream
    #pragma HLS INTERFACE ap_ctrl_none port = return

    

    pkt in_pkt;
    pkt out_pkt;

    #pragma HLS PIPELINE II=1

    in_stream.read(in_pkt);

    out_pkt.data = 0;
    out_pkt.dest = in_pkt.dest;
    out_pkt.keep = in_pkt.keep;
    out_pkt.last = in_pkt.last;

    bool match[NUM_OF_PARTITIONS][MAX_PATTERNS_PER_PART];



    ap_uint<256> decoder_out[BYTES_PER_BEAT];
    bytes_decoding: for (byte_i_t s = 0; s < BYTES_PER_BEAT; s++) {
      #pragma HLS UNROLL
      ap_uint<8> decoded_byte = in_pkt.data.range((s + 1)*8 - 1, s * 8);
      decoder_out[s] = 0;
      decoder_out[s].set(decoded_byte, 1);
    }

    static ap_uint<256> history_buffer[MAX_PATTERN_LEN_TOTAL + BYTES_PER_BEAT];
    fill_history: for (int i = 0; i < BYTES_PER_BEAT; i++) {
      #pragma HLS UNROLL
      history_buffer[MAX_PATTERN_LEN_TOTAL + i] = decoder_out[i];
    }
    
    process_beat_loop: for (byte_i_t s = 0; s < BYTES_PER_BEAT; s++) {
      #pragma HLS UNROLL
      //NORMAL PARTITIONS
      partition_loop: for (part_idx_t n = 0; n < NUM_OF_PARTITIONS; n++) {
        #pragma HLS UNROLL
        pattern_match:for (match_id_t p = 0; p < NUM_PATTERNS_MATRIX[n]; p++) {
          #pragma HLS UNROLL
          
          bool local_match = true;
          
          for (k_t k = 0; k < PATTERN_LENGTHS[n][p]; k++) {
            #pragma HLS UNROLL
            int p_offset = PATTERN_OFFSETS[n][p] + (PATTERN_LENGTHS[n][p] - 1 - k);

            ap_uint<8> required_char = PATTERN_DATA[n][p_offset];
            buf_idx_t delayed_offset = MAX_PATTERN_LEN_TOTAL + s - k;
            ap_uint<256> delayed_decoded = history_buffer[delayed_offset];

            if (!delayed_decoded[required_char]) {
              local_match = false;
            }
          }
          if (s==0)
            match[n][p] = (PATTERN_LENGTHS[n][p] > 0) && local_match;
          else 
            match[n][p] |= (PATTERN_LENGTHS[n][p] > 0) && local_match;
        }
      }

      
    }

    update_history: for (buf_idx_t i = 0; i < MAX_PATTERN_LEN_TOTAL; i++) {
      #pragma HLS UNROLL
      history_buffer[i] = history_buffer[i + BYTES_PER_BEAT];
    }

    match_id_t output[NUM_OF_PARTITIONS];
    bool found_part[NUM_OF_PARTITIONS];

    match_id_t offset[NUM_OF_PARTITIONS];
    offset[0] = 0;
    
    offset_calculator:for (part_idx_t i = 1; i < NUM_OF_PARTITIONS; i++){
      #pragma HLS UNROLL
      offset[i] = offset[i-1] + NUM_PATTERNS_MATRIX[i - 1];
    }

    match_check:for(part_idx_t n = 0 ; n < NUM_OF_PARTITIONS; n++){
      #pragma HLS UNROLL
      found_part[n] = false;
      for (pat_offset_t p = 0; p < NUM_PATTERNS_MATRIX[n]; p++){
        #pragma HLS UNROLL
        bool found = match[n][p];
        if (found){
            output[n] = p + offset[n];
            found_part[n] = true;
        }
      }
    } 

    output_build: for(part_idx_t n = 0 ; n < NUM_OF_PARTITIONS; n++){
      #pragma HLS UNROLL
      if(found_part[n])
      out_pkt.data = output[n];
    }

    
    out_stream.write(out_pkt);

    
  }
}