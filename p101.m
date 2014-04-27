pgen = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1];
xt = 1:6;
yt = [1,8,27,64,125,216];
xs = 1:11;
ys = polyval(pgen, xs);

xt = xs;
yt = ys;

bops = 0;
eps = 0.00001;
for k = 1:length(yt)
    # fit
    x = xt(1:k);
    y = yt(1:k);
    printf("Fiting to n^%d\n", k-1);
    pol = polyfit(x, y, k-1);
    # find bop's
    yts = polyval(pol, xt);
    difs = abs(yts - yt);
    pfit = find(difs >= eps);
    if pfit
        bops = bops + yts(pfit(1));
    else
        break
    endif
endfor

printf("Sum of BOPS: %f\n", sum(bops))
