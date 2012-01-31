#include <stdio.h>
#include <inttypes.h>
#include <malloc.h>
#include <stdbool.h>
#include <math.h>

uint64_t* sieve_u64(uint64_t N){
    printf("Allocating memory for candidates: %llu bytes\n", ((N+1)/2 * sizeof(uint64_t)));
    uint64_t *candidates = (uint64_t *) calloc(((N+1)/2), sizeof(uint64_t));
    *candidates = 2;
    for (uint64_t pos = 1; pos < (N+1)/2 ; pos++){
        *(candidates + pos) = (pos-1)*2 + 3;
    }
    for (uint64_t pos = 2; pos < (N+1)/2 ; pos++){
        if (*(candidates + pos) > 0){
            uint64_t candidate = *(candidates + pos);
            for (uint64_t spos = pos + candidate; spos < (N/2)+1; spos += candidate){
                *(candidates + spos) = 0;
            }
        }
    }
    uint32_t cont = 0;
    for (uint64_t pos = 0; pos < (N+1)/2; pos++) if (*(candidates + pos)) cont++;
    printf("Allocating memory for result: %u bytes\n", cont * sizeof(uint64_t));
    uint64_t *sieve = (uint64_t *) calloc(cont + 1, sizeof(uint64_t));
    cont = 0;
    for (uint64_t pos = 0; pos < (N+1)/2; pos++) {
        if(*(candidates + pos)){
            *(sieve + cont) = *(candidates + pos);
            cont++;
        }
    }
    free(candidates);
    return sieve;
}

uint32_t* sieve_u32( uint32_t N){
    printf("Allocating memory for candidates: %u bytes\n", ((N+1)/2 * sizeof(uint32_t)));
    uint32_t *candidates = (uint32_t *) calloc(((N+1)/2), sizeof(uint32_t));
    *candidates = 2;
    for (uint32_t pos = 1; pos < (N+1)/2 ; pos++){
        *(candidates + pos) = (pos-1)*2 + 3;
    }
    for (uint32_t pos = 2; pos < (N+1)/2 ; pos++){
        if (*(candidates + pos) > 0){
            uint32_t candidate = *(candidates + pos);
            for (uint32_t spos = pos + candidate; spos < (N/2)+1; spos += candidate){
                *(candidates + spos) = 0;
            }
        }
    }
    uint32_t cont = 0;
    for (uint32_t pos = 0; pos < (N+1)/2; pos++) if (*(candidates + pos)) cont++;
    printf("Allocating memory for result: %u bytes\n", cont * sizeof(uint32_t));
    uint32_t *sieve = (uint32_t *) calloc(cont + 1, sizeof(uint32_t));
    cont = 0;
    for (uint32_t pos = 0; pos < (N+1)/2; pos++) {
        if(*(candidates + pos)){
            *(sieve + cont) = *(candidates + pos);
            cont++;
        }
    }
    free(candidates);
    return sieve;
}

uint32_t* factorize(uint32_t n, uint32_t *primes){
    uint32_t MaxPrime = (uint32_t) (sqrt(n)+1);
    if (primes == NULL){
        primes = sieve_u32(MaxPrime);
    }
    uint32_t *factors = (uint32_t *) calloc(MaxPrime, sizeof(uint32_t));
    uint32_t acc = n;
    uint32_t cont = 0;
    while(*primes && (acc>1)){
        if (acc % ((uint64_t) (*primes)) == 0){
            *(factors + cont) = *primes;
            acc /= *primes;
            cont++;
        }
        else{
            primes++;
        }
    }
    factors = (uint32_t *) realloc(factors, (cont+1) * sizeof(uint32_t));
    return factors;
}

bool isprime(uint64_t n, uint64_t *primes){
    while(*primes){
        if (n % ((uint64_t) (*primes)) == 0) return false;
        primes++;
    }
    return true;
}

bool hamming(uint32_t n, uint32_t type, uint32_t *primes){
    uint32_t acc = n;
    while(*primes && (acc>1)){
        if (acc % ((uint64_t) (*primes)) == 0){
            acc /= *primes;
        }
        else{
            primes++;
        }
        if (*primes > type) return false;
    }
    return true;
}

int main(void){
    uint32_t Limit = 1e8;
    uint32_t MaxPrime = ((uint32_t) sqrt(Limit)) + 1;
    uint32_t *primes = sieve_u32(MaxPrime);
    uint32_t cont = 0;
    for(uint32_t n = 1; n <= Limit; n++) {
        if (hamming(n, 100, primes)){
            cont++;
        }
        if ((n % 1000000)==0) printf("n: %u, cont: %u\n", n, cont);
    }
    printf("Total: %u\n", cont);
    free(primes);
    return 0;
}
