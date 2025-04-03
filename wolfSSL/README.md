wolfSSL Simple Echo Client/Server using TLS 1.3
===============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 specification: https://datatracker.ietf.org/doc/html/rfc8446 

    2. v1.3 support: https://www.wolfssl.com/docs/tls13/

    3. Handshake overview: https://www.wolfssl.com/documentation/manuals/wolfssl/appendix04.html
    
    3. Example: https://github.com/wolfSSL/wolfssl-examples/tree/master/tls

Installation

    1. git clone https://github.com/wolfSSL/wolfssl.git

    2. ./autogen.sh (for raspbian, sudo apt-get install autoconf libtool)

    3. ./configure --enable-aesgcm --enable-aesctr --enable-tls13 LIBS=-lm

    4. make

    5. sudo make install

Steps

    1. Refer certificate generation steps in OpenSSL -> TLS.
    
    2. Start server process in one window:

        ./examples/server/server -D ../wolfSSL/TLS/dhparam.pem -c ../wolfSSL/TLS/server-cert.pem -k ../wolfSSL/TLS/server-key.pem -v 4 -A ../wolfSSL/TLS/ca-cert.pem      

        ./server-tls13 [For echo only]

    3. Start client process in another window of same PC:

        ./examples/client/client -h 127.0.0.1 -v 4 -c ../wolfSSL/TLS/client-cert.pem -k ../wolfSSL/TLS/client-key.pem -A ../wolfSSL/TLS/ca-cert.pem 

        ./client-tls13 127.0.0.1 [For echo only]

Issues

    1. Cannot open shared object file: 
    
        Add this line to ~/.bashrc and relaunch shell: LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
        Run: sudo ldconfig
    
Results

    1. Key Exchange: ecc_mulmod() from wolfcrypt/src/ecc.c

    2. Signing: RsaFunctionPrivate() from wolfcrypt/src/rsa.c

    3. Encryption: 
    
    4. Hashing: 



