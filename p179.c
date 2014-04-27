#include <stdio.h>
#include <math.h>

#define TH 0.000001

int ndivisors(int num){
    int total = 0;
    if (num>3){
        for (int i=1; i <= (num/2) + 1; i++){
            if ((num % i) == 0) {
                total += 1;
            }
        }
        return total + 1;
    }
    else{
        return num;
    }
}   


int main(void){
    unsigned int ndivs1 = 1;
    unsigned int ndivs2;
    unsigned int n, cont;
    cont = 0;
    for( n = 1; n < 10000000; n++){
        ndivs2  = ndivisors(n);
        //printf(" %d %d %d \n", n, ndivs2, ndivs1);
        if (ndivs2 == ndivs1){
            cont++;
            }
        if ((n % 10000) == 0) {
            printf("Num:%d, pairs:%d\n", n, cont);
        }
        ndivs1 = ndivs2;
    }
    printf("Num:%d, pairs:%d\n", n, cont);
    return 0;
}

