
README - 3-Phase Load Balancer
===============================
0) The motivation behind this app

I made this app to make phase balancing at work a lot simpler. We used to do it manually, checking and recalculating everything by hand, which took time and sometimes led to small mistakes.
Now the program figures out the best balance across the three phases in seconds, saving both time and effort.

---------------------------------
1) Overview

This program distributes a list of consumers (each with a power in kW)
into three phases so that the total power in each phase is as balanced as possible.

It automatically chooses the best algorithm:
- Exact solver (for small sets, up to 12 consumers): brute calculations, all combinations: x^y, where x = 3 (3 phases), and y = the number of single phase consumers.
- Complex solver (for larger sets, fast and near-optimal): when y > 12, the time needed for the exact solver to find the solution grows by a lot. In order to cut the time needed, a new solution was implemented.

------------
2) Usage

1. Run the program or the compiled .exe file.
2. Choose the language (1 = English, 2 = Romanian) and press Enter.
3. Enter the number of consumers (must be at least 1).
4. Enter each consumer’s power in kW (decimals can use "." or ",").
5. View the results:
   - Each phase and its consumers.
   - Total load and deviation from average.
   - Maximum imbalance summary.
6. Press:
   - R to run again
   - L to change language
   - X to exit

---------
3) Notes

- Exact solver guarantees the perfect split but is slower for large inputs.
- Complex solver is much faster for larger inputs and still produces very good results.
- The program chooses automatically which solver to use. If the number of single phase consumers is greater than 12, the app will use the complex solver.
- Average load is shown with two decimals; imbalance under 0.01 kW is considered balanced.

---------
4 Author and Version

Created by: Adrian Tudorica
Version: A.01
