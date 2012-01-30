#include <stdio.h>
#include <malloc.h>

long* sieve(long N){
    long *result = (long *) malloc(((N/2)+1) * sizeof(long));
    result[0] = 2;
    for (long pos = 1; pos < (N/2) +1 ; pos++){
        result[pos] = (pos-1)*2 + 3;
    }
    for (long pos = 2; pos < (N/2) +1 ; pos++){
        if (result[pos] > 0){
            for (long spos = pos+result[pos]; spos < (N/2)+1; spos++){
                result[spos] = 0;
            }
        }
    }
    return result;

}


