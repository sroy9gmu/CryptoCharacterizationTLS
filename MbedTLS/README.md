MbedTLS Simple Echo Client/Server using TLS 1.3
==============================================

This project implements a simple echo client/server using TLS v1.3.

Links

    1. v1.3 specification: https://datatracker.ietf.org/doc/html/rfc8446 

    2. Example: https://github.com/Mbed-TLS/mbedtls/tree/39e2e4c3cb6b0c07f6d1a12d974393c8a0830d89/programs#ssltls-feature-demonstrators

    3. https://mbed-tls.readthedocs.io/en/latest/kb/how-to/generate-a-self-signed-certificate/

    4. https://mbed-tls.readthedocs.io/en/latest/kb/cryptography/providing-diffie-hellman-or-dhm-parameters/

Issues

    1. https://github.com/Mbed-TLS/mbedtls/issues/10174

Installation

    1. Download latest release.

        wget https://github.com/Mbed-TLS/mbedtls/archive/refs/tags/mbedtls-3.6.3.tar.gz --no-check-certificate
        tar xvf mbedtls-3.6.3.tar.gz

    3. Add math library to LDFLAGS in scripts/common.make

        cd <mbedtls>
        LDFLAGS ?= -lm

    4. In file include/mbedtls/mbedtls_config.h, 
    
        Disable below features 
            MBEDTLS_HAVE_ASM 
            MBEDTLS_AESNI_C (on intel platforms)
            MBEDTLS_CCM_C / GCM_C
            MBEDTLS_CHACHAPOLY_C
            MBEDTLS_KEY_EXCHANGE_DHE_PSK_ENABLED
            MBEDTLS_KEY_EXCHANGE_RSA_PSK_ENABLED
            MBEDTLS_KEY_EXCHANGE_RSA_ENABLED  
            MBEDTLS_KEY_EXCHANGE_ECDHE_RSA_ENABLED
            MBEDTLS_KEY_EXCHANGE_ECDH_RSA_ENABLED

            FFDH, RSA-PSS:            
            MBEDTLS_KEY_EXCHANGE_ECDH_ECDSA_ENABLED            
            MBEDTLS_KEY_EXCHANGE_ECDHE_ECDSA_ENABLED            

            ECDH, DSA:
            MBEDTLS_KEY_EXCHANGE_DHE_RSA_ENABLED
            MBEDTLS_RSA_C
            MBEDTLS_X509_RSASSA_PSS_SUPPORT            
        
        (OLD)Enable below features 
            MBEDTLS_PSA_CRYPTO_CONFIG

            FFDH, RSA-PSS:   
            MBEDTLS_DHM_C
            MBEDTLS_RSA_C
            MBEDTLS_KEY_EXCHANGE_DHE_RSA_ENABLED

            ECDH, DSA: 
            MBEDTLS_PSA_P256M_DRIVER_ENABLED 

    5. In file include/psa/crypto_config.h,

        Set to 0 below macros
            #define PSA_WANT_ALG_CBC_NO_PADDING             0
            #define PSA_WANT_ALG_CBC_PKCS7                  0
            #define PSA_WANT_ALG_CCM / GCM                  0
            #define PSA_WANT_ALG_CCM_STAR_NO_TAG            0
            #define PSA_WANT_ALG_CFB                        0
            #define PSA_WANT_ALG_CHACHA20_POLY1305          0
            #define PSA_WANT_ALG_ECB_NO_PADDING             0
            #define PSA_WANT_ALG_OFB                        0
            #define PSA_WANT_ALG_STREAM_CIPHER              0
            #define PSA_WANT_KEY_TYPE_ARIA                  0
            #define PSA_WANT_KEY_TYPE_CAMELLIA              0
            #define PSA_WANT_KEY_TYPE_CHACHA20              0
            #define PSA_WANT_KEY_TYPE_DES                   0

    6. Compile:
        make
        sudo make install

Security Parameters

    1. 128-bit:  AES-GCM-128, DH/DSA (L = 3072, N = 256), RSA-3072, ECC (f = 256 - 383), SHA-256

Steps   

    1. Generate a private key for the CA

        RSA-PSS: 
        openssl genpkey -algorithm RSA -out rsa_pvt.pem -pkeyopt rsa_keygen_bits:3072 -text

        DSA: 


    2. Generate the X509 certificate for the CA:

        RSA-PSS: 
        openssl req -new -x509 -nodes -days 365000 -key rsa_pvt.pem -out rsa_cert.pem

        DSA:


    3. Generate the client and server's private key and certificate request:

        RSA-PSS: 
        openssl req -newkey rsa:3072 -nodes -days 365000 -keyout rsa_srv_pvt.pem -out rsa_srv_req.pem
        openssl req -newkey rsa:3072 -nodes -days 365000 -keyout rsa_cli_pvt.pem -out rsa_cli_req.pem

        DSA:


    4. Generate the X509 certificate for the server (may need regeneration):

        RSA-PSS: 
        openssl req -in rsa_srv_req.pem -out rsa_srv_cert.pem -verify -x509 -CA rsa_cert.pem -CAkey rsa_pvt.pem
        openssl req -in rsa_cli_req.pem -out rsa_cli_cert.pem -verify -x509 -CA rsa_cert.pem -CAkey rsa_pvt.pem

        DSA: 


    5. Generate DH parameters for key exchange between server and client:
        /usr/local/bin/openssl dhparam -out dh_param.pem 3072

    6. Start server and client in separate windows

        cd programs/ssl

        FFDH, RSA-PSS:  
        ./ssl_server2 ca_file=4b/rsa_cert.pem crt_file=4b/rsa_srv_cert.pem key_file=4b/rsa_srv_pvt.pem dhm_file=4b/dh_param.pem groups="ffdhe2048" force_version=tls13 tls13_kex_modes=ephemeral_all force_ciphersuite=TLS1-3-AES-128-GCM-SHA256

        ./ssl_client2 ca_file=4b/rsa_cert.pem crt_file=4b/rsa_cli_cert.pem key_file=4b/rsa_cli_pvt.pem groups="ffdhe2048" force_version=tls13 tls13_kex_modes=ephemeral_all force_ciphersuite=TLS1-3-AES-128-GCM-SHA256

        ECDH, ECDSA:


Results

    1. Key Exchange: 

        FFDH
        mbedtls_psa_ffdh_key_agreement, psa_crypto_ffdh.c, 276
        peer_key_length=256, shared_secret_size=256
        mbedtls_mpi_exp_mod, bignum.c, 1737
        mbedtls_mpi_exp_mod_optionally_safe, bignum.c, 1622

        ToDo: 
        1. implement rounds > 1
        2. show ssl state breakdown

        ECDH 

        <!-- ecp_use_curve25519, ecp_curves.c, 4625
        ecp_mul_mxz, ecp.c, 2550 -->

    2. Signing:
    
        RSA-PSS
        rsa_rsassa_pss_sign_no_mode_check, rsa.c, 2122
        mbedtls_rsa_private, rsa.c, 1415

        ToDo: implement rounds > 1.

        DSA

    3. Encryption:     

        mbedtls_gcm_update, gcm.c
        mbedtls_ccm_update, ccm.c

        ToDo: implement rounds > 1.
    
    4. Hashing: 
    
        mbedtls_sha256_update, sha256.c, 649



