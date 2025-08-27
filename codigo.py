from collections import defaultdict, deque

def readints(s: str):
    s = s.strip()
    return list(map(int, s.split())) if s else []

def parse_transitions(lines, n, k):
    trans = []
    i = 0
    while len(trans) < n:
        if i >= len(lines):
            raise ValueError("Faltan filas de transiciones.")
        row = lines[i].strip()
        i += 1
        if row == "":
            continue
        nums = readints(row)
        if len(nums) == k:
            trans.append(nums)
        elif len(nums) == k + 1:
            trans.append(nums[-k:])
        else:
            raise ValueError(
                f"Fila de transiciones con {len(nums)} números; se esperaban {k} o {k+1}: '{row}'"
            )
    return trans, i

def kozen_equivalences(n, k, trans, finals):
    parents = defaultdict(list)
    pairs = []
    for p in range(n):
        for q in range(p + 1, n):
            pairs.append((p, q))
            for ai in range(k):
                r, s = trans[p][ai], trans[q][ai]
                if r != s:
                    a, b = (r, s) if r < s else (s, r)
                    parents[(a, b)].append((p, q))

    marked = set()
    dq = deque()

    for p, q in pairs:
        if (p in finals) ^ (q in finals):
            marked.add((p, q))
            dq.append((p, q))

    while dq:
        r, s = dq.popleft()
        for p, q in parents.get((r, s), ()):
            if (p, q) not in marked:
                marked.add((p, q))
                dq.append((p, q))

    equiv = [pair for pair in pairs if pair not in marked]
    equiv.sort()
    return " ".join(f"({p},{q})" for p, q in equiv)

def main():
    with open("ejemplo.txt", "r", encoding="utf-8") as f:
        data = f.read().splitlines()

    idx = 0
    while idx < len(data) and data[idx].strip() == "":
        idx += 1
    if idx >= len(data):
        return
    c = int(data[idx].strip()); idx += 1

    out_lines = []

    for _ in range(c):
        while idx < len(data) and data[idx].strip() == "":
            idx += 1
        n = int(data[idx].strip()); idx += 1

        while idx < len(data) and data[idx].strip() == "":
            idx += 1
        alphabet = data[idx].strip().split(); idx += 1
        k = len(alphabet)
        if k == 0:
            raise ValueError("Línea de alfabeto vacía.")

        finals_line = data[idx] if idx < len(data) else ""
        idx += 1
        finals = set(readints(finals_line))

        trans, consumed = parse_transitions(data[idx:], n, k)
        idx += consumed

        out_lines.append(kozen_equivalences(n, k, trans, finals))

    print("\n".join(out_lines))

if __name__ == "__main__":
    main()