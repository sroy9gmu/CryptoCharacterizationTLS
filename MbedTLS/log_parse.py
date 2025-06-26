import sys
import re
import math
from statistics import geometric_mean

names = []
times = {}
times_sum = {}
times_mean = {}

pat = r'ssl_tls13'
ssl_kwds = ['process client hello', 'write server hello',\
             'write encrypted extensions', 'write certificate request', 'write server certificate',\
                  'write certificate verify', 'write server finished']
times_ssl = {}
times_sum_ssl = {}
kwd_dbg = 'mbedtls_mpi_exp_mod_optionally_safe'

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
                times_mean[key] = geometric_mean(value)
                total_dur += dur_sum

    for wd in ssl_kwds:
        times_ssl[wd] = []

    cnt = 0
    cnt_max = len(ssl_kwds) - 2
    kwd = ssl_kwds[cnt]
    for line in in_lines: 
        line_wds = line.split()
        if len(line_wds) > 0:            
            if time_str in line and kwd_dbg in line:            
                wd = line_wds[7]
                if wd != 'inf' and wd != '0' and wd != '0.000000':
                    times_ssl[kwd].append(float(wd))                
            elif re.match(pat, line_wds[0]) != None:
                tmp = line_wds[0].split('_',2)[2].replace('_', ' ').rstrip(',')         
                if re.match(tmp, ssl_kwds[cnt + 1]) != None and cnt < cnt_max:
                    cnt += 1
                    kwd = ssl_kwds[cnt]

    for index, (key, value) in enumerate(times_ssl.items()):  
        if value != []:  
            sum_dur = sum(value)    
            if sum_dur != 0:
                times_sum_ssl[key] = sum_dur

    with open(outfile, "w") as f:
        f.write(f"Total execution time of all direct invocations: {"{:,.2f}".format(total_dur)}\n")
        f.write("Breakdown of total execution time (direct invocation).\n")
        for index, (key, value) in enumerate(times_sum.items()):
            f.write(f"Function name: {key}, time (microseconds): {"{:,.2f}".format(value)}\n")
        f.write("\nExecution time of each direct invocation.\n")
        for index, (key, value) in enumerate(times_mean.items()):
            f.write(f"Function name: {key}, time (microseconds): {"{:,.2f}".format(value)}\n")

        f.write("\n**************Debug**************\n")
        
        f.write(f"Breakdown of total execution time of {kwd_dbg}.\n")
        for index, (key, value) in enumerate(times_sum_ssl.items()):
            v = "{:,.2f}".format(value)
            f.write(f"SSL state: {key}, time (microseconds): {v}\n")
        f.write(f"\nList of execution times of {kwd_dbg}\n")
        for index, (key, value) in enumerate(times_ssl.items()):
            f.write(f"SSL state: {key}, time (microseconds): {value}\n")          

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input log file> <output result file>")
    else:
        main(sys.argv[1], sys.argv[2])
