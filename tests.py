import unittest
import phaseOne
import os


class TestCircuitSimulator(unittest.TestCase):

    def run_isc_to_bench_test(self, input_file, output_file, expected_output_file):
        phaseOne.isc_to_bench(input_file, output_file)

        with open(expected_output_file, "r") as f:
            expected_bench = f.read()

        with open(output_file, "r") as f:
            actual_bench = f.read()

        self.assertEqual(actual_bench.strip(), expected_bench.strip())

        os.remove(output_file)

    def run_bench_test(self, bench_file_out, input_wire_in, expected_output_file, output_file):
        phaseOne.run_bench(bench_file_out, input_wire_in, output_file)

        with open(expected_output_file, "r") as f:
            expected_bench = f.read()

        with open(output_file, "r") as f:
            actual_bench = f.read()

        self.assertEqual(actual_bench.strip(), expected_bench.strip())

        os.remove(output_file)

    def test_check_all_number(self):
        self.assertTrue(phaseOne.check_all_number("123 456 789"))
        self.assertFalse(phaseOne.check_all_number("123 ABC 789"))
        self.assertTrue(phaseOne.check_all_number("42"))
        self.assertFalse(phaseOne.check_all_number("42.5"))

    def test_get_wires(self):
        self.assertEqual(phaseOne.get_wires("AND(A, B)", "AND"), ["A", " B"])
        self.assertEqual(phaseOne.get_wires("OR(X, Y, Z)", "OR"), ["X", " Y", " Z"])
        self.assertEqual(phaseOne.get_wires("NOT(A)", "NOT"), ["A"])

    def test_wire_counter_right(self):
        fanout_dict = {}
        phaseOne.wire_counter_right(["A", "B", "A"], fanout_dict)
        self.assertEqual(fanout_dict, {"A": 2, "B": 1})

    def test_logic_gates(self):
        self.assertEqual(phaseOne.my_and("1", "1"), "1")
        self.assertEqual(phaseOne.my_and("1", "0"), "0")
        self.assertEqual(phaseOne.my_and("U", "1"), "U")
        self.assertEqual(phaseOne.my_and("U", "U"), "U")

        self.assertEqual(phaseOne.my_or("0", "0"), "0")
        self.assertEqual(phaseOne.my_or("1", "0"), "1")
        self.assertEqual(phaseOne.my_or("U", "0"), "U")
        self.assertEqual(phaseOne.my_or("U", "U"), "U")

        self.assertEqual(phaseOne.my_xor("1", "0"), "1")
        self.assertEqual(phaseOne.my_xor("U", "1"), "U")
        self.assertEqual(phaseOne.my_xor("1", "1"), "0")
        self.assertEqual(phaseOne.my_xor("0", "0"), "0")

        self.assertEqual(phaseOne.my_not("1"), "0")
        self.assertEqual(phaseOne.my_not("0"), "1")
        self.assertEqual(phaseOne.my_not("U"), "U")

        self.assertEqual(phaseOne.my_buff("1"), "1")
        self.assertEqual(phaseOne.my_buff("0"), "0")
        self.assertEqual(phaseOne.my_buff("U"), "U")

    def test_isc_to_bench(self):
        input_file = "test_input.isc"
        output_file = "test_output.bench"

        with open(input_file, "w") as f:
            f.write("1 2\n3 4\n5 inpt 0 1\n")  # Sample Data

        phaseOne.isc_to_bench(input_file, output_file)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            content = f.readlines()
            self.assertFalse(any("INPUT(" in line for line in content))

        os.remove(input_file)
        os.remove(output_file)

    def test_run_bench(self):
        bench_file = "test.bench"
        pi_file = "test.pi"
        output_file = "test_output.txt"

        with open(bench_file, "w") as f:
            f.write("INPUT(A)\nINPUT(B)\nOUTPUT(Y)\nY = AND(A, B)\n")

        with open(pi_file, "w") as f:
            f.write("A B\n1 1\n0 1\n")

        phaseOne.run_bench(bench_file, pi_file, output_file)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            content = f.readlines()
            self.assertIn("A: 1", content[0])
            self.assertIn("B: 1", content[1])

        os.remove(bench_file)
        os.remove(pi_file)
        os.remove(output_file)

    def test_isc_to_bench_c5(self):
        input_file = "./testFiles/c5.isc"
        output_file = "c5.bench"
        expected_output_file = "./testFiles/c5.bench"
        self.run_isc_to_bench_test(input_file, output_file, expected_output_file)

    def test_isc_to_bench_c17(self):
        input_file = "./testFiles/c17.isc"
        output_file = "c17.bench"
        expected_output_file = "./testFiles/c17.bench"
        self.run_isc_to_bench_test(input_file, output_file, expected_output_file)

    # def test_isc_to_bench_c432(self):
    #     input_file = "./testFiles/c432.isc"
    #     output_file = "c432.bench"
    #     expected_output_file = "./testFiles/c432.bench"
    #     self.run_isc_to_bench_test(input_file, output_file, expected_output_file)

    # def test_isc_to_bench_c499(self):
    #     input_file = "./testFiles/c499.isc"
    #     output_file = "c499.bench"
    #     expected_output_file = "./testFiles/c499.bench"
    #     self.run_isc_to_bench_test(input_file, output_file, expected_output_file)

    # def test_isc_to_bench_c880(self):
    #     input_file = "./testFiles/c880.isc"
    #     output_file = "c880.bench"
    #     expected_output_file = "./testFiles/c880.bench"
    #     self.run_isc_to_bench_test(input_file, output_file, expected_output_file)

    def test_run_bench_c5(self):
        bench_file_out = "./testFiles/c5.bench"
        input_wire_in = "./testFiles/c5.pi"
        expected_output_file = "./testFiles/c5.log"
        output_file = "c5.log"
        self.run_bench_test(bench_file_out, input_wire_in, expected_output_file, output_file)

    def test_run_bench_c17(self):
        bench_file_out = "./testFiles/c17.bench"
        input_wire_in = "./testFiles/c17.pi"
        expected_output_file = "./testFiles/c17.log"
        output_file = "c17.log"
        self.run_bench_test(bench_file_out, input_wire_in, expected_output_file, output_file)

    def test_run_bench_zSmall(self):
        bench_file_out = "./testFiles/zSmall"
        input_wire_in = "./testFiles/zSmallData"
        expected_output_file = "./testFiles/zSmallLog"
        output_file = "zSmallLog"
        self.run_bench_test(bench_file_out, input_wire_in, expected_output_file, output_file)


if __name__ == "__main__":
    unittest.main()
