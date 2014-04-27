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

int test_triang(int num){
    float r = sqrt(1 + 8*num);
    float s1 = (-1+r)/2;
    float s2 = (-1-r)/2;
    if (abs(s1) > 0){
        if ((abs(s1) - ceil(s1)) < TH){
            return 1;
        }
        else{
            return 0;
        }
    }
    else{
        if ((abs(s2) - ceil(s2)) < TH){
            return 1;
        }
        else{
            return 0;
        }
    }
}

int main(void){
    unsigned int ndivs = 0;
    unsigned int num = 0;
    unsigned n = 0;
    while(ndivs <= 500){
        num = n*(n+1)/2;
        unsigned int nd = ndivisors(num);
        if (nd > ndivs){
            ndivs = nd;
            printf("Num:%d, ndivs:%d\n", num, ndivs);
        } 
        n +=1;
    }
    printf("Ndivisors: %d\n", ndivisors(100));
    return 0;
}

