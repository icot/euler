#include <stdio.h>
#include <stdlib.h>
#include <math.h>

v v v v v v v
#define limit 100000
*************
#define limit 50000 
^ ^ ^ ^ ^ ^ ^
#define dlimit 1000 
v v v v v v v
#define TH 0.000001 
*************
#define TH 1e-9 
^ ^ ^ ^ ^ ^ ^

int test_int(long double num){
    if (fabs(num - round(num)) < TH){
        return 1;
    }
    else{
        return 0;
    }
}

int main(void){
v v v v v v v
    long double maxx = 0;
    long double maxx2;
    unsigned long int maxy = 0;
    unsigned int maxd = 0;
    long double x2;
    long double x;
    for (unsigned int d = 2; d <= dlimit; d++){
        for (unsigned long int y = 1; y <= limit; y++){
            x2 = (long double) (1 + d*y*y);
            x = sqrt(x2);
*************
    unsigned long maxx = 0;
    unsigned long maxy = 0;
    unsigned long maxd = 0;
    for (unsigned long d = 2; d<= dlimit; d++){
        for (unsigned long y = 1; y <= limit; y++){
            double x = sqrt(1+d*y*y);
^ ^ ^ ^ ^ ^ ^
            if (test_int(x)){
                if (x > maxx){
v v v v v v v
                maxx = x;
                maxx2 = x2;
*************
                printf("X: %lf, Y: %ld, D: %ld\n", x, y ,d);
                maxx = (int) x;
^ ^ ^ ^ ^ ^ ^
                maxy = y;
                maxd = d;
                }
            }
        }
        printf("X: %Lf, X2: %Lf, Y: %ld, D: %d\n", maxx, maxx2, maxy ,d);
    }
v v v v v v v
    printf("\nD: %d, x: %LF, y: %ld\n", maxd, maxx ,maxy);
*************
    printf("\nX: %ld, Y: %ld, D: %ld\n", maxx, maxy ,maxd);
^ ^ ^ ^ ^ ^ ^
    return 0;
}
