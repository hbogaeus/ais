SCALARS
    b       table sizes /8/
    a       weighting of obj foo /3/
    genavg  gender diff /2/
;

VARIABLES
    x(k,j)  indicator for attendant j at table k
    si(k,l)   student interest at table k
    ei(k,l)   exhibitor interest at table k
    genval(k)  gender value at table k
    f1      interest obj value
    f2      gender obj value
    f
;

Integer Variable x;

x.up(k,j) = 1;
x.fx(k,js_s)$(StatS(k,js_s) eq 1) = 1;
x.fx(k,je_s)$(StatE(k,je_s) eq 1) = 1;

EQUATIONS
    seatedeqn(j)    make sure each person is seated on only one table
    tableeqn(k)     make sure each table isnt overfilled
    studinterest(k,l) student interest value at table k
    exinterest(k,l)   exhibitor interest at table k
    interestobj1    absvalue rewritten linearly
    interestobj2    absvalue rewritten linearly
    tablegender(k)  gender value at table
    genderobj1      absvalue of genderweighting linear
    genderobj2      absvalue of genderweighting linear
    objfoo          final obj foo

;

seatedeqn(j)    .. sum(k, x(k,j)) =e= 1;
tableeqn(k)     .. sum(j, x(k,j)) =l= b;
studinterest(k,l) .. sum(js, Cs(l, js)*x(k,js) ) =e= si(k, l);
exinterest(k,l)   .. sum(je, Ce(l, je)*x(k,je) ) =e= ei(k, l);

interestobj1    .. f1 =g= sum(k, sum(l, si(k,l) - ei(k,l) ) );
interestobj2    .. f1 =g= sum(k, sum(l, -(si(k,l) - ei(k,l)) ) );

tablegender(k)  .. genval(k) =e= sum(j, G(j)*x(k,j));
genderobj1      .. f2 =g= sum(k, genavg*sum(j, x(k,j)) - genval(k));
genderobj2      .. f2 =g= sum(k, -(genavg*sum(j, x(k,j)) - genval(k)) );

objfoo          .. f =e= a*f1 + (5-a)*f2

model banquetplacement /ALL/;
solve banquetplacement using mip minimizing f;

DISPLAY x.L, f1.L, f2.L;
