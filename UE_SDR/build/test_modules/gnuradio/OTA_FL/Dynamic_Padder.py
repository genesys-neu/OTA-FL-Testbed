#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Suyash Pradhan.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr

class Dynamic_Padder(gr.basic_block):
    """
    docstring for block Dynamic_Padder
    """
    def __init__(self, real, imag):
        gr.basic_block.__init__(self,
            name="Dynamic_Padder",
            in_sig=[np.complex64, ],
            out_sig=[np.complex64, ])

    def forecast(self, noutput_items, ninputs):
        # ninputs is the number of input connections
        # setup size of input_items[i] for work call
        # the required number of input items is returned
        #   in a list where each element represents the
        #   number of required items for each input
        ninput_items_required = [noutput_items] * ninputs
        return ninput_items_required

    def general_work(self, input_items, output_items):
        if self.padding is True:
            sub_input = input_items[0][:len(output_items[0]) -self.length ]

            output = np.append(sub_input, self.get_padding_array(self.length))
            
            output_items[0][:] = output
            self.consume(0, len(output_items[0])-self.length)

            self.padding = False
        else:
            output_items[0][:] = input_items[0][:len(output_items[0])]
            self.consume(0, len(output_items[0]))
            #self.consume_each(len(input_items[0]))

        return len(output_items[0])

    def set_padding(self, msg):

        self.length = int(pmt.symbol_to_string(msg))
	if self.length < 2000:
		self.padding = True

        print(self.length)
        #self.padding = True


    def get_padding_array(self, length):
        index = 0
        payload = []

        while index < length:
            payload.append(self.padding_sample)
            index = index +1

        return payload

        

