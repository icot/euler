#include <stdio.h>
#include <math.h>

unsigned int nfactors(unsigned int num){
    unsigned int buf = num;
    unsigned int div = 2;
    unsigned int oldiv = 1;
    unsigned int nf = 0;
    if (num>3){
        while ((div < (num/2)+1) && (buf>1)){
            //printf("buf:%d, div:%d\n", buf, div);
            if ((buf % div) == 0) {
                    nf++;
                    buf /= div;
                    oldiv = div;
                }
            else{
                div++;
            }
            if (nf > 2){
                return nf;
            }
        }
        return nf;
    }
    else{
        return 1;
    }
}   

int main(void){
    unsigned int cont = 0;
    for (unsigned int n=1; n <= 1e3; n++){
        unsigned int nd;
        nd = nfactors(n);
        if (nd == 2){
            cont++;
        }
        if ((n % 10000)==0){
            printf("n:%d, cont:%d\n", n, cont);
        }
        printf("n:%d, cont:%d\n", n, cont);
    }
    return 0;
}

