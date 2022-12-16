from splitmasked import io, split


def test_find_boundaries():
    assert split.find_boundaries("aaTTaa", is_masked = lambda x: x.islower()) == (True, [0, 2, 4, 6])
    assert split.find_boundaries("TTaa", is_masked = lambda x: x.islower()) == (False, [0, 2, 4])
    assert split.find_boundaries("TTaaTTT", is_masked = lambda x: x.islower()) == (False, [0, 2, 4, 7])
    assert split.find_boundaries("TTaaTTTgg", is_masked = lambda x: x.islower()) == (False, [0, 2, 4, 7, 9])
    assert split.find_boundaries("TTaaTTTgg", is_masked = lambda x: x == "a") == (False, [0, 2, 4, 9])


def test_distribute_split():
    a = io.new_record("A", "a", "a")
    b = io.new_record("B", "b", "b")
    c = io.new_record("C", "c", "c")
    d = io.new_record("D", "d", "d")
    assert split.distribute_split([a, b, c, d], first_masked = True) == {"masked": [a, c], "unmasked": [b, d]}
    assert split.distribute_split([a, b, c, d], first_masked = False) == {"masked": [b, d], "unmasked": [a, c]}
    assert split.distribute_split([a], first_masked = False) == {"masked": [], "unmasked": [a]}
    assert split.distribute_split([a], first_masked = True) == {"masked": [a], "unmasked": []}


def test_split_from_records():
    record = io.new_record("seq1 abc", "aaTTaa", "HHJJEE")
    split_records = split.split_record(record, is_masked = lambda x: x.islower())
    expected = {
        "masked": [
            io.new_record("seq1_part1 abc", "aa", "HH"),
            io.new_record("seq1_part3 abc", "aa", "EE")
        ],
        "unmasked": [
            io.new_record("seq1_part2 abc", "TT", "JJ")
        ]
    }
    assert split_records == expected

    record = io.new_record("seq2 abc", "TTaa", None)
    split_records = split.split_record(record, is_masked = lambda x: x.islower())
    expected = {
        "masked": [io.new_record("seq2_part2 abc", "aa", None)],
        "unmasked": [io.new_record("seq2_part1 abc", "TT", None)]
    }
    assert split_records == expected
