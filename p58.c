#include <stdio.h>
#include <math.h>

#define TH 0.000001

unsigned int isprime(unsigned int num){
    unsigned int limit = (int) sqrt(num) +1 ;
    for (unsigned int div=2; div <=  limit; div++){
        //printf("num: %d, div: %d, rem: %d\n", num, div, num % div);
        if ((num % div)==0) {
            return 0;
            }
    }
    return 1;
}
  
int main(void){
    unsigned int n = 3;
    unsigned int np = 0;
    unsigned int N = 0;
    unsigned int cond = 1;
    while(cond){
        unsigned int d1 = n*n;
        unsigned int d2 = d1 - n + 1;
        unsigned int d3 = d1 -2 * n + 2 ;
        unsigned int d4 = d1 -3 * n + 3;
        if (isprime(d2)) np++;
        if (isprime(d3)) np++;
        if (isprime(d4)) np++;
        N += 4;
        double perc = ((double) np)/((double) N);
        printf("Order: %d, N: %d, Np: %d, ratio: %.12lf\n", n, N, np, perc);
        if (np * 10 < N) cond--;
        n += 2;
    }
    return 0;
}

