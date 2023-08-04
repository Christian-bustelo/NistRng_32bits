#
# Copyright (C) 2019 Luca Pasqualini
# University of Siena - Artificial Intelligence Laboratory - SAILab
#
# Inspired by the work of David Johnston (C) 2017: https://github.com/dj-on-github/sp800_22_tests
#
# NistRng is licensed under a BSD 3-Clause.
#
# You should have received a copy of the license along with this
# work. If not, see <https://opensource.org/licenses/BSD-3-Clause>.

# Import packages

import sys
import numpy

# Import src

from nistrng import *

if __name__ == "__main__":
    # Generate the sequence of integers and pack it in its 8-bit representation
    #sequence: numpy.ndarray = numpy.random.randint(-128, 128, 1000, dtype=int)
    array = []
    top_limit = 2**32-1
    factor = 255/top_limit
    print(factor)
    print("test ",  int((2**32-1)*factor))
    print("test ", int(1*factor))
    print("test ", int((2**32-1)/2*factor))
    with open('/home/eortega/coding/cesga-qrng/small_output.txt', 'r') as file:
      for line in file.readlines():
          val = int(int(line.split("\n")[0]) * factor)
          print("debug", val, int(line.split("\n")[0]))
          array.append(val)
    #sequence: numpy.ndarray = numpy.array(array, dtype=numpy.uint8)
    sequence: numpy.ndarray = numpy.array(array, dtype=numpy.uint8)
    
    binary_sequence: numpy.ndarray = pack_sequence(sequence)
    
    #uint32 workaround
    #view = sequence.view(numpy.uint8)
    #if sequence.dtype.byteorder == '>' or (sequence.dtype.byteorder == '=' and sys.byteorder == 'big'):
    #    view = view[::-1]

    #binary_sequence: numpy.ndarray = numpy.unpackbits(view, axis=0, count=32, bitorder='little')[::-1]



    # Print sequence
    print("Random sequence from QRNG:")
    print(sequence)
    print("Random sequence generated by NumPy encoded in 8-bit signed format:")
    print(binary_sequence)
    print("Original sequence taken back by unpacking (to check the correctness of packing process:")
    print(unpack_sequence(binary_sequence))
    # Check the eligibility of the test and generate an eligible battery from the default NIST-sp800-22r1a battery
    eligible_battery: dict = check_eligibility_all_battery(binary_sequence, SP800_22R1A_BATTERY)
    # Print the eligible tests
    print("Eligible test from NIST-SP800-22r1a:")
    for name in eligible_battery.keys():
        print("-" + name)
    # Test the sequence on the eligible tests
    results = run_all_battery(binary_sequence, eligible_battery, False)
    # Print results one by one
    print("Test results:")
    for result, elapsed_time in results:
        if result.passed:
            print("- PASSED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
        else:
            print("- FAILED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
