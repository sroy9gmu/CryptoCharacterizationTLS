MbedTLS Simple Echo Client/Server using TLS 1.3
==============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 specification: https://datatracker.ietf.org/doc/html/rfc8446 

    2. Example: https://github.com/Mbed-TLS/mbedtls/tree/39e2e4c3cb6b0c07f6d1a12d974393c8a0830d89/programs#ssltls-feature-demonstrators

Steps

    1. Packages required: sudo apt-get install bzip2

    2. Download repository as a zip file.
        wget https://github.com/Mbed-TLS/mbedtls/releases/download/mbedtls-3.6.2/mbedtls-3.6.2.tar.bz2 

    3. Install libraries:
        tar xvf mbedtls-3.6.2.tar.bz2
        cd mbedtls-3.6.2

    4. Compile:
        NOTE: Comment out the server certificate verifcation in client code for test purpose.
        make
        sudo make install

    4. Start server process in one window:
        cd programs/ssl
        ./ssl_server2 ca_file=ca-cert.pem crt_file=server-cert.pem key_file=server-key.pem dhm_file=dhparam.pem force_version=tls13 tls13_kex_modes=ephemeral

    5. Start client process in another window of same PC: 
        ./ssl_client2 ca_file=ca-cert.pem crt_file=client-cert.pem key_file=client-key.pem force_version=tls13 tls13_kex_modes=ephemeral





