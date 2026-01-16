import sys
import math

# --- CONFIGURATION ---
PARTITION_BYTE_LIMIT = 8191
SRL_LIMIT_A = 32
SRL_LIMIT_B = 64

def parse_snort_line(line):
    line = line.strip()
    if not line: return None
    # RAW LITERAL MODE
    byte_array = [ord(c) for c in line]
    return byte_array

def remove_duplicates(all_patterns):
    unique_patterns = []
    seen = set()
    for p in all_patterns:
        t = tuple(p)
        if t not in seen:
            unique_patterns.append(p)
            seen.add(t)
    return unique_patterns

def get_pattern_group(length):
    if length <= SRL_LIMIT_A: return 0
    if length <= SRL_LIMIT_B: return 1
    return 2

def distribute_group(patterns, num_partitions):
    """
    Distributes a list of patterns across 'num_partitions' to balance load.
    Returns a list of lists (partitions).
    """
    if num_partitions < 1: return []
    if not patterns: return [[] for _ in range(num_partitions)]
    
    # Target bytes per partition to achieve perfect balance
    total_bytes = sum(len(p) for p in patterns)
    target_bytes = total_bytes / num_partitions
    
    partitions = []
    current_part = []
    current_bytes = 0
    
    for p in patterns:
        p_len = len(p)
        
        # Check hard hardware limit
        if (current_bytes + p_len) > PARTITION_BYTE_LIMIT:
            partitions.append(current_part)
            current_part = [p]
            current_bytes = p_len
            continue
            

        if current_bytes >= target_bytes and len(partitions) < (num_partitions - 1):
            partitions.append(current_part)
            current_part = [p]
            current_bytes = p_len
        else:
            current_part.append(p)
            current_bytes += p_len
            
    partitions.append(current_part)
    
    return partitions

def pack_partitions_balanced(patterns, total_partitions):
    # Sort and Bucketize
    patterns.sort(key=len)
    
    buckets = [[], [], []] # 0: SRL32, 1: SRL64, 2: Long
    bucket_bytes = [0, 0, 0]
    
    for p in patterns:
        g = get_pattern_group(len(p))
        buckets[g].append(p)
        bucket_bytes[g] += len(p)
        
    total_bytes = sum(bucket_bytes)
    if total_bytes == 0: return [[] for _ in range(total_partitions)]

    allocations = [0, 0, 0]
    remaining_partitions = total_partitions
    
    # Ensure every non-empty bucket gets 1
    for i in range(3):
        if bucket_bytes[i] > 0:
            allocations[i] = 1
            remaining_partitions -= 1
            
    if remaining_partitions < 0:
        print("Error: Not enough partitions for the 3 distinct groups (SRL32, SRL64, Long).")
        return [[] for _ in range(total_partitions)]
        
    # Distribute remaining based on weight
    if remaining_partitions > 0:
        for i in range(3):
            if bucket_bytes[i] > 0:
                share = (bucket_bytes[i] / total_bytes) * total_partitions
                extra = int(round(share)) - 1
                if extra > 0:
                    take = min(extra, remaining_partitions)
                    allocations[i] += take
                    remaining_partitions -= take

    # Dump any leftover partitions into the heaviest bucket
    # (Or the one with the most patterns to reduce count)
    while remaining_partitions > 0:
        # Find index with max bytes
        idx = bucket_bytes.index(max(bucket_bytes))
        allocations[idx] += 1
        remaining_partitions -= 1

    print(f"\n--- ALLOCATION STRATEGY ---")
    print(f"SRL32 Group: {bucket_bytes[0]} bytes -> {allocations[0]} partitions")
    print(f"SRL64 Group: {bucket_bytes[1]} bytes -> {allocations[1]} partitions")
    print(f"LONG  Group: {bucket_bytes[2]} bytes -> {allocations[2]} partitions")
    print(f"---------------------------\n")

    final_partitions = []
    
    for i in range(3):
        if allocations[i] > 0:
            parts = distribute_group(buckets[i], allocations[i])
            final_partitions.extend(parts)
            
    while len(final_partitions) < total_partitions:
        final_partitions.append([])

    assert len(final_partitions) <= total_partitions, f"Use a higher number of partitions! Suggested min: {len(final_partitions)}"
        
    return final_partitions

def print_partition_stats(partitions):
    print(f"{'Part #':<8} | {'Range':<10} | {'Count':<6} | {'Avg Len':<8} | {'Max Len':<8} | {'Bytes':<12}")
    print("-" * 70)
    
    for i, p_list in enumerate(partitions):
        if not p_list:
            print(f"{i:<8} | {'EMPTY':<10} | {0:<6} | {0:<8} | {0:<8} | {0:<12}")
            continue

        count = len(p_list)
        lens = [len(p) for p in p_list]
        avg = sum(lens) / count
        mx = max(lens)
        mn = min(lens)
        total_b = sum(lens)
        
        print(f"{i:<8} | {(str(mn)+'-'+str(mx)):<10} | {count:<6} | {avg:<8.1f} | {mx:<8} | {total_b:<12}")
    print("-" * 70)

def generate_hpp(input_file, output_file, total_partitions):
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f: 
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        return

    all_patterns = []
    for line in lines:
        p = parse_snort_line(line)
        if p: all_patterns.append(p)

    unique_patterns = remove_duplicates(all_patterns)
    # Sort Shortest -> Longest
    unique_patterns.sort(key=len)
    
    # --- BALANCED PACKING ---
    final_split = pack_partitions_balanced(unique_patterns, total_partitions)
    
    # --- PRINT STATS ---
    print_partition_stats(final_split)

    # --- CALCULATE HEADER METRICS ---
    max_patterns_per_part = 0
    max_row_byte_size = 0
    max_global_len = 0
    
    length_matrix = []
    offset_matrix = []
    packed_data = []
    max_len_per_part = []
    num_patterns_per_part = []

    for p_list in final_split:
        row_dat = []
        row_len = []
        row_off = []
        curr_off = 0
        
        current_max_len = 0
        
        for p in p_list:
            row_dat.extend(p)
            row_len.append(len(p))
            row_off.append(curr_off)
            curr_off += len(p)
            
            if len(p) > max_global_len: max_global_len = len(p)
            if len(p) > current_max_len: current_max_len = len(p)
            
        # Update Globals
        if len(p_list) > max_patterns_per_part: max_patterns_per_part = len(p_list)
        if len(row_dat) > max_row_byte_size: max_row_byte_size = len(row_dat)
        
        packed_data.append(row_dat)
        length_matrix.append(row_len)
        offset_matrix.append(row_off)
        max_len_per_part.append(current_max_len)
        num_patterns_per_part.append(len(p_list))

    # --- WRITE HEADER ---
    with open(output_file, 'w') as f:
        f.write(f"#ifndef PATTERNS_HPP\n#define PATTERNS_HPP\n#include <ap_int.h>\n\n")

        f.write(f"const int NUM_OF_PARTITIONS = {total_partitions};\n")
        
        f.write(f"const int MAX_ROW_SIZE = {max(max_row_byte_size, 1)};\n") 
        f.write(f"const int MAX_PATTERNS_PER_PART = {max(max_patterns_per_part, 1)};\n")
        f.write(f"const int TOTAL_NUM_PATTERNS = {len(unique_patterns)};\n")
        f.write(f"const int MAX_PATTERN_LEN_TOTAL = {max_global_len};\n\n")

        # --- DATA MATRIX ---
        f.write(f"const unsigned char PATTERN_DATA[{total_partitions}][{max(max_row_byte_size, 1)}] = {{\n")
        for row in packed_data:
            padded = row + [0] * (max_row_byte_size - len(row))
            if not padded: padded = [0]
            f.write("    {" + ", ".join([f"0x{b:02X}" for b in padded]) + "},\n")
        f.write("};\n\n")

        # --- LENGTH MATRIX ---
        f.write(f"const int PATTERN_LENGTHS[{total_partitions}][{max(max_patterns_per_part, 1)}] = {{\n")
        for row in length_matrix:
            padded = row + [0] * (max_patterns_per_part - len(row))
            if not padded: padded = [0]
            f.write("    {" + ", ".join(map(str, padded)) + "},\n")
        f.write("};\n\n")

        # --- OFFSET MATRIX ---
        f.write(f"const int PATTERN_OFFSETS[{total_partitions}][{max(max_patterns_per_part, 1)}] = {{\n")
        for row in offset_matrix:
            padded = row + [0] * (max_patterns_per_part - len(row))
            if not padded: padded = [0]
            f.write("    {" + ", ".join(map(str, padded)) + "},\n")
        f.write("};\n\n")

        # --- UTILITY ARRAYS ---
        f.write(f"const int NUM_PATTERNS_MATRIX[{total_partitions}] = {{ ")
        f.write(", ".join(map(str, num_patterns_per_part)))
        f.write(" };\n\n")

        f.write(f"const int MAX_LEN_IN_PARTITION[{total_partitions}] = {{ ")
        f.write(", ".join(map(str, max_len_per_part)))
        f.write(" };\n\n")

        f.write("#endif\n")
        print(f"\nHeader successfully written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <input> <output> <partitions>")
    else:
        generate_hpp(sys.argv[1], sys.argv[2], int(sys.argv[3]))