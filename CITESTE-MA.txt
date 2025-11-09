
CITESTE-MA - Echilibrarea Fazelor
============================================================
0) Motivatia realizarii aplicatiei
----------------------------------
Am creat aceasta aplicatie ca sa imi usurez calculul echilibrarii fazelor la munca. Inainte faceam totul manual, verificand si recalculand de mai multe ori, ceea ce lua timp si mai aparea cate o greseala.
Acum programul gaseste rapid cea mai buna distributie pe cele trei faze, economisind timp si efort.


1) Prezentare generala
----------------------
Acest program distribuie o lista de consumatori monofazati (P+N)(fiecare cu o putere in kW)
pe cele trei faze ale unui sistem trifazat (3P+N), astfel incat sarcina totala pe fiecare faza sa fie cat mai echilibrata.

Alege automat cel mai bun algoritm:
- Solver exact (pentru liste mici, pana la 12 consumatori): calcul brut, toate combinatiile: x^y, unde x = 3 (3 faze), iar y = numarul de consumatori monofazati.
- Solver complex (pentru liste mari, rapid si aproape optim):cand y era mai mare decat 12, timpul de calcul necesar solverului exact creste mult. Pentru a reduce timpul de calcul s-a implementat o solutie alternativa.

2) Utilizare
-------------
1. Ruleaza programul sau fisierul .exe compilat.
2. Alege limba (1 = Engleza, 2 = Romana) si apasa Enter.
3. Introdu numarul de consumatori (minim 1).
4. Introdu pentru fiecare consumator puterea in kW (zecimalele pot folosi "." sau ",").
5. Vezi rezultatele:
   - Fiecare faza si consumatorii sai.
   - Totalul si abaterea fata de medie.
   - Rezumatul dezechilibrului maxim.
6. Apasa:
   - R pentru a rula din nou
   - L pentru a schimba limba
   - X pentru a iesi

3) Observatii
--------------
- Solverul exact garanteaza echilibrarea perfecta, dar este mai lent pentru liste mari.
- Solverul complex este mult mai rapid pentru liste mari si ofera rezultate foarte bune.
- Programul alege automat metoda de rezolvare. Daca numarul de consumatori monofazati este mai mare de 12, se utilizeaza metoda complexa.
- Valoarea medie si dezechilibrul sunt afisate cu doua zecimale;
  daca abaterea este sub 0.01 kW, fazele sunt considerate echilibrate.

4) Autor si versiune
---------------------
Creat de: Adrian Tudorica
Versiune: A.01
