import collections


# Functions used for MAKING BENCH FILE
# Takes a string which is a line of file and returns TRUE if it's only numbers (only used when giving a list of fan_ins)
def check_all_number(string):
    string = string.split()
    flag = True
    for i in string:
        if not i.isnumeric():
            flag = False
            break
    return flag


# Functions used for SIMULATION
# Takes right part of "=" and gives back the list wires of fan_ins used to feed that gate
def get_wires(string, gate):
    string = string.replace(gate, "")
    string = string.replace("(", "")
    string = string.replace(")", "")
    wires = string.split(",")
    return wires


# Takes the dictionary of number of each wire used as input for each gate which is later used to know which wires
# represent fan_out stems so the output would list the branches of fan_outs as well
def wire_counter_right(wire_list, fanout_dict):
    for item in wire_list:
        fanout_dict[item] = fanout_dict.get(item, 0) + 1


def my_and(a, b):
    if a == '0' or b == '0':
        return '0'
    elif a == '1' and b == '1':
        return '1'
    else:
        return 'U'


def my_or(a, b):
    if a == '1' or b == '1':
        return '1'
    elif a == '0' and b == '0':
        return '0'
    else:
        return 'U'


def my_xor(a, b):
    if a == 'U' or b == 'U':
        return 'U'
    elif a == '1':
        return my_not(b)
    else:
        return b


def my_not(a):
    if a == '1':
        return '0'
    elif a == '0':
        return '1'
    else:
        return 'U'


def my_buff(a):
    return a


# Takes an isc format file and outputs the bench file only needs the path of isc file and path for output
def isc_to_bench(input_file, output_file):
    # Dict of fanout_branch :  fanout_steam
    fanout_dict = {}

    # Dict of address : name
    name_dict = {}

    # First one is inputs, second one is output, last one is body
    final = [[], [], []]

    # Lines in the input file
    lines = []
    gate_counter = {'AND': 0, 'NAND': 0, 'OR': 0, 'NOR': 0, 'XOR': 0, 'XNOR': 0, 'NOT': 0, 'BUFF': 0}

    # Read the file line by line and ignore the comments
    with open(input_file) as file:
        for line in file:
            if not (line.__contains__("*")):
                lines.append(line.strip())
    for i in range(0, len(lines)):

        # A line that is all number is just a list of fan_ins to a gate
        if not check_all_number(lines[i]):

            # data: [output_wire, address, gate_type, number_of_fan_outs, number_of_fan_ins, ...sa faults...]
            data = lines[i].split()
            name_dict[data[1]] = data[0]
            try:

                # Has fan_ins
                if int(data[4]) > 0:
                    i += 1
                    fan_ins = lines[i].split()
                    tmp = data[0] + " = " + data[2].upper() + "("
                    gate_counter[data[2].upper()] = gate_counter.get(data[2].upper()) + 1
                    for j in range(0, len(fan_ins)):
                        tmp = tmp + fanout_dict.get(fan_ins[j], fan_ins[j]) + ", "

                    # At the end tmp has an extra ", " and these two chars aren't needed just needs ")" at the end
                    final[2].append(tmp[:-2] + ")")

                # No fan_ins (PI wire)
                else:
                    if data[2] == 'inpt':
                        final[0].append("INPUT(" + data[0] + ")")

                # No fan_outs (PO wire)
                if int(data[3]) == 0:
                    final[1].append("OUTPUT(" + data[0] + ")")

                # Multiple fan_outs
                elif int(data[3]) > 1:
                    for j in range(0, int(data[3])):
                        i += 1

                        # fan_out_Line_data = [output_wire, address, from, fan_in_address, ...sa faults...] and only
                        # adds to the fan_out dict cause the steam and the branch have same values and are names by
                        # same wire in bench
                        fan_out_Line_data = lines[i].split()
                        fanout_dict[fan_out_Line_data[0]] = name_dict.get(fan_out_Line_data[3])
            except:
                pass
    # Writing data to bench file
    file_out = open(output_file, "w")
    file_out.write("#" + output_file.split(".")[0] + "\n")
    file_out.write("#" + str(len(final[0])) + " inputs\n")
    file_out.write("#" + str(len(final[1])) + " outputs\n")
    counter = 0
    for gate in gate_counter.keys():
        counter += gate_counter[gate]
    file_out.write("#" + str(gate_counter['NOT']) + " inverters\n")
    file_out.write("#" + str(counter) + " gates (")
    for gate in gate_counter.keys():
        if gate_counter[gate] > 0:
            file_out.write(" " + str(gate_counter[gate]) + " " + gate + "s")
    file_out.write(" )\n\n")
    for i in range(0, 3):
        for j in final[i]:
            file_out.write(j + "\n")
        file_out.write("\n")
    file_out.close()


# Takes the path of a bench file description and the path of a PI file and the path to produce an output file containing
# all the wires and their values
def run_bench(input_bench, input_data, output_file):
    # Dict of wire : value which will have all the wires in the circuit and their values and gets written to output file
    wire_value = collections.OrderedDict()

    # Dict of wire : number_of_times_in_input_of_gates so the output could know which stems have how many branches and
    # write the value of branch to output file as well
    fanout_check = {}

    # Lines of bench file
    lines = []

    final = list()
    with open(input_data) as file:

        # input_wires: PI1 PI2 PI3 PI4 ...
        input_wires = file.readline().strip().split()

        # input_wire_values: 0/1/U 0/1/U 0/1/U 0/1/U ...
        input_wire_values = file.readline().strip().split()
    for i in range(len(input_wires)):
        wire_value[input_wires[i]] = input_wire_values[i]
    with open(input_bench) as file:
        for line in file:
            if not line.__contains__("#") and line != "\n":
                lines.append(line.strip())
    for line in lines:
        if line.__contains__("OUTPUT"):
            tmp = get_wires(line, "OUTPUT")
            for PO in tmp:
                wire_value[PO] = "U"
        if line.__contains__("="):

            # tmp: output_wire=GATE(Wire1, Wire2, ...)
            tmp = line.replace(" ", "").split("=")
            if tmp[1].__contains__("NAND"):
                wires = get_wires(tmp[1], "NAND")
                wire_counter_right(wires, fanout_check)
                tmp_val = my_and(wire_value[wires[0]], wire_value[wires[1]])
                for i in range(2, len(wires)):
                    tmp_val = my_and(tmp_val, wire_value[wires[i]])
                tmp_val = my_not(tmp_val)
                wire_value[tmp[0]] = tmp_val
            elif tmp[1].__contains__("AND"):
                wires = get_wires(tmp[1], "AND")
                wire_counter_right(wires, fanout_check)
                tmp_val = my_and(wire_value[wires[0]], wire_value[wires[1]])
                for i in range(2, len(wires)):
                    tmp_val = my_and(tmp_val, wire_value[wires[i]])
                wire_value[tmp[0]] = tmp_val
            elif tmp[1].__contains__("XNOR"):
                wires = get_wires(tmp[1], "XNOR")
                wire_counter_right(wires, fanout_check)
                tmp_val = my_xor(wire_value[wires[0]], wire_value[wires[1]])
                for i in range(2, len(wires)):
                    tmp_val = my_xor(tmp_val, wire_value[wires[i]])
                tmp_val = my_not(tmp_val)
                wire_value[tmp[0]] = tmp_val
            elif tmp[1].__contains__("XOR"):
                wires = get_wires(tmp[1], "XOR")
                wire_counter_right(wires, fanout_check)
                tmp_val = my_xor(wire_value[wires[0]], wire_value[wires[1]])
                for i in range(2, len(wires)):
                    tmp_val = my_xor(tmp_val, wire_value[wires[i]])
                wire_value[tmp[0]] = tmp_val
            elif tmp[1].__contains__("NOR"):
                wires = get_wires(tmp[1], "NOR")
                wire_counter_right(wires, fanout_check)
                tmp_val = my_or(wire_value[wires[0]], wire_value[wires[1]])
                for i in range(2, len(wires)):
                    tmp_val = my_or(tmp_val, wire_value[wires[i]])
                tmp_val = my_not(tmp_val)
                wire_value[tmp[0]] = tmp_val
            elif tmp[1].__contains__("OR"):
                wires = get_wires(tmp[1], "OR")
                wire_counter_right(wires, fanout_check)
                tmp_val = my_or(wire_value[wires[0]], wire_value[wires[1]])
                for i in range(2, len(wires)):
                    tmp_val = my_or(tmp_val, wire_value[wires[i]])
                wire_value[tmp[0]] = tmp_val
            elif tmp[1].__contains__("NOT"):
                wires = get_wires(tmp[1], "NOT")
                wire_counter_right(wires, fanout_check)
                wire_value[tmp[0]] = my_not(wire_value[wires[0]])
            elif tmp[1].__contains__("BUFF"):
                wires = get_wires(tmp[1], "BUFF")
                wire_counter_right(wires, fanout_check)
                wire_value[tmp[0]] = my_buff(wire_value[wires[0]])
    for wire in wire_value.keys():
        final.append(wire + ": " + wire_value[wire])
        if wire in fanout_check.keys() and fanout_check[wire] > 1:
            for i in range(0, fanout_check.get(wire)):
                final.append(wire + "_" + str(i) + ": " + wire_value[wire])
    file_out = open(output_file, "w")
    for i in final:
        file_out.write(i + "\n")
    file_out.close()
