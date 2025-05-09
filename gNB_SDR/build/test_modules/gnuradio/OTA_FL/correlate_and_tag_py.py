#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Suyash Pradhan.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import socket
import struct
import json
import numpy as np
import os

try:
    from scipy import signal
except:
    print ("WARNING: Scipy module is not loaded. FFT-based cor. cannot be used.")
import pmt
from gnuradio import gr
import time

## Python libraries naming inconsistency
try:
    import queue
except:
    import Queue as queue

import numpy
from gnuradio import gr
from collections import deque

class correlate_and_tag_py(gr.sync_block):
    """
    docstring for block correlate_and_tag_py
    """
    def __init__(self, seq_len, frame_len, num_Tx, file_path, cor_method,feedback_type):
        gr.sync_block.__init__(self,
            name="correlate_and_tag_py",
            in_sig=[numpy.complex64],
            out_sig=[numpy.complex64, numpy.complex64])

        self.gold_seq_length = seq_len
        self.frame_length = frame_len
        self.payload_size = frame_len - seq_len - 500
        self.num_active_Tx = num_Tx
        self.debug = False
        self.fft_size = 256


        """Set UDP SERVER"""
        #self.multicast_group = ('224.3.29.71', 10000)

        # Create the socket
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the server address
        # sock.bind(server_address)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces
        '''try:
            group = socket.inet_aton('224.3.29.71')
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception as e:
            logging.exception("Cannot init multicast UDP socket: {}".format(e))
        '''
        """Get Gold Sequences"""
        self.gold_sequences = np.empty((num_Tx, self.gold_seq_length),
                                          np.complex64)

        for tx_index in range(num_Tx):
            self.gold_sequences[tx_index,:] = np.array(self.get_training_signal(file_path, tx_index))

        """Internal Buffers"""
        self.buffer = []
        #self.buffer = deque(maxlen = 16456 + 53100)
        self.output =  []
        self.corr_output = []
        #self.test = np.zeros(16456 + 53100)

        """Internal States"""
        self.delay = True
        self.transmit = False

        self.correlation_window = []

        """Init fft method"""
        # Use fft based correlation
        if cor_method == 1:
            print("FFT-based correlation init.")
            self.correlate = self.signal_fft_correllation
        elif cor_method == 0 : # Default correlation function
            print("Default correlation init.")
            self.correlate = self.numpy_correlation
        else:
            print("Undefined correlation type.")
            self.correlate = None

        """ Init CFO est type"""
        # if cfo_method == 1:
        #     self.corrCFO = self.numpy_correlation

        """ Init feedback type"""
        if feedback_type == 0: # Send only channel information
            self.generate_feedback = self.default_csi_feedback

    def work(self, input_items, output_items):
        self.debug = False

        in0 = input_items[0]
        out = output_items[0]
        corr_out = output_items[1]

        '''output_items[0][:] = input_items[0]'''

        if self.debug:
            print( "Size of input: {} \t output: {}-{} buffers".format(len(in0), len(out), len(corr_out)))
        
        self.buffer.extend(in0)
        '''
        #self.buffer = np.concatenate([self.buffer, in0[:]])

        #x = np.divide(self.buffer, np.ones(len(self.buffer)))

        #self.test = self.buffer
        #x = np.divide(self.test, self.test)
        #self.buffer = np.append(self.buffer, in0)
        '''

        if self.debug:
            print( "Size of internal buffer: {}".format(len(self.buffer)))
        
        """ Buffer has enough samples to run XCOR"""
        # buffer : internal buffer
        # correlation_window : items might be left after previous correlation
        # gold_seq_length
        # frame_length
        if len(self.buffer) + len(self.correlation_window) > self.gold_seq_length + self.frame_length:
            output_head = self.nitems_written(0)
            corr_output_head = self.nitems_written(1)

            initial_size = len(self.correlation_window)
            # Add items (samples) to correlation window
            #   to make its size equals gold_seq_length+frame_length

            item_size_to_add =  self.gold_seq_length + self.frame_length - initial_size
            self.correlation_window.extend(self.buffer[:item_size_to_add])
            self.buffer = self.buffer[item_size_to_add:]

            ## Variables which construct feedback
            channel_estimations = np.ones(self.num_active_Tx, dtype=np.complex64)
            CHEST = np.ones((self.num_active_Tx, self.fft_size), dtype=np.complex64)
            delays = np.zeros(self.num_active_Tx, dtype=np.int32)
            corr_indices = np.zeros(self.num_active_Tx, dtype=np.int32)
            found_flags = np.zeros(self.num_active_Tx, dtype=np.int32)

            # index to push samples to output buffer,
            # not related with the feedback
            push_index = 0

            ## a loop implemented for all active transmitters
            # run cross correlation to detect peaks and
            # calculate CSI
            for tx_index in range(self.num_active_Tx):
                self.debug = False

                if self.debug:	print(tx_index)
                s_time = time.time()
                x_cor_result = self.correlate(self.correlation_window, self.gold_sequences[tx_index])
                e_time = time.time()
                # cfo_cor_result = self.corrCFO(self.correlation_window, self.gold_sequences[tx_index])
                #sum_cfo = numpy.angle(x_cor_result)


                print("Xcorr calculation time: {} seconds".format(e_time - s_time))
                # print ("Xcorr calculation time: {} seconds".format(e_time - s_time))
                self.debug = False
                if self.debug:
                    print( "XCOR output type: {} \t size: {}".format(
                                        type(x_cor_result),
                                        len(x_cor_result)))
                    #print("CFO: {}\n".format(sum_cfo[0]))
                    print("xcorr value {}".format(x_cor_result[0]))
                    # print( "CFO_corr output type: {} \t size: {}".format(
                    #                     type(cfo_cor_result),
                    #                     len(cfo_cor_result)))

                self.debug = False
                ## MATLAB CODE
                # peakIntervals1 = find(abs(crossCorr{1})>(0.8*max(abs(crossCorr{1}))));

                tag_index = np.argmax(np.absolute(x_cor_result))
                peak_indices = self.get_peaks(x_cor_result)

                print("Tx: {} - Max item index: {}, First Peak index: {}".format(tx_index+1, tag_index, peak_indices[0] ))

                if peak_indices[0] > push_index:
                    push_index = peak_indices[0]

                # Calculate CSI
                s_index_of_gold_seq = int(peak_indices[0] - self.gold_seq_length/2)
                e_index_of_gold_seq = int(s_index_of_gold_seq +  self.gold_seq_length)

                #s_index_DMRS = int(peak_indices[0] + (self.gold_seq_length/2) + 400)
                #e_index_DMRS = int(s_index_of_gold_seq +  self.gold_seq_length + 400 + self.fft_size)

                #DMRS = (np.fromfile(open("/home/genesys/Demo_BS/Suyash_OTA_FL/gr-OTA_FL/data/Ones.bin"), dtype = np.complex64))
                #print("DMRS SHAPEEE = ", DMRS.shape)


#                if s_index_of_gold_seq >= 0 and e_index_of_gold_seq <= len(self.correlation_window):
                if  e_index_of_gold_seq <= len(self.correlation_window):
                    corr_indices[tx_index] = s_index_of_gold_seq
                    found_flags[tx_index] = 1
                    print ("Training Signal starts :{} ends {}".format(s_index_of_gold_seq, e_index_of_gold_seq ))
                    """
                    print  numpy.divide(
                            self.correlation_window[s_index_of_gold_seq:e_index_of_gold_seq],
                            self.gold_sequences[tx_index], out=numpy.zeros_like(self.correlation_window[s_index_of_gold_seq:e_index_of_gold_seq]), where=self.gold_sequences[tx_index]!=0
                        )
                    print numpy.mean(   numpy.divide(
                        self.correlation_window[s_index_of_gold_seq:e_index_of_gold_seq],
                        self.gold_sequences[tx_index], out=numpy.zeros_like(self.correlation_window[s_index_of_gold_seq:e_index_of_gold_seq]), where=self.gold_sequences[tx_index]!=0
                    )           )
                    """

                    self.debug = False

                    ## Channel states
                    # @todo assign value to channel_estimations[tx_index]
                    # @todo if it is zero make it one\
                    if s_index_of_gold_seq < 0:
                        s_index_of_gold_seq = 0
                        rec_gs = np.array(self.correlation_window[s_index_of_gold_seq:e_index_of_gold_seq])
                        stored_gs = np.array((self.gold_sequences[tx_index])[s_index_of_gold_seq:e_index_of_gold_seq])

                        #rec_DMRS = np.array(self.correlation_window[s_index_DMRS:e_index_DMRS])
                        #stored_DMRS = np.array(DMRS)

                    else:
                        rec_gs = np.array(self.correlation_window[s_index_of_gold_seq:e_index_of_gold_seq])
                        stored_gs = np.array(self.gold_sequences[tx_index])

                        #rec_DMRS = np.array(self.correlation_window[s_index_DMRS:e_index_DMRS])
                        #stored_DMRS = np.array(DMRS)

                        print ("rec_gs", np.mean(np.abs((rec_gs))))
                        print ("stored_gs", np.mean(np.abs((stored_gs))))
                    
                    channel_estimations[tx_index] = np.nanmean(np.divide(rec_gs, stored_gs, out=np.zeros_like(rec_gs), where=stored_gs!=0))
                    #CHEST[tx_index] = np.divide(rec_DMRS, stored_DMRS, out=np.zeros_like(rec_DMRS), where=stored_DMRS!=0)
		    
                if self.debug: 
                    print("Tx: {} CSI: {}".format(tx_index+1, channel_estimations[tx_index]))

                else:
                    self.debug = False
                    found_flags[tx_index] = 0
                    if self.debug: print("Could not correlate training signal {}".format(tx_index+1))

                # Create the TAGS
                key_flow = pmt.intern("training_Sig_{}".format(tx_index+1))
                value_flow = pmt.intern(str(self.gold_seq_length))
                # srcid = pmt.intern("sourceID")

                key_xcor = pmt.intern("training_Sig_{}".format(tx_index+1))
                value_xcor  = pmt.intern(str(peak_indices[0]))

                # attach TAGS to the output streams
                self.add_item_tag(0,
                                  int(output_head
                                  + len(self.output) # Items waiting in output queue
                                  + peak_indices[0]
                                  - self.gold_seq_length/2)
                                  , key_flow, value_flow)

                self.add_item_tag(1, int(corr_output_head
                                  + len(self.corr_output) # Items waiting in output queue
                                  + peak_indices[0])
                                  , key_xcor, value_xcor)
                ## @note always mark payload based on the 1st Tx
                if tx_index == 0 :
                    key_payload = pmt.intern("payload")
                    value_payload = pmt.intern(str(self.payload_size))
                    self.add_item_tag(0,
                                      int(output_head
                                      + len(self.output) # Items waiting in output queue
                                      + peak_indices[0]
                                      + self.gold_seq_length/2
                                      + 400) # zero padding comes after Gold Seq.
                                      , key_payload, value_payload)


            max_index = int(np.max(corr_indices))

            # Calculate the individual delay values
            for tx_index in range(self.num_active_Tx):
                if int(found_flags[tx_index]) == 1:
                    possible_delay = max_index - int(corr_indices[tx_index])
                    if possible_delay < 500:
                        delays[tx_index] = possible_delay
                    else:
                        delays[tx_index] = 0
                if self.debug: print("Tx: {} Delay: {}".format(tx_index+1,  delays[tx_index]))
                #delays[tx_index] = 0

            feedback_weights = self.generate_feedback(channel_estimations)
            #CHEST = np.array(CHEST, dtype = np.complex128)[:, 0:16]

            dict_objects = []
            ## Fill out dictionary used in feedback
            for tx_index in range(self.num_active_Tx):
                dict_objects.append(
                    {
                        "Tx_ID": int(tx_index+1),
                        #"real": np.real(CHEST[tx_index]).tolist(),
                        #"imaginary": np.imag(CHEST[tx_index]).tolist()
                        #"delay": int(delays[tx_index])
                    }
                )


            self.debug = True
            if self.debug: 
                print("JSON: {}".format(str(dict_objects)))


            #serialized = json.dumps(dict_objects, indent = 4)
            #self.sock.sendto(serialized.encode(), self.multicast_group)


            self.debug = False

            # Push one frame
            push_size = int(push_index + self.frame_length - self.gold_seq_length/2)

            if self.debug: 
                print( "Sample size pushed to output buffers: {}".format(push_size))

            self.output.extend(self.correlation_window[:push_size])
            self.corr_output.extend(x_cor_result[:push_size])

            self.correlation_window = self.correlation_window[push_size:]

        if len (self.output) > len(out):
            out[:] = self.output[:len(out)]
            self.output = self.output[len(out):]

        if len(self.corr_output) > len(corr_out):
            corr_out[:] = self.corr_output[:len(out)]
            self.corr_output = self.corr_output[len(out):]

        if self.debug:
            print( "Sizes of buffers\nout: {}, c_out: {}, in: {}".format(len(out), len(corr_out), len(in0)))
        return len(in0)

    def get_peaks(self, correlation_output):

        self.debug = False
        expected_distance = 100 # If the dist is greater, another cluster

        filtered_candidates = []
        max_samp = np.absolute(correlation_output).max()

        peak_candidates = np.nonzero(np.absolute(correlation_output) > max_samp*0.80)[0]
        if self.debug:
            print("Values bigger than max*0.80 = ", np.absolute(correlation_output)[np.absolute(correlation_output) > max_samp*0.95])
            print("Their indices are ", peak_candidates)

        t_peak = None
        for candidate in  peak_candidates:
            if t_peak is None:
                t_peak = candidate

            elif abs(candidate - t_peak) < expected_distance: # They are in the same cluster
                if np.absolute(correlation_output[candidate]) > np.absolute(correlation_output[t_peak]):
                    t_peak = candidate
            else:
                # candidate belongs to a different cluster
                filtered_candidates.append(t_peak)
                # the first element of next cluster
                t_peak = candidate

        # push the head of last cluster
        filtered_candidates.append(t_peak)

        if self.debug:            print("Candidates: {}", filtered_candidates)

        self.debug = False
        return filtered_candidates


    ## Reads Gold Sequences from a file
    def get_training_signal(self, file_path, number_Tx):

        gold_sequence = []

        # Enumeration starts with 1 in files
        Tx_index = int(number_Tx) + 1

        dir_path = os.path.dirname(os.path.realpath(__file__))

        if self.debug:
            print ("Data Path at cor_and_tag block: {}".format(dir_path))


        # Real part of the payload read from 'payload_real.txt' file
        with open( file_path + str(Tx_index) + '_real.txt', 'r') as f:
            pay_real = [line.strip() for line in f]

        length = (len(pay_real))

        # Imaginary part of the payload read from 'payload_imag.txt' file
        with open(file_path + str(Tx_index) + '_imag.txt', 'r') as f1:
            pay_imag = [line.strip() for line in f1]

        # Reconstructing the payload in complex format
        for ii in range(length):
            data_p_c = complex(float(pay_real[ii]), float(pay_imag[ii]))
            data = np.complex64(data_p_c)
            gold_sequence.append(data)


        print("Training Signal {} is successfully retrieved from the target files.".format(Tx_index))

        return gold_sequence

    ## Feedback adapters
    def default_csi_feedback(self, channel_estimations):
        print("CHEST Value:", channel_estimations)
        print('{},{}'.format(int(time.time()*1000000),channel_estimations))

        return channel_estimations

    ## Correlation adapter functions
    def numpy_correlation(self, in1, in2):
        return  numpy.correlate(in1, in2, mode='same')

    def signal_fft_correllation(self,in1, in2):
        return signal.correlate(in1, in2, mode='same',method='fft')
