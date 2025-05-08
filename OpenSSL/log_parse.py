import sys
import re

kwds_algo = ['NamedGroup', 'Signature Algorithm', 'CIPHER is'] # Key exchange, signature, encryption and hashing
kx_algo_g = ''
sg_algo_g = ''
en_dg_algo_g = ''

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

    global kx_algo_g, sg_algo_g, en_dg_algo_g

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
