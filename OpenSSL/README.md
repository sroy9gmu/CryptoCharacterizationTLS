OpenSSL Simple Echo Client/Server using TLS 1.3
===============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 
    
        1.1 Specification: https://datatracker.ietf.org/doc/html/rfc8446 
        1.2 Usage: https://wiki.openssl.org/index.php/TLS1.3

    2. Key Exchange: https://wiki.openssl.org/index.php/EVP_Key_Agreement

    3. Signing: 
    
        3.1 Direct invocation: https://wiki.openssl.org/index.php/EVP_Signing_and_Verifying
        3.2 Specification: https://datatracker.ietf.org/doc/html/rfc8017

    4. Hashing: https://github.com/openssl/openssl/blob/c2ab75e30a211aa278f8da1f0f040f9368adb81d/doc/man3/EVP_DigestInit.pod

    5. Creating cerificates: 

        5.1 Self-signed: https://www.ibm.com/docs/en/license-metric-tool?topic=communication-configuring-secure-ca-signed-certificate
        5.2 Certificate authority: https://medium.com/@yakuphanbilgic3/create-self-signed-certificates-and-keys-with-openssl-4064f9165ea3

    6. Enable/disable build options:
        https://github.com/openssl/openssl/blob/master/INSTALL.md#enable-and-disable-features


Description

It is a console application, with command line parameters determining the mode
of operation (client or server). Start it with no parameters to see usage.
The server code was adapted from the Simple TLS Server on the OpenSSL Wiki.
The server code was modified to perform the echo function, and client code
was added to open a connection with the server and to send keyboard input
to the server.
The new client code illustrates that:
    - Connection to the TLS server starts as a standard TCP 'connect'.
    - Once connected with TCP, the client 'upgrades' to TLS using
        TLS_connect().
    - When the TLS connection completes, data is sent and received using
        TLS_write() and TLS_read().
The cert.pem and key.pem files included are self signed certificates with the
"Common Name" of 'localhost'.

Issues

    1. https://github.com/openssl/openssl/issues/19639

Installation

    1. git clone https://github.com/openssl/openssl.git

    2. cd openssl

    3. FFDH, RSA-PSS:   ./Configure LDLIBS=-lm no-ec no-ecdh no-ecdsa --libdir=lib
       ECDH, DSA:   ./Configure LDLIBS=-lm no-tls-deprecated-ec --libdir=lib

    4. make [build_sw]  []: Optional

    5. sudo make install[_sw]

    6. sudo cp lib*so /lib/x86_64-linux-gnu/

    7. sudo ldconfig

Security Parameters

    1. 128-bit:  AES-GCM-128, DH/DSA (L = 3072, N = 256), RSA-3072, ECC (f = 256 - 383), SHA-256

Steps

    1. Generate a private key for the CA

        RSA-PSS: 
        openssl genpkey -algorithm RSA-PSS -out rsa_pvt.pem -pkeyopt rsa_keygen_bits:3072 

        DSA: 
        openssl genpkey -genparam -algorithm DSA -out dsa_param.pem -pkeyopt pbits:3072 -pkeyopt qbits:256 \
            -pkeyopt digest:SHA256 -pkeyopt gindex:1 -text
        openssl gendsa -out dsa_pvt.pem dsa_param.pem 

    2. Generate the X509 certificate for the CA:

        RSA-PSS: 
        openssl req -new -x509 -nodes -days 365000 -key rsa_pvt.pem -out rsa_cert.pem

        DSA:
        openssl req -new -x509 -nodes -days 365000 -key dsa_pvt.pem -out dsa_cert.pem

    3. Generate the client and server's private key and certificate request:

        RSA-PSS: 
        openssl req -newkey rsa:3072 -nodes -days 365000 -keyout rsa_srv_pvt.pem -out rsa_srv_req.pem
        openssl req -newkey rsa:3072 -nodes -days 365000 -keyout rsa_cli_pvt.pem -out rsa_cli_req.pem

        DSA:
        openssl req -newkey dsa:dsa_param.pem -nodes -days 365000 -keyout dsa_srv_pvt.pem -out dsa_srv_req.pem
        openssl req -newkey dsa:dsa_param.pem -nodes -days 365000 -keyout dsa_cli_pvt.pem -out dsa_cli_req.pem

    4. Generate the X509 certificate for the server:

        RSA-PSS: 
        openssl req -in rsa_srv_req.pem -out rsa_srv_cert.pem -verify -x509 -CA rsa_cert.pem -CAkey rsa_pvt.pem
        openssl req -in rsa_cli_req.pem -out rsa_cli_cert.pem -verify -x509 -CA rsa_cert.pem -CAkey rsa_pvt.pem

        DSA: 
        openssl req -in dsa_srv_req.pem -out dsa_srv_cert.pem -verify -x509 -CA dsa_cert.pem -CAkey dsa_pvt.pem
        openssl req -in dsa_cli_req.pem -out dsa_cli_cert.pem -verify -x509 -CA dsa_cert.pem -CAkey dsa_pvt.pem

    5. Generate DH parameters for key exchange between server and client:

        /usr/local/bin/openssl dhparam -out dh_param.pem 3072

    6. Get list of supported ciphers

        /usr/local/bin/openssl ciphers -s -tls1_3

    9. Start SSL server and client in separate windows

        FFDH, RSA-PSS:
        /usr/local/bin/openssl s_server -dhparam dh_param.pem -cert rsa_srv_cert.pem -key rsa_srv_pvt.pem\
         -verifyCAfile rsa_cert.pem -state -trace -tls1_3 -ciphersuites TLS_AES_128_GCM_SHA256
        /usr/local/bin/openssl s_client -cert rsa_cli_cert.pem -key rsa_cli_pvt.pem -verifyCAfile\
         rsa_cert.pem -state -trace -tls1_3 -ciphersuites TLS_AES_128_GCM_SHA256 localhost

        ECDH, ECDSA:
        /usr/local/bin/openssl s_server -cert dsa_srv_cert.pem -key dsa_srv_pvt.pem -verifyCAfile\
         dsa_cert.pem -state -trace -tls1_3 -ciphersuites TLS_AES_128_GCM_SHA256 -curves "P-256"
        /usr/local/bin/openssl s_client -connect localhost -cert dsa_cli_cert.pem -key dsa_cli_pvt.pem -verifyCAfile\
         dsa_cert.pem -state -trace -tls1_3 -ciphersuites TLS_AES_128_GCM_SHA256 -curves "P-256"
         
Results

    1. Key Exchange: 

        FFDH
        NamedGroup: ffdhe2048 (256)
        key_exchange:  (len=256)
        BN_mod_exp_mont(), crypto/bn/bn_exp.c

        ECDH
        NamedGroup: secp256r1 (P-256) (23)
        key_exchange:  (len=65)

    2. Signing: 

        RSA-PSS
        Signature Algorithm: rsa_pss_rsae_sha256 (0x0804)
        Signature (len=384)
        rsa_ossl_private_encrypt(), crypto/rsa/rsa_ossl.c

        DSA
            

    3. Encryption:     
            
        CRYPTO_gcm128_encrypt() from crypto/modes/gcm128.c lines 801-824
            Refer https://github.com/openssl/openssl/blob/8d2e4d6d8c927f05948e048fcbf62982feaf11b4/crypto/aes/aes_cbc.c#L26
    
    4. Hashing: 
    
        Hash Algorithm: sha256
        crypto/sha/sha256.c:#define HASH_UPDATE             SHA256_Update        
        HASH_UPDATE() from include/crypto/md32_common.h lines 156-214
