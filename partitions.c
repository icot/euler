#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <malloc.h>
#include <string.h>

uint64_t restricted_partitions(uint32_t k, uint32_t n, uint64_t *cache){
    if (k > n) return 0;
    else if (k == n) return 1;
    else{
        if (cache == NULL){
                return restricted_partitions(k+1, n, cache) + restricted_partitions(k, n-k, cache);
        }
        else{
            uint64_t cached = *(cache + (k*sizeof(uint64_t))+ n);
            if (cached > 0){
                // return cache[k,n]
                printf(" Cache Hit: (k:%d, n:%d, rp(k,n): %llu index: %d\n", k,n, cached, k*sizeof(uint64_t)+n);
                return cached;
            }
            else{
                //ps[(k,n)] = rp(k+1,n) + rp(k, n-k)
                uint64_t acc;
                acc = restricted_partitions(k+1, n, cache) + restricted_partitions(k, n-k, cache);
                *(cache + (k*sizeof(uint64_t))+ n) = acc;
                return acc;
            }
        }
    }
}

uint64_t partitions(uint32_t n, uint64_t *cache){
    uint64_t p = 2;
    for (uint64_t k = 1; k < (n/2); k++){
        p += restricted_partitions(k, n-k, cache);
    }
    return p;
}

int main(int argc, char **argv){
    if (argc != 2){
        printf("Use: partitions N\n");
        return -1;
    }
    uint32_t N = (uint32_t) atoi(argv[1]);
    uint32_t cachesize = (N+1) * (N+1) * sizeof(uint64_t);
    uint64_t *cache = (uint64_t *) malloc(cachesize);
    if (cache == NULL){
        printf("Unable to reserve memory for cache\n");
        return -1;
    }
    else{
        printf("Reserved %d bytes for cache\n", cachesize);
    }
    for(uint32_t n = 1; n <= N; n++){
        printf("Computing p(%d): %llu\n", n, partitions(n, NULL));
    }
    free(cache);
    return 0;
}
