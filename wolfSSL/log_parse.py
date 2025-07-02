import sys
import re
import math
from statistics import geometric_mean

kwds_algo = ['curve name', 'Sign_ex', 'cipher suite'] # Key exchange, signature, encryption and hashing
kx_algo_g = ''
sg_algo_g = ''
en_dg_algo_g = ''
names = []
times = {}
times_sum = {}
times_cnt = {}
times_mean = {}

def get_kx_algo(l):
    r = None
    w_l = l.split(' ')
    for w in w_l:
        if 'DH' in w:
            r = w

    return r

def get_sg_algo(l):
    r = None
    w_l = l.split(' ')
    for w in w_l:
        if 'Rsa' in w or 'Dsa' in w:
            w_m = w.split('_')
            r = w_m[1]

    return r

def get_en_dg_algo(l):
    r = None
    w_l = l.split(' ')
    for w in w_l:
        if 'TLS' in w:
            w_m = w.split('_', 1)
            r = w_m[1]

    return r

def main(infile, outfile):
    """
    This is the main function.
    It takes input log file and prints results to output file.
    """
    print(f"Input log file: {infile}")
    print(f"Output result file: {outfile}")

    global kx_algo_g, sg_algo_g, en_dg_algo_g, names, times
    time_str1 = 'Mean execution time of function'
    time_str2 = 'Duration of'

    with open(infile, "r") as f:
        in_str = f.read()

    in_lines = in_str.splitlines()

    for line in in_lines:
        for i in range(len(kwds_algo)):
            kwd = kwds_algo[i]
            if kwd in line:
                if i == 0 and not(kx_algo_g):
                    kx_algo_g = get_kx_algo(line)
                elif i == 1 and not(sg_algo_g):
                    sg_algo_g = get_sg_algo(line)
                elif i == 2 and not(en_dg_algo_g):
                    en_dg_algo_g = get_en_dg_algo(line)
            if kx_algo_g != '' and sg_algo_g != '' and en_dg_algo_g != '':
                break

        if time_str1 in line or time_str2 in line:
            line_wds = line.split()
            name = line_wds[5].rstrip(",")
            if name not in names:
                names.append(name)

    for name in names:
        times[name] = []

    for line in in_lines:
        if time_str1 in line:
            for name in names:
                if name in line:
                    line_wds = line.split()
                    wd = line_wds[9]
                    if wd != 'inf' and wd != '0' and wd != '0.000000':
                        times[name].append(float(wd))
        elif time_str2 in line:
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
                times_cnt[key] = len(value)
                times_mean[key] = geometric_mean(value)
                total_dur += dur_sum

    with open(outfile, "w") as f:
        f.write("List of crypto algorithms (direct invocation).\n")
        f.write(f"Key Exchange: {kx_algo_g}\n")
        f.write(f"Signature: {sg_algo_g}\n")
        f.write(f"Encryption and Hashing: {en_dg_algo_g}\n\n")
        f.write(f"Total execution time of all direct invocations: {"{:,.2f}".format(total_dur)}\n")
        f.write("\nBreakdown of total execution time (direct invocation).\n")
        for index, (key, value) in enumerate(times_sum.items()):
            f.write(f"Function name: {key}, time (microseconds): {"{:,.2f}".format(value)}\n")
        f.write("\nNumber of direct invocations.\n")
        for index, (key, value) in enumerate(times_cnt.items()):
            f.write(f"Function name: {key}, time (microseconds): {"{:,.2f}".format(value)}\n")
        f.write("\nExecution time of each direct invocation.\n")
        for index, (key, value) in enumerate(times_mean.items()):
            f.write(f"Function name: {key}, time (microseconds): {"{:,.2f}".format(value)}\n")

        f.write("\n**************Debug**************\n")
        f.write(f"Key Exchange: \n")
        f.write(str(times['_sp_exptmod_mont_ex']))
        s = "{:,.2f}".format(times_sum['_sp_exptmod_mont_ex'])
        f.write(f"\ntotal duration = {s} microseconds\n")            

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input log file> <output result file>")
    else:
        main(sys.argv[1], sys.argv[2])
