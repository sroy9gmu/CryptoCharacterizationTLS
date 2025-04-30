GnuTLS Simple Echo Client/Server using TLS 1.3
==============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 specification: https://datatracker.ietf.org/doc/html/rfc8446 

    2. Wiki: https://gitlab.com/gnutls/gnutls

    3. gnutls-serv and gnutls-cli commands: https://gnutls.org/manual/html_node/Other-included-programs.html.

    4. Priority strings: https://gnutls.org/manual/html_node/Priority-Strings.html#Priority-Strings

    5. Stable release: https://www.gnutls.org/download.html


Issues

    1. gnutls with allowlisting doesn't allow enabling sigalgs with priority strings (OPEN)
        
        https://gitlab.com/gnutls/gnutls/-/issues/1681 


SInstallation

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

    <!-- 6. cd TLS
        NOTE: Comment out the server certificate verifcation in client code for test purpose.

    7. Compile:
        gcc server-x509.c -o server -lgnutls
        gcc client-x509.c tcp.c -o client -lgnutls

    8. Execute:
        Start server process in one window:  ./server > server.txt
        Start client process in another window of same PC: ./client 127.0.0.1 > client.txt -->

    5. Start SSL server and client in separate windows

        FFDH, RSA-PSS:
        ./gnutls-serv --dhparams=../../CryptoCharacterizationTLS/OpenSSL/dh_param.pem --x509cafile=../../CryptoCharacterizationTLS/OpenSSL/rsa_cert.pem --x509keyfile=../../CryptoCharacterizationTLS/OpenSSL/rsa_srv_pvt.pem --x509certfile=../../CryptoCharacterizationTLS/OpenSSL/rsa_srv_cert.pem --priority="NORMAL:-SIGN-ALL:+SIGN-RSA-PSS-SHA256:-VERS-ALL:+VERS-TLS1.3:-CIPHER-ALL:+AES-128-GCM:-GROUP-ALL:+GROUP-FFDHE2048"


        ECDH, ECDSA:


Results

    1. Key Exchange: 

        FFDH


        ECDH

        <!-- nettle_curve25519_mul, curve25519-mul.c, 59
        _nettle_ecc_mul_m, ecc-mul-m.c, 52 -->

    2. Signing: 
    
        RSA-PSS
        rsa_compute_root_tr() from devel/nettle/rsa-sign-tr.c

        DSA


    3. Encryption: 


    
    4. Hashing: 