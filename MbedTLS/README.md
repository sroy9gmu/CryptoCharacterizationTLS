MbedTLS Simple Echo Client/Server using TLS 1.3
==============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 specification: https://datatracker.ietf.org/doc/html/rfc8446 

    2. Example: https://github.com/Mbed-TLS/mbedtls/tree/39e2e4c3cb6b0c07f6d1a12d974393c8a0830d89/programs#ssltls-feature-demonstrators

Steps

    1. Download latest release.

        wget https://github.com/Mbed-TLS/mbedtls/archive/refs/tags/mbedtls-3.6.3.tar.gz --no-check-certificate

    2. Install libraries:

        tar xvf mbedtls-3.6.3.tar.gz
        cd mbedtls-3.6.3

    3. Add math library to LDFLAGS in scripts/common.make

        LDFLAGS ?= -lm

    4. In file include/mbedtls/mbedtls_config.h, 
    
        Disable below features 
            MBEDTLS_HAVE_ASM MBEDTLS_AESNI_C
            MBEDTLS_CHACHAPOLY_C          

    5. Compile:
        make clean
        make
        sudo make install

    6. Start server process in one window:

        cd CryptoCharacterizationTLS/MbedTLS

        ../../mbedtls-mbedtls-3.6.3/programs/ssl/ssl_server2 ca_file=ca-cert.pem crt_file=server-cert.pem key_file=server-key.pem dhm_file=dhparam.pem force_version=tls13 tls13_kex_modes=ephemeral

    7. Start client process in another window of same PC: 

        ../../mbedtls-mbedtls-3.6.3/programs/ssl/ssl_client2 ca_file=ca-cert.pem crt_file=client-cert.pem key_file=client-key.pem force_version=tls13 tls13_kex_modes=ephemeral

Results

    1. Key Exchange: 

        ecp_use_curve25519, ecp_curves.c, 4625
        ecp_mul_mxz, ecp.c, 2550

    2. Signing:
    
        mbedtls_rsa_private, rsa.c, 1415

    3. Encryption: 
    
        mbedtls_cipher_aead_encrypt, cipher.c, 1448
        mbedtls_gcm_crypt_and_tag, gcm.c, 718
        mbedtls_internal_aes_encrypt, aes.c, 887
        mbedtls_gcm_update, gcm.c, 569
        mbedtls_internal_aes_encrypt, aes.c, 887
    
    4. Hashing: 
    
        mbedtls_sha256_update, sha256.c, 649



