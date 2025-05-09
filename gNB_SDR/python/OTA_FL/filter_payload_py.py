#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Suyash Pradhan.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr

class filter_payload_py(gr.basic_block):
    """
    docstring for block filter_payload_py
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="filter_payload_py",
            in_sig=[np.complex64],
            out_sig=[np.complex64])

        self.tag_name = "payload"
        self.transmit = False
        self.end_of_payload = -1
        self.start_of_payload = -1

        self.debug = False


    '''def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items'''

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        s_index = np.uint64(self.nitems_read(0))
        # There is no payload just consume input

        if self.debug:
            print ("Size of input buffer: {}, samples read: {} ".format(len(in0),self.nitems_read(0)))


        tags = self.get_tags_in_window(0, 0, len(in0))

        for tag in tags:
            if str(tag.key) == self.tag_name:
                if self.debug: print ("Size of input buffer: {}, samples read: {}, tag index:{} ".format(len(in0),self.nitems_read(0),tag.offset))
                # uint64_t gr::block::nitems_read	(	unsigned int 	which_input	)
                self.transmit = True
                self.end_of_payload = np.uint64(tag.offset + np.uint64(str(tag.value)))
                self.start_of_payload =  np.uint64(tag.offset)

        ## Following if/else statement
        #
        # 4 Major Cases
        # - Payload head is in active batch
        # - Payload head and end are not in active batch but batch is the subset of payload
        # - Payload end is in active batch
        # - Payload head and end are not in active batch, batch is not part of payload
        #
        # 2 Minor Cases
        # - output buffer is smaller then the number of elements to be sent
        # - else ...
        #
        # Good luck with understanding the index adjustments. - GKN March 13, 2019
        #
        if  s_index < self.start_of_payload < s_index+len(in0):
            # Payload starts in this input batch
            unused_item_size = int (self.start_of_payload - s_index)

            items_to_send = len(in0) - unused_item_size
            if len(out) >  items_to_send:
                out[:items_to_send] = in0[unused_item_size:]
                self.consume(0, len(in0)) # consume all input buffer
                return items_to_send
            else:
                out[:] = in0[unused_item_size:unused_item_size +len(out)]
                self.consume(0, unused_item_size + len(out))
                return len(out)

        elif s_index + len(in0) < self.end_of_payload:
            # Payload overlaps this input batch
            if len(out) < len(in0):
                out[:] = in0[:len(out)]
                self.consume(0, len(out))
                return len(out)
            else:
                out[:len(in0)] = in0[:]
                self.consume(0, len(in0))
                return len(in0)

        elif s_index < self.end_of_payload < s_index + len(in0):
            # Payload ends in this input batch
            remaining_size = int(self.end_of_payload-s_index)
            if remaining_size < len(out):
                out[:remaining_size] = in0[:remaining_size]
                self.consume(0, remaining_size)
                return remaining_size
            else:
                out[:] = in0[:len(out)]
                self.consume(0, len(out))
                return len(out)

        elif self.end_of_payload <= s_index:
            # There is no payload just consume input
            self.consume(0, len(in0))
            return 0


