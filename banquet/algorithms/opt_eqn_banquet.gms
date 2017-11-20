***********************************************************
*
*
*
*
***********************************************************
SETS
    j           attendants          /j1*j12/
    k           tables              /k1*k3/
    l           interests           /l1*l5/
    js(j)       subset of students  /j1*j5/
    je(j)       subset of exhibit   /j6*j12/
    js_s(js)    static students     /j4*j5/
    je_s(je)    static exhibitors   /j10*j12/
;

TABLE Cs(l,js) interest adjecency matrix for students
    j1  j2  j3  j4  j5
l1  0   1   0   0   0
l2  1   0   0   0   0
l3  0   0   1   0   0
l4  0   0   0   1   0
l5  0   0   0   0   0
;

TABLE Ce(l,je) interest adjecency matrix for exhibitors
    j6  j7  j8  j9  j10 j11 j12
l1  1   0   0   1   0   0   1
l2  0   0   0   0   0   0   0
l3  0   0   0   0   0   1   0
l4  1   1   0   0   0   0   0
l5  0   0   1   0   1   0   0
;

TABLE StatE(k, je_s) exhibitor attendants with a fixed placement
    j10 j11 j12
k1  1   0   0
k2  0   1   1
k3  0   0   0
;

TABLE StatS(k, js_s) student attendants with a fixed placement
    j4  j5
k1  1   0
k2  0   0
k3  0   1
;

PARAMETER G(j) gender of attendants
/
j1  1
j2  2
j3  3
j4  1
j5  3
j6  1
j7  2
j8  3
j9  1
j10 3
j11 1
j12 3
/;

SCALARS
    b       table sizes /4/
    a       weighting of obj foo /0/
    genavg  gender diff /2/
;

VARIABLES
    x(k,j)  indicator for attendant j at table k
    si(k)   student interest at table k
    ei(k)   exhibitor interest at table k
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
    studinterest(k) student interest value at table k
    exinterest(k)   exhibitor interest at table k
    interestobj1    absvalue rewritten linearly
    interestobj2    absvalue rewritten linearly
    tablegender(k)  gender value at table
    genderobj1      absvalue of genderweighting linear
    genderobj2      absvalue of genderweighting linear
    objfoo          final obj foo
;

seatedeqn(j)    .. sum(k, x(k,j)) =e= 1;
tableeqn(k)     .. sum(j, x(k,j)) =l= b;
studinterest(k) .. sum(js, sum(l, Cs(l, js)*x(k,js) ) ) =e= si(k);
exinterest(k)   .. sum(je, sum(l, Ce(l, je)*x(k,je) ) ) =e= ei(k);

interestobj1    .. f1 =g= sum(k, si(k) - ei(k) );
interestobj2    .. f1 =g= sum(k, -(si(k) - ei(k)) );

tablegender(k)  .. genval(k) =e= sum(j, G(j)*x(k,j));

genderobj1      .. f2 =g= sum(k, 2*sum(j, x(k,j)) - genval(k));
genderobj2      .. f2 =g= sum(k, -(2*sum(j, x(k,j)) - genval(k)) );

objfoo          .. f =e= a*f1 + (5-a)*f2

model banquetplacement /ALL/;
solve banquetplacement using mip minimizing f;

DISPLAY x.L, f1.L, f2.L;
