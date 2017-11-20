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
j2  1
j3  3
j4  3
j5  3
j6  1
j7  1
j8  3
j9  1
j10 3
j11 1
j12 3
/;
