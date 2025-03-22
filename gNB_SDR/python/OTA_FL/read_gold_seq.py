#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Suyash Pradhan.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class read_gold_seq(gr.basic_block):
    """
    docstring for block read_gold_seq
    """
    numTxAntennas = 1
    binary_byte_read = 8
    counter = 0

    def __init__(self, file_path):
        gr.basic_block.__init__(self,
            name="read_gold_seq",
            in_sig=None,
            out_sig=[np.complex64])

        self.file_path = file_path

        #dir_path = os.path.dirname(os.path.realpath(__file__))
        #print ("Data Path at matlab_payload module: {}".format(dir_path))

        self.payload = []


        # Real part of the payload read from 'payload_real.txt' file
        with open( self.file_path + '_real.txt', 'r') as f:
            pay_real = [line.strip() for line in f]

        length = (len(pay_real))

        # Imaginary part of the payload read from 'payload_imag.txt' file
        with open(self.file_path + '_imag.txt', 'r') as f1:
            pay_imag = [line.strip() for line in f1]

        # Reconstructing the payload in complex format
        for ii in range(length):
            data_p_c = complex(float(pay_real[ii]), float(pay_imag[ii]))
            data = np.complex64(data_p_c)
            self.payload.append(data)

        print("Training Signal is successfully retrieved from the target file.")

    def general_work(self, input_items, output_items):
        out = output_items[0]
        req_size = len(out)

        end = self.counter + req_size
        if end > len(self.payload):
            residue_size = len(self.payload) - self.counter
            remaining_req = req_size - residue_size

            out[:] = np.append(
                self.payload[self.counter: len(self.payload)],
                self.payload[0: remaining_req]
            )
            self.counter = remaining_req
            return len(output_items[0])

        else:
            out[:] = self.payload[self.counter:end]
            self.counter = end
            return len(output_items[0])
