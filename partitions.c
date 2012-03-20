#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <malloc.h>
#include <string.h>

#define align sizeof(uint64_t)

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
            uint64_t cached = cache->data[((k * cache->rows) + n) * align];
            if (cached > 0){
                //printf(" Cache Hit: (k:%llu, n:%llu, rp(k,n): %llu index: %llu\n", k,n, cached,
                //        ((k * cache->rows) + n ) * align);
                return cached;
            }
            else{
                uint64_t acc;
                acc = restricted_partitions(k+1, n, cache) + restricted_partitions(k, n-k, cache);
                cache->data[((k * cache->rows) + n) * align] = acc;
                //printf(" Cache Fail: (k:%llu, n:%llu, rp(k,n): %llu index: %llu\n", k,n, cached, 
                //        ((k * cache->rows) + n ) * align);
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
    if (buffer.data == NULL){
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

    // Print cache contents:
    /*
    for(uint64_t i = 0; i <= N; i++)
        for(uint64_t j=0; j<=N; j++)
        {
        printf("Buffer pointer: %p, position: %p, offset: %llu val: %llu\n",  
                buffer.data, 
                buffer.data + (j*buffer.cols+i)*align,
                (j*buffer.cols+i)*align,
                *(buffer.data + (j*buffer.cols+i)*align));
        }
    */
    for(uint64_t n = 1; n <= N; n++){
        uint64_t pn = partitions(n, &buffer);
        printf("Computing p(%llu): %llu\n", n, pn);
    }
    free(memory);
    return 0;
}
