# Crypto Libraries on IoT devices: A Detailed Characterization of Performance, Energy Efficiency, and Memory Footprint

This repository contains software to characterize C-language based crypto libraries on microprocessor-based IoT devices. 

The following crypto libraries were analysed:

    1. OpenSSL
    2. wolfSSL
    3. GnuTLS
    4. MbedTLS

The following Raspberry Pi devices and their OS versions were used:

    1. ZeroW - Linux raspberrypi 6.1.19+ armv6l GNU/Linux
    2. 3B+ - Linux raspberrypi 6.1.21-v8+ aarch64 GNU/Linux
    3. 4B - Linux raspberrypi 6.1.21-v8+ aarch64 GNU/Linux


Links

    1. Security Levels - section 5.6.1 table 2
        https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf

Steps

    1. Traditional DH key exchange + RSA signing + 128 bit security level ciphers (AES + SHA)
        If RSA PSS not available, use default one. Refer GnuTLS issue.
            Add encoding step has minimal overhead.

    2. ECDH key exchange + ECDSA signing + 128 bit security level ciphers (AES + SHA)

    3. Vary security level 

