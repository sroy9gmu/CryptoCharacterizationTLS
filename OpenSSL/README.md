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
    3. ./Configure LDLIBS=-lm
    4. make
    5. make test (Optional)
    6. sudo make install

In case of shared library errors

    1. sudo cp *.so.3 /usr/local/lib
    2. sudo ldconfig  

Steps

  1. Generate DH parameters for Handshake between server and client:

      /usr/local/bin/openssl dhparam -out dhparam.pem 2048 > dhout.txt

  2. Generate a private key for the CA:

      <!-- certtool --generate-privkey --sec-param Medium --outfile secret.key

      openssl req -new -key secret.key -out srv.csr

      openssl req -new -newkey rsa:2048 -nodes -out srv.csr -keyout CA_srv_pvt.key -sha256

      openssl x509 -signkey CA_srv_pvt.key -days 90 -req -in srv.csr -out CA_srv.cert -sha256

      openssl x509 -req -days 90 -in srv.csr -CA CA_srv.cert -CAkey CA_srv_pvt.key -out signed_CA_srv.cert -set_serial 01 -sha256 -->

      openssl genrsa 2048 > ca-key.pem 

  3. Generate the X509 certificate for the CA:

      openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.pem

  4. Generate the server's private key and certificate request:

      openssl req -newkey rsa:2048 -nodes -days 365000 -keyout server-key.pem -out server-req.pem

  5. Generate the X509 certificate for the server:

      openssl x509 -req -days 365000 -set_serial 01 -in server-req.pem -out server-cert.pem -CA cacert.pem -CAkey ca-key.pem

  6. Generate the client's private key and certificate request:

      openssl req -newkey rsa:2048 -nodes -days 365000 -keyout client-key.pem -out client-req.pem

  7. Generate the X509 certificate for the client:

      openssl x509 -req -days 365000 -set_serial 01 -in client-req.pem -out client-cert.pem -CA cacert.pem -CAkey ca-key.pem
      
  8. Verify server and client certificates:

      openssl verify -CAfile cacert.pem ca-cert.pem server-cert.pem

      openssl verify -CAfile cacert.pem ca-cert.pem client-cert.pem

  9. Start SSL server for doing Handshake

      /usr/local/bin/openssl s_server -dhparam dhparam.pem -cert server-cert.pem -key server-key.pem -verifyCAfile ca-cert.pem -tls1_3 -debug -msg > s_server.txt

  4. Start SSL client for doing Handshake

      /usr/local/bin/openssl s_client -cert client-cert.pem -key client-key.pem -verifyCAfile ca-cert.pem -tls1_3 -debug -msg localhost > s_client.txt 

  5. Run TLS 1.3 record layer encryption test

      make TESTS='test_tls13encryption' V=1 test
  
  6. Run echo between server and client using SSL/TLS and TCP

      cd OpenSSL/TLSEcho

      make

      ./tlsecho s > server_r.txt
      
      ./tlsecho c localhost > client_r.txt

Results

  1. Key Exchange: 

        X25519 [ECDH] from include/crypto/ecx.h

        x25519_scalar_mulx() [x86_64], 

        ge_scalarmult_base() [aarch64] from crypto/ec/curve25519.c

  2. Signing: 

        <!-- RSA PKCS#1 PSS from include/crypto/rsa.h -->

        rsa_ossl_private_encrypt() from crypto/rsa/rsa_ossl.c

  3. Encryption: 
  
        AES GCM 128 from openssl/include/openssl/modes.h

        {Refer https://github.com/openssl/openssl/blob/8d2e4d6d8c927f05948e048fcbf62982feaf11b4/crypto/aes/aes_cbc.c#L26}

        CRYPTO_gcm128_encrypt() from crypto/modes/gcm128.c
  
  4. Hashing: 
  
        SHA1_Update() from include/crypto/md32_common.h

        SHA512_Update() from crypto/sha/sha512.c
        
        SHA256_Update() from include/crypto/md32_common.h
