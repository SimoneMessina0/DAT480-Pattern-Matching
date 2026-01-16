import sys
import math

PARTITION_BYTE_LIMIT = 8191
SRL_LIMIT_A = 32
SRL_LIMIT_B = 64

def parse_snort_line(line):
    line = line.strip()
    if not line: return None
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
    if num_partitions < 1: return []
    if not patterns: return [[] for _ in range(num_partitions)]
    
    total_bytes = sum(len(p) for p in patterns)
    target_bytes = total_bytes / num_partitions
    
    partitions = []
    current_part = []
    current_bytes = 0
    
    for p in patterns:
        p_len = len(p)
        
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
    patterns.sort(key=len)
    
    buckets = [[], [], []] 
    bucket_bytes = [0, 0, 0]
    
    for p in patterns:
        g = get_pattern_group(len(p))
        buckets[g].append(p)
        bucket_bytes[g] += len(p)
        
    total_bytes = sum(bucket_bytes)
    if total_bytes == 0: return [[] for _ in range(total_partitions)]

    allocations = [0, 0, 0]
    remaining_partitions = total_partitions
    
    for i in range(3):
        if bucket_bytes[i] > 0:
            allocations[i] = 1
            remaining_partitions -= 1
            
    if remaining_partitions < 0:
        print("Error: Not enough partitions for the 3 distinct groups (SRL32, SRL64, Long).")
        return [[] for _ in range(total_partitions)]
        
    if remaining_partitions > 0:
        for i in range(3):
            if bucket_bytes[i] > 0:
                share = (bucket_bytes[i] / total_bytes) * total_partitions
                extra = int(round(share)) - 1
                if extra > 0:
                    take = min(extra, remaining_partitions)
                    allocations[i] += take
                    remaining_partitions -= take

    while remaining_partitions > 0:
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

def generate_txt_map(input_file, output_file, total_partitions):
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
    unique_patterns.sort(key=len)
    
    final_split = pack_partitions_balanced(unique_patterns, total_partitions)
    
    print_partition_stats(final_split)

    current_global_base = 0
    
    with open(output_file, 'w') as f:
        for p_list in final_split:
            for i, p_bytes in enumerate(p_list):
                global_id = current_global_base + i
                
                p_str = "".join([chr(b) for b in p_bytes])
                
                f.write(f"{p_str} {global_id}\n")
            
            current_global_base += len(p_list)

    print(f"Successfully generated sorted map: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 sort_and_map.py <input> <output> <partitions>")
    else:
        generate_txt_map(sys.argv[1], sys.argv[2], int(sys.argv[3]))