GnuTLS Simple Echo Client/Server using TLS 1.3
==============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 specification: https://datatracker.ietf.org/doc/html/rfc8446 

    2. Wiki: https://gitlab.com/gnutls/gnutls

    2. Code
    
        Server: https://gitlab.com/gnutls/gnutls/-/blob/5c1a38f7e6943cb21cbca4d220beb93cbf57397f/doc/examples/ex-serv-x509.c
        Client: https://gitlab.com/gnutls/gnutls/-/blob/5c1a38f7e6943cb21cbca4d220beb93cbf57397f/doc/examples/ex-client-x509-3.1.c
    
    3. (OPTIONAL) Generating certificates: https://help.ubuntu.com/community/GnuTLS

    4. Tutorial: https://x509errors.org/guides/gnutls
    
    5. Manual: https://gnutls.org/manual/html_node/index.html

    6. DH parameters: https://www.gnutls.org/manual/html_node/Parameter-generation.html

Steps

    1. (DEBUG/LOGGING purpose only) Compile Nettle library separately using below steps:

        git clone https://gitlab.com/gnutls/gnutls.git   
        cd gnutls
        ./bootstrap     
        cd devel/nettle
        ./.bootstrap
        ./configure LIBS=-lm
        make
        sudo make install
        sudo cp /usr/local/lib64/libhogweed* /usr/lib/<TARGET ARCHITECTURE>-linux-gnu
        sudo cp /usr/local/lib64/libnettle* /usr/lib/<TARGET ARCHITECTURE>-linux-gnu
        sudo ldconfig
        cd ../..

    2. Compile GnuTLS library and install shared libraries:

        ./configure
        make
        sudo make install

    3. If facing missing 'trousers' library error, specify location as /usr/local
        ./configure --with-trousers-lib=/usr/local/

    4. Additional packages required: sudo apt-get install zlib1g-dev libzstd-dev libbrotli-dev make gnutls-bin

    5. Refer certificate generation steps in OpenSSL -> TLS.

    <!-- 6. cd TLS
        NOTE: Comment out the server certificate verifcation in client code for test purpose.

    7. Compile:
        gcc server-x509.c -o server -lgnutls
        gcc client-x509.c tcp.c -o client -lgnutls

    8. Execute:
        Start server process in one window:  ./server > server.txt
        Start client process in another window of same PC: ./client 127.0.0.1 > client.txt -->

    6. cd src
        Refer gnutls-serv and gnutls-cli commands in https://gnutls.org/manual/html_node/Other-included-programs.html.

Results

    1. Key Exchange: ecc_mul_a() from devel/nettle/ecc-mul-a.c

    2. Signing: rsa_compute_root_tr() from devel/nettle/rsa-sign-tr.c

    3. Encryption: 
    
    4. Hashing: 