import unittest
import phaseOne
import os


class TestCircuitSimulator(unittest.TestCase):

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

    def test_isc_to_bench_c17(self):
        input_file = "test_c17.isc"
        output_file = "test_c17.bench"

        isc_content = """1     1gat inpt    1   0      >sa1
    2     2gat inpt    1   0      >sa1
    3     3gat inpt    2   0 >sa0 >sa1
    8     8fan from     3gat      >sa1
    9     9fan from     3gat      >sa1
    6     6gat inpt    1   0      >sa1
    7     7gat inpt    1   0      >sa1
   10    10gat nand    1   2      >sa1
     1     8
   11    11gat nand    2   2 >sa0 >sa1
     9     6
   14    14fan from    11gat      >sa1
   15    15fan from    11gat      >sa1
   16    16gat nand    2   2 >sa0 >sa1
     2    14
   20    20fan from    16gat      >sa1
   21    21fan from    16gat      >sa1
   19    19gat nand    1   2      >sa1
    15     7
   22    22gat nand    0   2 >sa0 >sa1
    10    20
   23    23gat nand    0   2 >sa0 >sa1
    21    19"""

        expected_bench = """#test_c17
#5 inputs
#2 outputs
#0 inverters
#6 gates ( 6 NANDs )

INPUT(1)
INPUT(2)
INPUT(3)
INPUT(6)
INPUT(7)

OUTPUT(22)
OUTPUT(23)

10 = NAND(1, 3)
11 = NAND(3, 6)
16 = NAND(2, 11)
19 = NAND(11, 7)
22 = NAND(10, 16)
23 = NAND(16, 19)"""

        with open(input_file, "w") as f:
            f.write(isc_content)

        phaseOne.isc_to_bench(input_file, output_file)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            content = f.read()
            self.assertEqual(content.strip(), expected_bench.strip())

        os.remove(input_file)
        os.remove(output_file)


if __name__ == "__main__":
    unittest.main()
