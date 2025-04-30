MbedTLS Simple Echo Client/Server using TLS 1.3
==============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 specification: https://datatracker.ietf.org/doc/html/rfc8446 

    2. Example: https://github.com/Mbed-TLS/mbedtls/tree/39e2e4c3cb6b0c07f6d1a12d974393c8a0830d89/programs#ssltls-feature-demonstrators

Installation

    1. Download latest release.

        wget https://github.com/Mbed-TLS/mbedtls/archive/refs/tags/mbedtls-3.6.3.tar.gz --no-check-certificate

    2. Install libraries:

        tar xvf mbedtls-3.6.3.tar.gz
        cd mbedtls-3.6.3

    3. Add math library to LDFLAGS in scripts/common.make

        LDFLAGS ?= -lm

    4. In file include/mbedtls/mbedtls_config.h, 
    
        Disable below features 
            MBEDTLS_HAVE_ASM 
            MBEDTLS_AESNI_C
            MBEDTLS_CHACHAPOLY_C  

            FFDH, RSA-PSS:
            MBEDTLS_KEY_EXCHANGE_ECDH_ECDSA_ENABLED
            MBEDTLS_KEY_EXCHANGE_ECDH_RSA_ENABLED
            MBEDTLS_KEY_EXCHANGE_ECDHE_ECDSA_ENABLED
            MBEDTLS_KEY_EXCHANGE_ECDHE_RSA_ENABLED

            ECDH, DSA:   
            MBEDTLS_KEY_EXCHANGE_ECDH_RSA_ENABLED
            MBEDTLS_KEY_EXCHANGE_ECDHE_RSA_ENABLED
            MBEDTLS_KEY_EXCHANGE_DHE_RSA_ENABLED
            MBEDTLS_KEY_EXCHANGE_RSA_ENABLED
            MBEDTLS_RSA_C
            MBEDTLS_X509_RSASSA_PSS_SUPPORT
            MBEDTLS_KEY_EXCHANGE_RSA_PSK_ENABLED
            
        
        Enable below features 
             

            FFDH, RSA-PSS:   
            

            ECDH, DSA: 
            MBEDTLS_PSA_P256M_DRIVER_ENABLED 

    5. Compile:
        make
        sudo make install

Security Parameters

    1. 128-bit:  AES-GCM-128, DH/DSA (L = 3072, N = 256), RSA-3072, ECC (f = 256 - 383), SHA-256

Steps   

    1. Start server and client in separate windows

        cd CryptoCharacterizationTLS/OpenSSL

        FFDH, RSA-PSS:  
        ../../mbedtls-mbedtls-3.6.3/programs/ssl/ssl_server2 ca_file=rsa_cert_mbd.pem crt_file=rsa_srv_cert_mbd.pem key_file=rsa_srv_pvt_mbd.pem dhm_file=dh_param.pem groups="ffdhe2048" force_version=tls13 tls13_kex_modes=ephemeral_all
        ../../mbedtls-mbedtls-3.6.3/programs/ssl/ssl_client2 ca_file=rsa_cert_mbd.pem crt_file=rsa_cli_cert_mbd.pem key_file=rsa_cli_pvt_mbd.pem groups="ffdhe2048" force_version=tls13 tls13_kex_modes=ephemeral_all

        ECDH, ECDSA:
        ../../mbedtls-mbedtls-3.6.3/programs/ssl/ssl_server2 ca_file=dsa_cert.pem crt_file=dsa_srv_cert.pem key_file=dsa_srv_pvt.pem groups="secp256r1" sig_algs="ecdsa_secp256r1_sha256" force_version=tls13 tls13_kex_modes=ephemeral_all
        ../../mbedtls-mbedtls-3.6.3/programs/ssl/ssl_client2 ca_file=rsa_cert_mbd.pem crt_file=rsa_cli_cert_mbd.pem key_file=rsa_cli_pvt_mbd.pem groups="secp256r1" sig_algs="ecdsa_secp256r1_sha256" force_version=tls13 tls13_kex_modes=ephemeral_all

Results

    1. Key Exchange: 

        FFDH
        mbedtls_mpi_exp_mod_optionally_safe, bignum.c, 1622
        mbedtls_psa_ffdh_key_agreement, psa_crypto_ffdh.c, 300

        ECDH 

        <!-- ecp_use_curve25519, ecp_curves.c, 4625
        ecp_mul_mxz, ecp.c, 2550 -->

    2. Signing:
    
        RSA-PSS
        rsa_rsassa_pss_sign_no_mode_check, rsa.c, 2122
        mbedtls_rsa_private, rsa.c, 1415

        DSA

    3. Encryption:     

        mbedtls_gcm_update, gcm.c, 569
    
    4. Hashing: 
    
        mbedtls_sha256_update, sha256.c, 649



