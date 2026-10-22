from src.attack_two_time_pad import simulate_scenario
p1, p2 = b"attack at dawn!!", b"retreat at noon!"
r = simulate_scenario(p1, p2, "1223456789ABCDEF", 5, 5)
print(r["reused"], r["c1_xor_c2"] == r["p1_xor_p2"])
r2 = simulate_scenario(p1, p2, "1223456789ABCDEF", 5, 6)
print(r2["reused"], r2["c1_xor_c2"] == r2["p1_xor_p2"])
