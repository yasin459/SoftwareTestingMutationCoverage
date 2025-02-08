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
        
if __name__ == "__main__":
    unittest.main()
