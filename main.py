import phaseOne

if __name__ == '__main__':
    isc_file_in = "c17.isc"
    bench_file_out = "c17.bench"
    input_wire_in = "c17.pi"
    output_wire_out = "c17.log"

    phaseOne.isc_to_bench(isc_file_in, bench_file_out)
    phaseOne.run_bench(bench_file_out, input_wire_in, output_wire_out)

    ##########

    isc_file_in = "c5.isc"
    bench_file_out = "c5.bench"
    input_wire_in = "c5.pi"
    output_wire_out = "c5.log"

    phaseOne.isc_to_bench(isc_file_in, bench_file_out)
    phaseOne.run_bench(bench_file_out, input_wire_in, output_wire_out)

    ##########

    bench_file_out = "zSmall"
    input_wire_in = "zSmallData"
    output_wire_out = "zSmallLog"

    phaseOne.run_bench(bench_file_out, input_wire_in, output_wire_out)

    print("Done!")
