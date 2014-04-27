#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define TH 1e-9 

int test_int(double num){
    if (fabs(num - round(num)) < TH){
        return 1;
    }
    else{
        return 0;
    }
}

double gentriangle(long double b, long double h){
    return sqrt(b*b/4.0 + h*h);
}

double area(long b, long h){
    return sqrt((long double)b*h/2.0);
}

int main(void){
    unsigned long sum = 0;
    unsigned long b = 2;
    unsigned int cont = 0;
    while (cont <= 11){
        unsigned long h1 = b - 1;
        unsigned long h2 = b + 1;
        double s1 = area(b, h1);
        double s2 = area(b, h2);
        if (test_int(s1)){
            double L1 = gentriangle(b, h1);
            if (test_int(L1)){
                sum += L1;
                printf("cont: %d, b:%ld h:%ld L:%e S:%e \n", cont, b, h1, L1, s1);
                cont++;
            }
        }
        if (test_int(s2)){
            double L2 = gentriangle(b, h2);
            if (test_int(L2)){
                sum += L2;
                printf("cont: %d, b:%ld h:%ld L:%e S:%e \n", cont, b, h2, L2, s2);
                cont++;
            }
        }

        b++;
    }
    printf("Suma: %ld\n", sum);
    return 0;
}
