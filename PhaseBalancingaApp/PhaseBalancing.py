import itertools 		# combinatorics/backtracking helpers
import os        		# clear screen
import re			# decimal comma [,] to decimal dot [.]
import random			# tie-breakers
from time import perf_counter   # precise timer for search limits

#==================
# UI TEXT [EN / RO]

LANGS = {
    "en": {
        "title": "3-Phase Load Balancer",
        "choose_lang_header": "=== Choose language / Alegeti limba ===",
        "choose_lang": "Choose language: 1=English, 2=Romana",
        "enter_n": "Enter number of consumers (≥1): ",
        "consumer_kw": "Consumer {i} [kW]: ",
        "result": "=== Result ===",
        "phase": "Phase {i}",
        "none": "(none)",
        "total": "Total",
        "delta": "Imbalance from average [kW]",
        "press_rx": "Press R to run again, L to change language, or X to exit...",
        "interrupted": "Interrupted.",
        "bad_value": "Invalid input. Please enter numbers.",
        "ideal": "Ideally each phase ≈ {avg:.2f} kW.",
        "no_imbalance": "No imbalance: all phases are balanced (0.00 kW).",
        "max_imbalance": "Maximum imbalance is on {phase}",
        "over": "over",
        "under": "under",
        "solver_Exact": "[Exact solver]",
        "solver_Complex": "[Complex solver]"
    },
    "ro": {
        "title": "Echilibrarea Fazelor",
        "choose_lang_header": "=== Alegeti limba / Choose language ===",
        "choose_lang": "Alegeti limba: 1=English, 2=Romana",
        "enter_n": "Introduceti numarul de consumatori (≥1): ",
        "consumer_kw": "Consumator {i} [kW]: ",
        "result": "=== Rezultat ===",
        "phase": "Faza {i}",
        "none": "(niciunul)",
        "total": "Total",
        "delta": "Dezechilibru fata de medie [kW]",
        "press_rx": "Apasati R pentru a rula din nou, L pentru a schimba limba, sau X pentru a iesi...",
        "interrupted": "Intrerupt.",
        "bad_value": "Valoare invalida. Introduceti numere.",
        "ideal": "Ideal, fiecare faza ≈ {avg:.2f} kW.",
        "no_imbalance": "Nu exista dezechilibru: toate fazele sunt echilibrate (0.00 kW).",
        "max_imbalance": "Dezechilibrul maxim este pe {phase}",
        "over": "peste",
        "under": "sub",
        "solver_Exact": "[Solver Exact]",
        "solver_Complex": "[Solver Complex]"
    }
}


#=============================================
# Parsing helpers - accepts both x.yz and x,yz

def normalize_decimal(s: str) -> str:
    return re.sub(r'(?<=\d),(?=\d)', '.', s)


#==========================
# Common evaluation helpers

def totals_and_diff(assign, weights):
    totals = [0.0, 0.0, 0.0]
    phases = [[], [], []]
    for i, b in enumerate(assign):
        phases[b].append(i)
        totals[b] += weights[i]
    diff = max(totals) - min(totals)
    return phases, totals, diff


#======================
# Exact solver (n ≤ 12)

def solve_Exact(weights):
    n = len(weights)
    if n == 0:
        return [[], [], []], [0.0, 0.0, 0.0], 0.0

    indexed = list(enumerate(weights))
    indexed.sort(key=lambda x: x[1], reverse=True)
    idx_order = [i for i,_ in indexed]
    w_sorted  = [w for _,w in indexed]

    best_diff = float("inf")
    best_assign = None
    totals = [0.0, 0.0, 0.0]
    assign = [-1]*n

    assign[0] = 0
    totals[0] += w_sorted[0]

    def backtrack(pos):
        nonlocal best_diff, best_assign, totals, assign
        if pos == n:
            diff = max(totals) - min(totals)
            if diff < best_diff:
                best_diff = diff
                best_assign = assign.copy()
            return
        if max(totals) - min(totals) >= best_diff:
            return
        w = w_sorted[pos]
        for b in sorted((0,1,2), key=lambda bb: totals[bb]):
            assign[pos] = b
            totals[b] += w
            backtrack(pos+1)
            totals[b] -= w
            assign[pos] = -1

    backtrack(1)

    final_assign = [0]*n
    for pos, b in enumerate(best_assign):
        final_assign[idx_order[pos]] = b
    return totals_and_diff(final_assign, weights)


#========================
# Complex solver (n > 12)

def greedy_seed(weights, near_equal_eps=0.01, rnd=random):
    items = list(enumerate(weights))
    items.sort(key=lambda x: x[1], reverse=True)
    grouped = []
    cur = [items[0]] if items else []
    for a, b in zip(items, items[1:]):
        if abs(a[1]-b[1]) <= near_equal_eps*max(1.0, a[1], b[1]):
            cur.append(b)
        else:
            rnd.shuffle(cur)
            grouped.extend(cur)
            cur = [b]
    if cur:
        rnd.shuffle(cur)
        grouped.extend(cur)

    totals = [0.0, 0.0, 0.0]
    assign = [-1]*len(weights)
    for idx, w in grouped:
        mval = min(totals)
        candidates = [i for i,t in enumerate(totals) if abs(t - mval) < 1e-12]
        b = rnd.choice(candidates)
        assign[idx] = b
        totals[b] += w
    return assign

def local_search(weights, assign, time_cap_ms=200, max_moves=500, rnd=random):
    n = len(weights)
    best_assign = assign[:]
    phases, totals, best_diff = totals_and_diff(best_assign, weights)
    start = perf_counter()
    moves = 0
    tabu = set()

    def improve_by_single_move():
        nonlocal best_assign, phases, totals, best_diff, moves
        improved = False
        order = list(range(n))
        rnd.shuffle(order)
        for i in order:
            src = best_assign[i]
            for dst in (0,1,2):
                if dst == src:
                    continue
                key = (i, src, dst)
                if key in tabu:
                    continue
                totals[src] -= weights[i]
                totals[dst] += weights[i]
                diff = max(totals) - min(totals)
                if diff + 1e-12 < best_diff:
                    best_diff = diff
                    best_assign[i] = dst
                    phases[src].remove(i)
                    phases[dst].append(i)
                    improved = True
                    moves += 1
                    tabu.add((i, dst, src))
                else:
                    totals[src] += weights[i]
                    totals[dst] -= weights[i]
        return improved

    def improve_by_pair_swap():
        nonlocal best_assign, phases, totals, best_diff, moves
        improved = False
        for a in (0,1,2):
            for b in (a+1,2):
                if b > 2 or not phases[a] or not phases[b]:
                    continue
                sample_a = phases[a][:]
                sample_b = phases[b][:]
                random.shuffle(sample_a); random.shuffle(sample_b)
                tries = 0
                for i in sample_a:
                    for j in sample_b:
                        if tries > 200:
                            break
                        tries += 1
                        key = (i,a,b,j,b,a)
                        if key in tabu:
                            continue
                        totals[a] -= weights[i]; totals[a] += weights[j]
                        totals[b] -= weights[j]; totals[b] += weights[i]
                        diff = max(totals) - min(totals)
                        if diff + 1e-12 < best_diff:
                            best_diff = diff
                            best_assign[i] = b
                            best_assign[j] = a
                            phases[a].remove(i); phases[a].append(j)
                            phases[b].remove(j); phases[b].append(i)
                            improved = True
                            moves += 1
                            tabu.add(key)
                        else:
                            totals[a] += weights[i]; totals[a] -= weights[j]
                            totals[b] += weights[j]; totals[b] -= weights[i]
                if improved:
                    return True
        return improved

    while moves < max_moves and (perf_counter()-start)*1000.0 < time_cap_ms:
        if improve_by_single_move():
            continue
        if improve_by_pair_swap():
            continue
        break

    phases, totals, best_diff = totals_and_diff(best_assign, weights)
    return best_assign, phases, totals, best_diff

def solve_Complex(weights, rnd_seed=None):
    rnd = random.Random(rnd_seed)
    n = len(weights)
    if n <= 25:
        K = 8
    elif n <= 60:
        K = 16
    else:
        K = 32

    time_ms = 200 if n <= 40 else 300
    max_moves = 400 if n <= 40 else 600

    best_overall = None
    best_diff = float("inf")

    for k in range(K):
        seed = (rnd_seed if rnd_seed is not None else random.randrange(10**9)) + k
        r = random.Random(seed)
        assign0 = greedy_seed(weights, near_equal_eps=0.01, rnd=r)
        assign1, phases, totals, diff = local_search(weights, assign0, time_cap_ms=time_ms, max_moves=max_moves, rnd=r)
        if diff < best_diff:
            best_diff = diff
            best_overall = (assign1, phases, totals, diff)
            if diff < 1e-6:
                break
    _, phases, totals, diff = best_overall
    return phases, totals, diff


#=====================================================================
# Switch between solvers based on the number of single phase consumers

def Phase_Balancing(weights):
    n = len(weights)
    THRESH = 12
    if n <= THRESH:
        return solve_Exact(weights), "Exact"
    else:
        return solve_Complex(weights), "Complex"


#===
# UI
def pick_language():
    while True:
        os.system("cls")
        print("=== Choose language / Alegeti limba ===")
        print("1 = English, 2 = Romana")
        print("(then press Enter / apoi apasati Enter)")
        choice = input("> ").strip()
        if choice == "1":
            return "en"
        if choice == "2":
            return "ro"

def run_once(lang):
    txt = LANGS[lang]
    while True:
        n_str = input(txt["enter_n"]).strip()
        try:
            n = int(n_str)
            if n < 1:
                raise ValueError
        except ValueError:
            print(txt["bad_value"])
            continue

        kW = []
        ok = True
        for i in range(n):
            val = input(txt["consumer_kw"].format(i=i+1))
            try:
                kW.append(float(normalize_decimal(val)))
            except ValueError:
                print(txt["bad_value"])
                ok = False
                break
        if ok:
            break

    (phases, totals, _diff), mode = Phase_Balancing(kW)
    avg = sum(kW)/3 if kW else 0.0

    print("\n" + txt["result"])
    print((txt["solver_Exact"] if mode=="Exact" else txt["solver_Complex"]) + "\n")

    deltas = []
    max_abs = -1.0
    for pi in range(3):
        d = totals[pi] - avg
        deltas.append(d)
        if abs(d) > max_abs:
            max_abs = abs(d)

    lines = []
    for pi in range(3):
        d = deltas[pi]
        if abs(d) < 0.005:
            label_word = "≈ balanced" if lang=="en" else "≈ echilibrat"
            d_str = f"{d:+.2f} {label_word}"
        elif d > 0:
            d_str = f"{d:+.2f} {txt['over']}"
        else:
            d_str = f"{d:+.2f} {txt['under']}"

        label = txt["phase"].format(i=pi+1)
        name_word = "Consumer" if lang=="en" else "Consumator"
        names = ", ".join(f"{name_word} {i+1}" for i in phases[pi]) if phases[pi] else txt["none"]
        lines.append(f"{label}: {names} | {txt['total']} = {totals[pi]:.2f} ({txt['delta']}: {d_str})")

    for i, line in enumerate(lines):
        print(line)
        if i < len(lines) - 1:
            print()

    print()
    print(txt["ideal"].format(avg=avg))

    tol = 0.005
    if max_abs < tol:
        print(txt["no_imbalance"])
        print()
    else:
        phase_word = "Phase" if lang=="en" else "Faza"
        labels = [f"{phase_word} {i+1}" for i,d in enumerate(deltas) if abs(abs(d)-max_abs) < tol]
        if lang=="en":
            if len(labels)==1:
                phase_list = labels[0]
            elif len(labels)==2:
                phase_list = " and ".join(labels)
            else:
                phase_list = ", ".join(labels[:-1]) + " and " + labels[-1]
            print(txt["max_imbalance"].format(phase=phase_list, val=max_abs))
        else:
            if len(labels)==1:
                phase_list = labels[0]
            elif len(labels)==2:
                phase_list = " si ".join(labels)
            else:
                phase_list = ", ".join(labels[:-1]) + " si " + labels[-1]
            print(f"Dezechilibrul maxim este pe {phase_list}")
        print()

def wait_key(lang):
    txt = LANGS[lang]
    try:
        import msvcrt
        print(txt["press_rx"], end="", flush=True)
        while True:
            ch = msvcrt.getch()
            if not ch:
                continue
            key = ch.decode(errors="ignore").lower()
            if key in ("r","x","l"):
                print(key.upper())
                return key
    except ImportError:
        choice = input("\n[R]un again / [L]anguage / [E]xit: ").strip().lower()
        if choice.startswith("l"):
            return "l"
        return "r" if choice.startswith("r") else "x"

def main_loop():
    lang = pick_language()
    while True:
        os.system("cls")
        print(f"=== {LANGS[lang]['title']} ===\n")
        try:
            run_once(lang)
        except KeyboardInterrupt:
            print("\n" + LANGS[lang]["interrupted"] + "\n")
        key = wait_key(lang)
        if key == "x":
            break
        elif key == "l":
            lang = pick_language()

if __name__ == "__main__":
    main_loop()
