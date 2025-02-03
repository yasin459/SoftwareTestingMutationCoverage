import unittest
from phaseOne import (
    check_all_number,
    get_wires,
    wire_counter_right,
    my_and,
    my_or,
    my_xor,
    my_not,
    my_buff,
    isc_to_bench,
    run_bench,
)
import os


class TestCircuitSimulator(unittest.TestCase):

    def test_check_all_number(self):
        self.assertTrue(check_all_number("123 456 789"))
        self.assertFalse(check_all_number("123 abc 789"))

    def test_get_wires(self):
        result = get_wires("AND(A, B)", "AND")
        self.assertEqual(result, ["A", " B"])

    def test_wire_counter_right(self):
        fanout_dict = {}
        wire_counter_right(["A", "B", "A"], fanout_dict)
        self.assertEqual(fanout_dict, {"A": 2, "B": 1})

    def test_logic_gates(self):
        self.assertEqual(my_and("1", "1"), "1")
        self.assertEqual(my_and("0", "1"), "0")
        self.assertEqual(my_or("0", "0"), "0")
        self.assertEqual(my_or("0", "1"), "1")
        self.assertEqual(my_xor("1", "0"), "1")
        self.assertEqual(my_xor("U", "1"), "U")
        self.assertEqual(my_not("1"), "0")
        self.assertEqual(my_not("0"), "1")
        self.assertEqual(my_buff("U"), "U")

    def test_isc_to_bench(self):
        input_isc = "test_input.isc"
        output_bench = "test_output.bench"

        with open(input_isc, "w") as f:
            f.write("1 2\n3 4 AND 0 2\n1 2\n5 6 OR 0 2\n3 4\n")

        isc_to_bench(input_isc, output_bench)

        self.assertTrue(os.path.exists(output_bench))

        with open(output_bench, "r") as f:
            content = f.read()
        self.assertIn("AND", content)
        self.assertIn("OR", content)

        os.remove(input_isc)
        os.remove(output_bench)

    def test_run_bench(self):
        input_bench = "test.bench"
        input_data = "test_data.pi"
        output_result = "test_result.txt"

        with open(input_bench, "w") as f:
            f.write("INPUT(A)\nINPUT(B)\nX = AND(A, B)\nOUTPUT(X)\n")

        with open(input_data, "w") as f:
            f.write("A B\n1 0\n")

        run_bench(input_bench, input_data, output_result)

        self.assertTrue(os.path.exists(output_result))

        with open(output_result, "r") as f:
            content = f.read()
        self.assertIn("X: U", content)

        os.remove(input_bench)
        os.remove(input_data)
        os.remove(output_result)


if __name__ == "__main__":
    unittest.main()
