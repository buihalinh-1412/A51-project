from src.attack_two_time_pad import *
p1 = open("examples/p1.txt","rb").read()
p2 = open("examples/p2.txt","rb").read()
r = simulate_scenario(p1, p2, "1223456789ABCDEF", 7, 7)
assert recover_with_known_plaintext(r["c1"], p1, r["c2"]) == p2
print("p2[:5] =", p2[:5].decode())
for row in crib_drag(r["c1"], r["c2"], p1[:5], top=3): print(row)
top = crib_drag(r["c1"], r["c2"], p1[:5], top=1)[0]
assert top["offset"] == 0 and top["text"] == p2[:5].decode()
print("--- crib dai (12 ky tu) ---")
crib = p1[4:16]
for row in crib_drag(r["c1"], r["c2"], crib, top=3): print(row)
best = crib_drag(r["c1"], r["c2"], crib, top=1)[0]
assert best["offset"] == 4 and best["text"] == p2[4:16].decode()
print("--- doi khung (frame 7 vs 8): ra rac ---")
d = simulate_scenario(p1, p2, "1223456789ABCDEF", 7, 8)
print(d["reused"], d["c1_xor_c2"] == d["p1_xor_p2"])
for row in crib_drag(d["c1"], d["c2"], crib, top=3): print(row)
print("D2 OK")
