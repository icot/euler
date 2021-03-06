#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <malloc.h>
#include <string.h>

#define align sizeof(uint64_t)
#define neg_one_pow(n) (((n) % 2 == 0) ? 1 : -1)

typedef struct {
    uint64_t *data;
    uint64_t rows;
    uint64_t cols;
} cache_t;

uint64_t restricted_partitions(uint64_t k, uint64_t n, cache_t *cache){
    if (k > n) return (uint64_t ) 0;
    else if (k == n) return (uint64_t) 1;
    else{
        if (cache == NULL){
                return restricted_partitions(k+1, n, cache) + restricted_partitions(k, n-k, cache);
        }
        else{
            uint64_t cached = cache->data[((k * cache->rows) + n)];
            if (cached > 0){
                return cached;
            }
            else{
                uint64_t acc;
                acc = restricted_partitions(k+1, n, cache) + restricted_partitions(k, n-k, cache);
                cache->data[((k * cache->rows) + n)] = acc;
                return acc;
            }
        }
    }
}


uint64_t partitions(uint64_t n, cache_t *cache){
    uint64_t p = 2;
    for (uint64_t k = 1; k < (n/2); k++){
        p += restricted_partitions(k, n-k, cache);
    }
    return p;
}

/*
def partitions(n):
    if n <=1 :
        return 1
    elif n == 2:
        return 2
    else:
        j1 = [ (3*pow(k,2) -k)/2 for k in range(1, n)]
        j2 = [ (3*pow(k,2) +k)/2 for k in range(1, n)]
        js = [j for j in flatten(zip(j1,j2)) if j <= n]
        p = 0
        cpos = 0
        for pos, j in enumerate(js):
            if pos % 2 == 0:
                cpos += 1
            p += pow(-1, cpos - 1) * partitions(n-j)
        return p
*/

uint64_t partitions_macmahon(uint64_t n, cache_t *cache){
    uint64_t p = 0;
    if (n <= 1) return 1;
    else 
        if (n == 2) return 2;
        else{
            for (uint64_t k = 1; k < n; k++){
                uint64_t j1 = (3 * k * k - k)/2;
                uint64_t j2 = (3 * k * k + k)/2;
                if (j1 <=n) p+= neg_one_pow(k-1) * partitions_macmahon(n-j1, cache);
                if (j2 <=n) p+= neg_one_pow(k-1) * partitions_macmahon(n-j2, cache);
                if ((j1 > n) || (j2 > n)) break;
            }

        }
    return p;
}

int main(int argc, char **argv){
    if (argc != 2){
        printf("Use: partitions N\n");
        return -1;
    }
    uint64_t N = (uint64_t) atoi(argv[1]);
    cache_t buffer;
    buffer.rows = N+1;
    buffer.cols = N+1;
    uintptr_t mask = ~(uintptr_t)(align - 1); /* mask for memory alignement */
    void *memory = malloc((buffer.rows * buffer.cols * align) + (align -1));
    buffer.data = (uint64_t *) (((uintptr_t) memory + align - 1) & mask); /* Aligned pointer */
    memset(buffer.data, 0, buffer.rows * buffer.cols * align);
    if (memory == NULL){
        printf("Unable to reserve memory for cache\n");
        return -1;
    }
    else{
        printf("Reserved %llu bytes for cache\n", buffer.rows * buffer.cols * align);
        printf("Memory: %p, %p\n", &memory, memory);
        printf(" Align mask: %u, pre-aligned: %p, aligned: %p\n", mask, memory + align -1, 
            (void *) ( ((uintptr_t) memory + align - 1) & mask));
        printf("Buffer.data: %p, %p\n", &buffer.data, buffer.data);
    }

    for(uint64_t n = 1; n <= N; n++){
        uint64_t pn = partitions(n, &buffer);
        uint64_t pnm = partitions_macmahon(n, &buffer);
        printf("Computing p(%llu): %llu, %llu\n", n, pn, pnm);
    }
    free(memory);
    return 0;
}
