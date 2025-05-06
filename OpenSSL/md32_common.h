/*
 * Copyright 1999-2022 The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the Apache License 2.0 (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html
 */

/*-
 * This is a generic 32 bit "collector" for message digest algorithms.
 * Whenever needed it collects input character stream into chunks of
 * 32 bit values and invokes a block function that performs actual hash
 * calculations.
 *
 * Porting guide.
 *
 * Obligatory macros:
 *
 * DATA_ORDER_IS_BIG_ENDIAN or DATA_ORDER_IS_LITTLE_ENDIAN
 *      this macro defines byte order of input stream.
 * HASH_CBLOCK
 *      size of a unit chunk HASH_BLOCK operates on.
 * HASH_LONG
 *      has to be at least 32 bit wide.
 * HASH_CTX
 *      context structure that at least contains following
 *      members:
 *              typedef struct {
 *                      ...
 *                      HASH_LONG       Nl,Nh;
 *                      either {
 *                      HASH_LONG       data[HASH_LBLOCK];
 *                      unsigned char   data[HASH_CBLOCK];
 *                      };
 *                      unsigned int    num;
 *                      ...
 *                      } HASH_CTX;
 *      data[] vector is expected to be zeroed upon first call to
 *      HASH_UPDATE.
 * HASH_UPDATE
 *      name of "Update" function, implemented here.
 * HASH_TRANSFORM
 *      name of "Transform" function, implemented here.
 * HASH_FINAL
 *      name of "Final" function, implemented here.
 * HASH_BLOCK_DATA_ORDER
 *      name of "block" function capable of treating *unaligned* input
 *      message in original (data) byte order, implemented externally.
 * HASH_MAKE_STRING
 *      macro converting context variables to an ASCII hash string.
 *
 * MD5 example:
 *
 *      #define DATA_ORDER_IS_LITTLE_ENDIAN
 *
 *      #define HASH_LONG               MD5_LONG
 *      #define HASH_CTX                MD5_CTX
 *      #define HASH_CBLOCK             MD5_CBLOCK
 *      #define HASH_UPDATE             MD5_Update
 *      #define HASH_TRANSFORM          MD5_Transform
 *      #define HASH_FINAL              MD5_Final
 *      #define HASH_BLOCK_DATA_ORDER   md5_block_data_order
 */
#include <sys/time.h>
#include <math.h>

#define M 1000000
#define ROUNDS 10

static double get_GM(uint64_t *arr){
    double prod = 1;
    double root;
    
    root = (double)1 / (double)ROUNDS;
    #ifdef DBG  
        printf("%s: root= %lf\n", __func__, root);
    #endif

    for (int i = 0; i < ROUNDS; i++){
        prod *= arr[i];        
    }
    
    return pow(prod, root);
}

#ifndef OSSL_CRYPTO_MD32_COMMON_H
# define OSSL_CRYPTO_MD32_COMMON_H
# pragma once

# include <openssl/crypto.h>

# if !defined(DATA_ORDER_IS_BIG_ENDIAN) && !defined(DATA_ORDER_IS_LITTLE_ENDIAN)
#  error "DATA_ORDER must be defined!"
# endif

# ifndef HASH_CBLOCK
#  error "HASH_CBLOCK must be defined!"
# endif
# ifndef HASH_LONG
#  error "HASH_LONG must be defined!"
# endif
# ifndef HASH_CTX
#  error "HASH_CTX must be defined!"
# endif

# ifndef HASH_UPDATE
#  error "HASH_UPDATE must be defined!"
# endif
# ifndef HASH_TRANSFORM
#  error "HASH_TRANSFORM must be defined!"
# endif
# ifndef HASH_FINAL
#  error "HASH_FINAL must be defined!"
# endif

# ifndef HASH_BLOCK_DATA_ORDER
#  error "HASH_BLOCK_DATA_ORDER must be defined!"
# endif

# define ROTATE(a,n)     (((a)<<(n))|(((a)&0xffffffff)>>(32-(n))))

#ifndef PEDANTIC
# if defined(__GNUC__) && __GNUC__>=2 && \
     !defined(OPENSSL_NO_ASM) && !defined(OPENSSL_NO_INLINE_ASM)
#  if defined(__riscv_zbb) || defined(__riscv_zbkb)
#   if __riscv_xlen == 64
#   undef ROTATE
#   define ROTATE(x, n) ({ MD32_REG_T ret;            \
                       asm ("roriw %0, %1, %2"        \
                       : "=r"(ret)                    \
                       : "r"(x), "i"(32 - (n))); ret;})
#   endif
#   if __riscv_xlen == 32
#   undef ROTATE
#   define ROTATE(x, n) ({ MD32_REG_T ret;            \
                       asm ("rori %0, %1, %2"         \
                       : "=r"(ret)                    \
                       : "r"(x), "i"(32 - (n))); ret;})
#   endif
#  endif
# endif
#endif

# if defined(DATA_ORDER_IS_BIG_ENDIAN)

#  define HOST_c2l(c,l)  (l =(((unsigned long)(*((c)++)))<<24),          \
                         l|=(((unsigned long)(*((c)++)))<<16),          \
                         l|=(((unsigned long)(*((c)++)))<< 8),          \
                         l|=(((unsigned long)(*((c)++)))    )           )
#  define HOST_l2c(l,c)  (*((c)++)=(unsigned char)(((l)>>24)&0xff),      \
                         *((c)++)=(unsigned char)(((l)>>16)&0xff),      \
                         *((c)++)=(unsigned char)(((l)>> 8)&0xff),      \
                         *((c)++)=(unsigned char)(((l)    )&0xff),      \
                         l)

# elif defined(DATA_ORDER_IS_LITTLE_ENDIAN)

#  define HOST_c2l(c,l)  (l =(((unsigned long)(*((c)++)))    ),          \
                         l|=(((unsigned long)(*((c)++)))<< 8),          \
                         l|=(((unsigned long)(*((c)++)))<<16),          \
                         l|=(((unsigned long)(*((c)++)))<<24)           )
#  define HOST_l2c(l,c)  (*((c)++)=(unsigned char)(((l)    )&0xff),      \
                         *((c)++)=(unsigned char)(((l)>> 8)&0xff),      \
                         *((c)++)=(unsigned char)(((l)>>16)&0xff),      \
                         *((c)++)=(unsigned char)(((l)>>24)&0xff),      \
                         l)

# endif

/*
 * Time for some action :-)
 */

int HASH_UPDATE(HASH_CTX *c, const void *data_, size_t len)
{
    // printf("%d, %s, %s\n", __LINE__, __func__, __FILE__);
    int prof_ret = 0;
    time_t traw;
    struct tm * timeinfo;    
    struct timeval tstart, tend;    
    uint64_t dur_start, dur_end;
    uint64_t dur[ROUNDS];

    time(&traw);
    timeinfo = localtime(&traw);
    printf("\nProfile start time and date: %s, number of rounds: %u\n", asctime(timeinfo), ROUNDS);

    for (int round = 0; round < ROUNDS; round++){

        HASH_CTX c_org;
        HASH_CTX *c_ptr = &c_org;
        memcpy(&c_org, c, sizeof(HASH_CTX));

        if (gettimeofday(&tstart, NULL) == 0) {
            dur_start = (unsigned long)(tstart.tv_sec) * M + (unsigned long)(tstart.tv_usec);
        } else {
            sprintf(stderr,"Error getting start time of function %s, round #%d\n", __func__, round);
        }

        const unsigned char *data = data_;
        unsigned char *p;
        HASH_LONG l;
        size_t n;

        if (len == 0)
            return 1;

        l = (c_ptr->Nl + (((HASH_LONG) len) << 3)) & 0xffffffffUL;
        if (l < c_ptr->Nl)              /* overflow */
            c_ptr->Nh++;
        c_ptr->Nh += (HASH_LONG) (len >> 29); /* might cause compiler warning on
                                        * 16-bit */
        c_ptr->Nl = l;

        n = c_ptr->num;
        if (n != 0) {
            p = (unsigned char *)c_ptr->data;

            if (len >= HASH_CBLOCK || len + n >= HASH_CBLOCK) {
                memcpy(p + n, data, HASH_CBLOCK - n);
                HASH_BLOCK_DATA_ORDER(c_ptr, p, 1);
                n = HASH_CBLOCK - n;
                data += n;
                len -= n;
                c_ptr->num = 0;
                /*
                * We use memset rather than OPENSSL_cleanse() here deliberately.
                * Using OPENSSL_cleanse() here could be a performance issue. It
                * will get properly cleansed on finalisation so this isn't a
                * security problem.
                */
                memset(p, 0, HASH_CBLOCK); /* keep it zeroed */
            } else {
                memcpy(p + n, data, len);
                c_ptr->num += (unsigned int)len;

                if (gettimeofday(&tend, NULL) == 0) {
                    dur_end = (unsigned long)(tend.tv_sec) * M + (unsigned long)(tend.tv_usec);
                } else {
                    sprintf(stderr,"Error getting end time of function %s, round #%d\n", __func__, round);
                } 
                // return 1;
                prof_ret = 1;
                dur[round] = dur_end - dur_start;   
                printf("Duration for round #%d = %u microseconds\n", round, dur[round]); // DBG only
                continue;
            }
        }

        n = len / HASH_CBLOCK;
        if (n > 0) {
            HASH_BLOCK_DATA_ORDER(c, data, n);
            n *= HASH_CBLOCK;
            data += n;
            len -= n;
        }

        if (len != 0) {
            p = (unsigned char *)c->data;
            c->num = (unsigned int)len;
            memcpy(p, data, len);
        }

        if (gettimeofday(&tend, NULL) == 0) {
            dur_end = (unsigned long)(tend.tv_sec) * M + (unsigned long)(tend.tv_usec);
        } else {
            sprintf(stderr,"Error getting end time of function %s, round #%d\n", __func__, round);
        }
        // return 1;
        prof_ret = 1;
        dur[round] = dur_end - dur_start;   
        printf("Duration for round #%d = %u microseconds\n", round, dur[round]); // DBG only
        continue;
    }

    printf("Mean execution time of function %s = %lf microseconds.\n", __func__, get_GM(dur));
    time(&traw);
    timeinfo = localtime(&traw);
    printf("Profile start end time and date: %s\n", asctime(timeinfo));   

    return prof_ret;
}

void HASH_TRANSFORM(HASH_CTX *c, const unsigned char *data)
{
    HASH_BLOCK_DATA_ORDER(c, data, 1);
}

int HASH_FINAL(unsigned char *md, HASH_CTX *c)
{
    unsigned char *p = (unsigned char *)c->data;
    size_t n = c->num;

    p[n] = 0x80;                /* there is always room for one */
    n++;

    if (n > (HASH_CBLOCK - 8)) {
        memset(p + n, 0, HASH_CBLOCK - n);
        n = 0;
        HASH_BLOCK_DATA_ORDER(c, p, 1);
    }
    memset(p + n, 0, HASH_CBLOCK - 8 - n);

    p += HASH_CBLOCK - 8;
# if   defined(DATA_ORDER_IS_BIG_ENDIAN)
    (void)HOST_l2c(c->Nh, p);
    (void)HOST_l2c(c->Nl, p);
# elif defined(DATA_ORDER_IS_LITTLE_ENDIAN)
    (void)HOST_l2c(c->Nl, p);
    (void)HOST_l2c(c->Nh, p);
# endif
    p -= HASH_CBLOCK;
    HASH_BLOCK_DATA_ORDER(c, p, 1);
    c->num = 0;
    OPENSSL_cleanse(p, HASH_CBLOCK);

# ifndef HASH_MAKE_STRING
#  error "HASH_MAKE_STRING must be defined!"
# else
    HASH_MAKE_STRING(c, md);
# endif

    return 1;
}

# ifndef MD32_REG_T
#  if defined(__alpha) || defined(__sparcv9) || defined(__mips)
#   define MD32_REG_T long
/*
 * This comment was originally written for MD5, which is why it
 * discusses A-D. But it basically applies to all 32-bit digests,
 * which is why it was moved to common header file.
 *
 * In case you wonder why A-D are declared as long and not
 * as MD5_LONG. Doing so results in slight performance
 * boost on LP64 architectures. The catch is we don't
 * really care if 32 MSBs of a 64-bit register get polluted
 * with eventual overflows as we *save* only 32 LSBs in
 * *either* case. Now declaring 'em long excuses the compiler
 * from keeping 32 MSBs zeroed resulting in 13% performance
 * improvement under SPARC Solaris7/64 and 5% under AlphaLinux.
 * Well, to be honest it should say that this *prevents*
 * performance degradation.
 */
#  else
/*
 * Above is not absolute and there are LP64 compilers that
 * generate better code if MD32_REG_T is defined int. The above
 * pre-processor condition reflects the circumstances under which
 * the conclusion was made and is subject to further extension.
 */
#   define MD32_REG_T int
#  endif
# endif

#endif
