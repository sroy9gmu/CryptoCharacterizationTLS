wolfSSL Simple Echo Client/Server using TLS 1.3
===============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 specification: https://datatracker.ietf.org/doc/html/rfc8446 

    2. v1.3 support: https://www.wolfssl.com/docs/tls13/

    3. Handshake overview: https://www.wolfssl.com/documentation/manuals/wolfssl/appendix04.html
    
    3. Example: https://github.com/wolfSSL/wolfssl-examples/tree/master/tls

Issues

    1. https://github.com/wolfSSL/wolfssl/issues/8793

Installation

    1. git clone https://github.com/wolfSSL/wolfssl.git

    2. ./autogen.sh (for raspbian, sudo apt-get install autoconf libtool)

    3. FFDH, RSA-PSS:   
        ./configure CFLAGS="-DNO_AES_192 -DNO_AES_256 -DWOLFSSL_SP_NO_256" --enable-aesgcm --enable-aesctr --enable-tls13 --enable-rsapss LIBS=-lm
        ./configure CFLAGS="-DNO_AES_192 -DNO_AES_256 -DWOLFSSL_SP_NO_256" --disable-aesgcm --disable-aescbc --enable-aesccm --enable-aesctr --enable-tls13 --enable-rsapss LIBS=-lm

       ECDH, DSA:   
        ./configure CFLAGS="-DNO_AES_192 -DNO_AES_256 -DNO_RSA" --enable-tls13 --disable-dh --enable-supportedcurves --enable-aesgcm --enable-aesctr --enable-dsa LIBS=-lm

    4. make

    5. sudo make install

Security Parameters

    1. 128-bit:  AES-GCM-128, DH/DSA (L = 3072, N = 256), RSA-3072, ECC (f = 256 - 383), SHA-256

Steps

    1. Refer certificate and key generation steps in OpenSSL directory.
    
    2. Start SSL server and client in separate windows

        cd wolfssl

        FFDH, RSA-PSS:        
        ./examples/server/server -v 4 -c ../CryptoCharacterizationTLS/OpenSSL/rsa_srv_cert.pem -k ../CryptoCharacterizationTLS/OpenSSL/rsa_srv_pvt.pem -A ../CryptoCharacterizationTLS/OpenSSL/rsa_cert.pem -D ../CryptoCharacterizationTLS/OpenSSL/dh_param.pem
        ./examples/client/client -h 127.0.0.1 -v 4 -c ../CryptoCharacterizationTLS/OpenSSL/rsa_cli_cert.pem -k ../CryptoCharacterizationTLS/OpenSSL/rsa_cli_pvt.pem -A ../CryptoCharacterizationTLS/OpenSSL/rsa_cert.pem -y

        ECDH, ECDSA:
        ./examples/server/server -v 4 -c ../CryptoCharacterizationTLS/OpenSSL/dsa_srv_cert.pem -k ../CryptoCharacterizationTLS/OpenSSL/dsa_srv_pvt.pem -A ../CryptoCharacterizationTLS/OpenSSL/dsa_cert.pem
        ./examples/client/client -h 127.0.0.1 -v 4 -c ../CryptoCharacterizationTLS/OpenSSL/dsa_cli_cert.pem -k ../CryptoCharacterizationTLS/OpenSSL/dsa_cli_pvt.pem -A ../CryptoCharacterizationTLS/OpenSSL/dsa_cert.pem -y

Issues

    1. Cannot open shared object file: 
    
        Add this line to ~/.bashrc and relaunch shell: LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
        Run: sudo ldconfig
    
Results

    1. Key Exchange: 

        FFDH
        SSL curve name is FFDHE_2048
        key_exchange:  (len=256)
        GeneratePublicDh, wolfcrypt/src/dh.c, 1302
        _sp_exptmod_mont_ex, wolfcrypt/src/sp_int.c, 13237

        ECDH

    2. Signing: 

        RSA-PSS
        wc_RsaPSS_Sign_ex, wolfcrypt/src/rsa.c, 4316
        RsaFunctionPrivate, wolfcrypt/src/rsa.c, 2527

        ToDo: implement rounds > 1.

        DSA        

    3. Encryption: 
        AES_GCM_encrypt_C, wolfcrypt/src/aes.c, 8563

        ToDo: implement rounds > 1.
    
    4. Hashing: 
        Sha256Update, wolfcrypt/src/sha256.c, 1325


