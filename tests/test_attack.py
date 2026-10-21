from src.attack_two_time_pad import (
    simulate_scenario,
    recover_with_known_plaintext,
    crib_drag,
)


KEY = "1223456789ABCDEF"
FRAME = 7

P1 = b"attack at dawn!!"
P2 = b"retreat at noon!"


def test_reused_frame_exposes_plaintext_xor():
    """Cùng frame phải làm lộ quan hệ C1 XOR C2 = P1 XOR P2."""
    result = simulate_scenario(P1, P2, KEY, FRAME, FRAME)

    assert result["reused"] is True
    assert result["c1_xor_c2"] == result["p1_xor_p2"]


def test_different_frame_does_not_expose_plaintext_xor():
    """Đổi frame phải tạo dòng khóa khác và phá quan hệ XOR."""
    result = simulate_scenario(P1, P2, KEY, FRAME, FRAME + 1)

    assert result["reused"] is False
    assert result["c1_xor_c2"] != result["p1_xor_p2"]


def test_recover_with_known_plaintext_returns_p2():
    """Biết P1 khi dùng lại dòng khóa phải khôi phục đúng P2."""
    result = simulate_scenario(P1, P2, KEY, FRAME, FRAME)

    recovered = recover_with_known_plaintext(
        result["c1"],
        P1,
        result["c2"],
    )

    assert recovered == P2


def test_crib_drag_correct_crib_reveals_p2_and_scores_higher():
    """Crib đúng phải lộ đoạn tương ứng của P2 và tốt hơn crib sai."""
    result = simulate_scenario(P1, P2, KEY, FRAME, FRAME)

    correct_crib = b"attack"
    correct_results = crib_drag(
        result["c1"],
        result["c2"],
        correct_crib,
        top=10,
    )

    assert correct_results

    best_correct = correct_results[0]
    expected_text = P2[: len(correct_crib)].decode()

    assert best_correct["offset"] == 0
    assert expected_text in best_correct["text"]

    wrong_crib = b"\xff" * len(correct_crib)
    wrong_results = crib_drag(
        result["c1"],
        result["c2"],
        wrong_crib,
        top=10,
    )

    assert wrong_results
    assert best_correct["score"] > wrong_results[0]["score"]
