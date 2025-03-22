#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Suyash Pradhan.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class addSubSelect(gr.sync_block):
    """
    docstring for block addSubSelect
    """
    def __init__(self, selector=True):
        gr.sync_block.__init__(self,
            name="addSubSelect",
            in_sig=[np.complex64,np.complex64],
            out_sig=[np.complex64])
        self.selector = selector

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]

        if (self.selector):
            output_items[0][:] = in0 + in1
        else:
            output_items[0][:] = in0 - in1

        return len(output_items[0])


