#include <stdio.h>
#include <math.h>

#define TH 0.000001

unsigned int nfactors(int num){
    unsigned int total = 0;
    unsigned int buf = num;
    unsigned int div = 2;
    unsigned int oldiv = 1;
    if (num>3){
        while ((div < (num/2)+1) && (buf>1)){
            //printf("buf:%d, div:%d\n", buf, div);
            if ((buf % div) == 0) {
                    buf = buf / div;
                    if (div != oldiv){
                        total += 1;
                    }
                    oldiv = div;
                }
            else{
                div ++;
            }
        }
        return total;
    }
    else{
        return num;
    }
}   


int main(void){
    unsigned n = 1;
    unsigned s = 1;
    while(s <= 4){
        unsigned int nd;
        nd = nfactors(n);
        if (nd >= 4){
            s++;
            printf("N:%d, f:%d, s:%d\n", n, nd, s);
        }
        else{
            s = 1;
        }
        n++;
    }
    printf("N: %d\n", n-3);
    return 0;
}

