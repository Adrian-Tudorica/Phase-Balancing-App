
Phase Balancing App | Aplicatie pentru Echilbarea Fazelor
=========================================================

EN = English
RO = Romana

---------------------------------
0) The motivation behind this app

EN:
I made this app to make phase balancing at work a lot simpler. We used to do it manually, checking and recalculating everything by hand, which took time and sometimes led to small mistakes.
Now the program figures out the best balance across the three phases in seconds, saving both time and effort.

RO:
Am creat aceasta aplicatie ca sa imi usurez calculul echilibrarii fazelor la munca. Inainte faceam totul manual, verificand si recalculand de mai multe ori, ceea ce lua timp si mai aparea cate o greseala.
Acum programul gaseste rapid cea mai buna distributie pe cele trei faze, economisind timp si efort.

----------------------------------
1) Overview / Prezentare generala

EN:
The app lets the user input a number of consumers (each with a power in kW)
and automatically distributes them into 3 phases to balance the total load as evenly as possible.

It is a console-based hybrid solver that chooses between an exact algorithm (for small sets)
and a fast complex algorithm (for large sets). It supports English and Romanian, and lets you rerun,
change language, or exit using keyboard keys.

RO:
Aplicatia permite introducerea unui numar de consumatori (fiecare cu o putere in kW)
si ii distribuie automat pe 3 faze astfel incat sarcina totala sa fie cat mai echilibrata.

Este un program in consola cu un algoritm hibrid: foloseste o metoda exacta pentru seturi mici
si una complexa rapida pentru seturi mari. Accepta limbile engleza si romana si ofera optiuni pentru
reluare, schimbarea limbii sau iesire.

--------------------------------------------------------
2) Language Resources (LANGS) / Resurse de limba (LANGS)

EN:
The app stores all messages (labels, prompts, etc.) for both languages in one dictionary called LANGS.

LANGS is a dictionary with two keys ("en" and "ro"). Each key contains the texts used
throughout the app. This design allows the entire UI to switch languages dynamically and keeps
translations organized in one place.

RO:
Toate mesajele (etichete, instructiuni, etc.) pentru ambele limbi sunt stocate intr-un singur
dictionar numit LANGS.

LANGS este un dictionar cu doua chei ("en" si "ro"). Fiecare cheie contine textele
folosite in program. Astfel, se poate schimba limba dinamic si traducerile sunt usor de intretinut.

----------------------------------------
3) Number Input / Introducerea valorilor

EN:
You enter the number of consumers, then enter each consumer’s kW value one by one.

The input phase ensures valid numerical data: if the user types a wrong value, it shows
an error and asks again. Decimal commas (1,25) are converted to decimal points (1.25) automatically.

RO:
Se introduce numarul de consumatori, apoi puterea fiecarui consumator (kW), una cate una.

Faza de introducere valideaza datele numerice: daca valoarea introdusa este gresita,
aplicatia afiseaza o eroare si cere repetarea. Virgulele zecimale (1,25) sunt convertite automat
in puncte zecimale (1.25).

----------------------------------
4) Exact Solver / Algoritmul exact

EN:
For small numbers of consumers (up to 12), the app tries all combinations (all possible combinations but optimized)
to find the perfect balance.

This solver uses a branch-and-bound search with symmetry breaking. The heaviest consumer
is fixed to one phase to avoid equivalent permutations. The recursion stops early when a partial result
is already worse than the best found. It guarantees the optimal distribution for small sets.

RO:
Pentru un numar mic de consumatori (pana la 12), aplicatia incearca toate combinatiile
(posibile, dar optimizate) pentru a gasi echilibrul perfect.

Acest solver foloseste o cautare branch-and-bound cu ruperea simetriei. Cel mai mare
consumator este fixat pe o faza pentru a evita permutarile echivalente. Recursia se opreste
anticipat daca un rezultat partial este deja mai slab decat cel mai bun gasit. Garanteaza solutia optima
pentru seturi mici.

--------------------------------------
5) Complex Solver / Algoritmul complex

EN:
For larger lists, it uses a fast, near-optimal algorithm instead of checking every possibility.

It runs in three stages:
A) Greedy seed: sorts consumers by power, then assigns each to the lightest phase (randomly in case of equality).
B) Local search: moves or swaps consumers between phases to reduce imbalance.
C) Multi-start: runs the algorithm multiple times with small random variations and keeps the best result.

RO:
Pentru liste mai mari, foloseste un algoritm rapid care ofera rezultate aproape optime in loc sa verifice toate combinatiile.

Ruleaza in trei etape:
A) Distributie greedy: sorteaza consumatorii descrescator si ii adauga pe faza cu sarcina cea mai mica (aleator in caz de egalitate).
B) Cautare locala: muta sau schimba consumatori intre faze pentru a reduce dezechilibrul.
C) Repetare multipla: ruleaza algoritmul de mai multe ori cu mici variatii aleatoare si pastreaza cel mai bun rezultat.

--------------------------------------------------------------
6) Phase Balancing Function / Functia de Echilibrare a Fazelor

EN:
It decides whether to use the exact or complex solver based on the number of consumers.

The function Phase_Balancing() checks the number of consumers.
If ≤ 12 → exact solver; if > 12 → complex solver.
It returns the lists of consumers per phase, totals, and imbalance.

RO:
Decide daca se foloseste metoda exacta sau cea complexa in functie de numarul de consumatori.

Functia Phase_Balancing() verifica numarul de consumatori.
Daca este ≤ 12 → foloseste solverul exact; daca este > 12 → foloseste solverul complex.
Returneaza listele de consumatori pe faze, totalurile si dezechilibrul obtinut.

--------------------------------------------
7) Output Formatting / Afisarea rezultatului

EN:
The app prints each phase’s total kW and the deviation (positive = over, negative = under).
“≈ balanced” appears when the deviation is near zero.

RO:
Aplicatia afiseaza totalul kW pentru fiecare faza si deviatia (pozitiv = peste, negativ = sub).
Afiseaza „≈ echilibrat” daca deviatia este aproape de zero.

-----------------------------------------
8) Summary Section / Sectiunea de rezumat

EN:
After listing phases, it prints the ideal average load and shows whether any imbalance exists.

If all phases are within ±0.005 kW of the average, it prints “No imbalance.” Otherwise,
it lists all phases with the maximum absolute deviation.

RO:
Dupa afisarea fazelor, programul afiseaza valoarea medie ideala si indica daca exista un dezechilibru.

Daca toate fazele sunt la ±0.005 kW fata de medie, afiseaza „Nu exista dezechilibru.”
In caz contrar, enumera toate fazele cu cea mai mare deviatia absoluta.

---------------------------------------
9) Language Selection / Alegerea limbii

EN:
At the start (or when you press L), you choose the language (1 or 2) and confirm with Enter.

pick_language() clears the screen, displays the bilingual prompt, waits for input "1" or "2",
and returns the code “en” or “ro.” The whole interface uses that setting until changed.

RO:
La inceput (sau cand se apasa L), se alege limba (1 sau 2) si se confirma cu Enter.

pick_language() sterge ecranul, afiseaza promptul bilingv, asteapta introducerea „1” sau „2”
si returneaza codul „en” sau „ro”. Intreaga interfata foloseste aceasta setare pana este schimbata.

--------------------------------------------
10) Controls (R, L, X) / Controale (R, L, X)

EN:
After results the wait_key() function reads the key pressed.
R restarts the process, L reopens language selection, X ends the program.

RO:
Dupa rezultate functia wait_key() citeste tasta apasata.
R reporneste procesul, L redeschide selectarea limbii, X inchide programul.

----------------------------------------------------
11) Performance and Scaling / Performanta si scalare

EN:
The exact algorithm grows exponentially (3^n), so it’s only used up to 12 consumers.

The complex version runs in milliseconds even for dozens of consumers by using greedy initialization,
local optimization, and limited random restarts.

RO:
Algoritmul exact creste exponential (3^n), deci este folosit doar pana la 12 consumatori.

Versiunea complexa ruleaza in cateva milisecunde chiar si pentru zeci de consumatori,
folosind initializare greedy, optimizare locala si reporniri aleatorii limitate.

------------------------------------------------------------
12) Possible Future Updates / Imbunatatiri viitoare posibile

EN:
Potential upgrades include:
 - a parallel version for multi-core CPUs (i don't think it's necessary for now)
 - a configuration file to remember language and preferences
 - a Tkinter interface for easier data entry.
 - the possibility to export the results to a .xlsx file.

RO:
Imbunatatiri posibile includ:
 - o versiune paralela pentru procesoare multi-core (nu consider necesar la momentul actual)
 - un fisier de configurare care sa retina limba si preferintele,
 - o interfata Tkinter pentru introducerea mai usoara a datelor.
 - posibilitatea exportarii rezultatelor intr-un fisier tip .xlsx.
