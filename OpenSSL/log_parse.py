import sys
import re
import math

kwds_algo = ['NamedGroup', 'Signature Algorithm', 'CIPHER is'] # Key exchange, signature, encryption and hashing
kx_algo_g = ''
sg_algo_g = ''
en_dg_algo_g = ''
names = []
times = {}
times_mean = {}
max_cnt = 50

def geometric_mean(data):
    """
    Calculate the geometric mean of a list of numbers.

    Args:
      data: A list of numbers.

    Returns:
      The geometric mean of the numbers in the list.
    
    Raises:
      ValueError: If the list is empty or contains non-positive numbers.
    """
    if not data:
        raise ValueError("Cannot calculate geometric mean of an empty list.")
    
    for d in data:
        if not isinstance(d, int):
            d = int(float(d))

    product = 1
    i_max = 1
    if len(data) > max_cnt:
        i_max = max_cnt
    else:
        i_max = len(data)

    for i in range(i_max):
        d = data[i]
        if data[i] <= 0:
            raise ValueError("All numbers must be positive to calculate geometric mean.")
        product *= data[i]

    return math.pow(product, 1/i_max)

    # Example usage
    """ data = [2, 8, 32]
    try:
    geo_mean = geometric_mean(data)
    print(f"The geometric mean is: {geo_mean}")  # Output: 8.0
    except ValueError as e:
    print(f"Error: {e}") """

def get_kx_algo(l):
    r = None
    w_l = l.split(' ')
    for w in w_l:
        if 'dh' in w:
            r = w

    return r

def get_sg_algo(l):
    r = None
    w_l = l.split(' ')
    for w in w_l:
        if 'rsa' in w or 'dsa' in w:
            r = w

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
    time_str2 = 'Duration for'

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
                    if wd != 'inf' and wd != '0':
                        times[name].append(int(float(wd)))
        elif time_str2 in line:
            for name in names:
                if name in line:
                    line_wds = line.split()
                    wd = line_wds[7]
                    if wd != 'inf' and wd != '0':
                        times[name].append(int(wd))

    for index, (key, value) in enumerate(times.items()):
        times_mean[key] = geometric_mean(value)

    print(times_mean)

    with open(outfile, "w") as f:
        f.write("List of crypto algorithms (direct invocation).\n")
        f.write(f"Key Exchange: {kx_algo_g}\n")
        f.write(f"Signature: {sg_algo_g}\n")
        f.write(f"Encryption and Hashing: {en_dg_algo_g}\n\n")
        f.write("Mean execution time of crypto algorithms (direct invocation).\n")
        f.write("Key Exchange:\n")
        f.write("Signature:\n")
        f.write("Encryption:\n")
        f.write("Hashing:\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input log file> <output result file>")
    else:
        main(sys.argv[1], sys.argv[2])
