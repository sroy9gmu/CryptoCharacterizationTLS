import sys
import re
import math

names = []
times = {}
times_sum = {}

def main(infile, outfile):
    """
    This is the main function.
    It takes input log file and prints results to output file.
    """
    print(f"Input log file: {infile}")
    print(f"Output result file: {outfile}")

    global names, times    
    time_str = 'Duration of'

    with open(infile, "r") as f:
        in_str = f.read()

    in_lines = in_str.splitlines()

    for line in in_lines:
        if time_str in line:
            line_wds = line.split()
            name = line_wds[5].rstrip(",")
            if name not in names:
                names.append(name)

    for name in names:
        times[name] = []

    for line in in_lines:
        if time_str in line:
            for name in names:
                if name in line:
                    line_wds = line.split()
                    wd = line_wds[7]
                    if wd != 'inf' and wd != '0' and wd != '0.000000':
                        times[name].append(float(wd))

    total_dur = 0
    for index, (key, value) in enumerate(times.items()):  
        if value != []: 
            dur_sum = sum(value)  
            if dur_sum != 0:   
                times_sum[key] = dur_sum
                total_dur += dur_sum

    with open(outfile, "w") as f:
        f.write(f"Total execution time of all direct invocations: {"{:,.2f}".format(total_dur)}\n")
        f.write("Breakdown of total execution time (direct invocation).\n")
        for index, (key, value) in enumerate(times_sum.items()):
            f.write(f"Function name: {key}, time (microseconds): {"{:,.2f}".format(value)}\n")

        f.write("\n**************Debug**************\n")
        f.write(f"Key Exchange: \n")
        f.write(str(times['_nettle_rsa_sec_compute_root_tr']))
        s = "{:,.2f}".format(times_sum['_nettle_rsa_sec_compute_root_tr'])
        f.write(f"\ntotal duration = {s} microseconds\n")            

            
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input log file> <output result file>")
    else:
        main(sys.argv[1], sys.argv[2])
