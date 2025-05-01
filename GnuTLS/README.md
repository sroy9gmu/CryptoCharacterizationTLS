GnuTLS Simple Echo Client/Server using TLS 1.3
==============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 specification: https://datatracker.ietf.org/doc/html/rfc8446 

    2. Wiki: https://gitlab.com/gnutls/gnutls

    3. gnutls-serv and gnutls-cli commands: https://gnutls.org/manual/html_node/Other-included-programs.html.

    4. Priority strings: https://gnutls.org/manual/html_node/Priority-Strings.html#Priority-Strings

    5. Stable release: 
        https://www.gnupg.org/ftp/gcrypt/gnutls/v3.7    3.7.11
        https://ftp.gnu.org/gnu/nettle/                 3.9.1

    6. Nettle manual: https://www.lysator.liu.se/~nisse/nettle/nettle.html


Issues

    1. gnutls with allowlisting doesn't allow enabling sigalgs with priority strings (OPEN)
        
        https://gitlab.com/gnutls/gnutls/-/issues/1681 


Installation

    1.  Nettle
        git clone https://git.lysator.liu.se/nettle/nettle.git
        cd nettle
        ./.bootstrap
        ./configure LIBS=-lm
        make
        sudo make install
        sudo cp /usr/local/lib64/libhogweed* /usr/local/lib64/libnettle* /usr/lib/<TARGET ARCHITECTURE>-linux-gnu
        sudo ldconfig
    
        GnuTLS
        <!-- git clone https://gitlab.com/gnutls/gnutls.git    -->
        Download latest stable release
        cd gnutls
        <!-- ./bootstrap  -->
        ./configure
        make
        sudo make install

    <!-- 3. If facing missing 'trousers' library error, specify location as /usr/local
        ./configure --with-trousers-lib=/usr/local/

    4. Additional packages required: sudo apt-get install zlib1g-dev libzstd-dev libbrotli-dev make gnutls-bin

    6. cd TLS
        NOTE: Comment out the server certificate verifcation in client code for test purpose.

    7. Compile:
        gcc server-x509.c -o server -lgnutls
        gcc client-x509.c tcp.c -o client -lgnutls

    8. Execute:
        Start server process in one window:  ./server > server.txt
        Start client process in another window of same PC: ./client 127.0.0.1 > client.txt -->

Steps

    1. Start SSL server and client in separate windows

        cd src
        FFDH, RSA-PSS:
        ./gnutls-serv --disable-client-cert --dhparams=../../CryptoCharacterizationTLS/OpenSSL/dh_param.pem --x509cafile=../../CryptoCharacterizationTLS/OpenSSL/rsa_cert.pem --x509keyfile=../../CryptoCharacterizationTLS/OpenSSL/rsa_srv_pvt.pem --x509certfile=../../CryptoCharacterizationTLS/OpenSSL/rsa_srv_cert.pem --priority="NORMAL:+SIGN-RSA-PSS-SHA256:-VERS-ALL:+VERS-TLS1.3:-CIPHER-ALL:+AES-128-GCM:-GROUP-ALL:+GROUP-FFDHE2048"

        ./gnutls-cli  --no-ca-verification --x509cafile=../../CryptoCharacterizationTLS/OpenSSL/rsa_cert.pem --x509keyfile=../../CryptoCharacterizationTLS/OpenSSL/rsa_cli_pvt.pem --x509certfile=../../CryptoCharacterizationTLS/OpenSSL/rsa_cli_cert.pem --priority="NORMAL:+SIGN-RSA-PSS-SHA256:-VERS-ALL:+VERS-TLS1.3:-CIPHER-ALL:+AES-128-GCM:-GROUP-ALL:+GROUP-FFDHE2048" 127.0.0.1:5556

        ECDH, ECDSA:


Results

    1. Key Exchange: 

        FFDH


        ECDH

        <!-- nettle_curve25519_mul, curve25519-mul.c, 59
        _nettle_ecc_mul_m, ecc-mul-m.c, 52 -->

    2. Signing: 
    
        RSA-PSS
        nettle_rsa_pss_sha256_sign_digest_tr, rsa-pss-sha256-sign-tr.c, 52
        _nettle_rsa_sec_compute_root_tr, rsa-sign-tr.c, 301

        DSA


    3. Encryption: 


    
    4. Hashing: 

        nettle_sha256_update, sha256.c, 107