#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Suyash Pradhan.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
import pmt

class dynamic_padder_py(gr.basic_block):
    """
    docstring for block dynamic_padder_py
    """
    def __init__(self, real, imag):
        gr.basic_block.__init__(self,
            name="dynamic_padder_py",
            in_sig=[np.complex64],
            out_sig=[np.complex64])


        complex_value = complex(float(real) ,float(imag))
        self.padding_sample = np.complex64(complex_value)

        self.padding = False

        # Init input message port
        self.message_port_register_in(pmt.intern("trigger"))
        self.set_msg_handler(pmt.intern("trigger"), self.set_padding)

    '''def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items'''

    def general_work(self, input_items, output_items):
        if self.padding is True:
            sub_input = input_items[0][:len(output_items[0]) -self.length ]
            output = numpy.append(sub_input, self.get_padding_array(self.length))
            output_items[0][:] = output
            self.consume(0, len(output_items[0])-self.length)

            self.padding = False
        else:
            print("Int Vector Check")
            output_items[0][:] = input_items[0][:len(output_items[0])]
            self.consume(0, len(output_items[0]))

        return len(output_items[0])

    def set_padding(self, msg):
        self.length = int(pmt.symbol_to_string(msg))
        if self.length < 2000:
            self.padding = True

    def get_padding_array(self, length):
        index = 0
        payload = []

        while index < length:
            payload.append(self.padding_sample)
            index = index +1

        return payload

