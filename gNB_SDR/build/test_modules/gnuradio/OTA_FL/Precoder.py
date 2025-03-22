#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Suyash Pradhan.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct
import pmt
import numpy as np
import sys
import math
import cmath
from gnuradio import gr
import json


# UDP related libraries
import socket
import struct
import threading
import time
import logging


class Precoder(gr.sync_block):
    
    """
    docstring for block Precoder
    """
    def __init__(self, file_path, number_of_tx_antennas, multicast_IP, multicast_port, Tx_ID):
        gr.sync_block.__init__(self,
            name="Precoder",
            in_sig=[(np.complex64, 256)],
            out_sig=[(np.complex64, 256)])
        ### Store and initialize generic object parameters
        self.numTxAntennas = number_of_tx_antennas
        self.file_path = file_path
        self.Tx_ID = int (Tx_ID)


        # Init input and output ports
        self.message_port_register_in(pmt.intern("trigger"))

        #self.set_msg_handler(pmt.intern("trigger"), self.send_beamweight)

        address = multicast_IP, int(multicast_port)
        self.UDP_socket = UDPServer(address, self.udp_packet_handler)
        self.UDP_socket.start()

        self.precoder_feedback = self.default_csi_calculation
        self.precoder = np.ones(256, dtype = np.complex64)

    def udp_packet_handler(self, json_package):
        de_serialized = json.loads(json_package)
        length = len(de_serialized)

        #print("JSON Decoded Data = ", de_serialized)

        update_in_delay = False
        try:
            target_object = de_serialized[0]

            #if int (target_object['Tx_ID']) != self.Tx_ID:
            #    raise Exception("Inconsistent Tx array from RX")
            #else:
                #print 'For TX {}'.format(self.Tx_ID)
            #print("DATA", str(target_object))
            real = np.array(target_object['real'])
            imaginary = np.array(target_object['imaginary'])
            #scaling_factor = target_object['Scaling Factor']

            ## Filter out the echos
            if int (target_object['delay']) > 0 and \
                    int (target_object['delay']) != self.delay:
                update_in_delay = True
                self.delay = int(target_object['delay'])


        except IndexError:
            print ("Transmitter number is out of index. - Tx: {}".format(self.Tx_ID))
        except KeyError as format_error:
            print ("Keys are not defined in the received packet:\n{}".format(format_error))
        except Exception as e:
            print (e)

        feedback = real + (1j * imaginary)
        print("Complex CSI =", feedback)

        #feedback = complex(real, imaginary)

        self.precoder = self.precoder_feedback(feedback)

    def default_csi_calculation(self, feedback):
        # Reconstructing channel estimation value in complex format
        channel_est_complex = feedback
        
        phase_correction = channel_est_complex
        precoder = 1 / phase_correction
        return precoder

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        #out[:] = in0 * self.precoder
        out[:] = in0
        #print("PF =", in0 / out[:])
        
        return len(output_items[0])

class UDPServer(threading.Thread):
    def __init__(self, address, udp_packet_handler):
        print("UDP server generated.")
        self.multicast_group = address[0]
        self.port = address[1]
        self.udp_packet_handler = udp_packet_handler
        threading.Thread.__init__(self)

    def run(self):
        try:
            # Create the socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Bind to the server address
            sock.bind(('', self.port))

            # Tell the operating system to add the socket to the multicast group
            # on all interfaces.
            group = socket.inet_aton(self.multicast_group)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        except socket.error as exp:
            print("Exception while creating the socket\n%s" % exp)
            sock.close()


        # Receive loop
        while True:
            try:
                data, address = sock.recvfrom(4096)
                data = data.decode()
                #print(data)
            except socket.timeout:
                print('timed out, no incoming CSI feedback')
                break
            #else:
                #print('received "%s" from %s - time: %f ' % (data, address, time.time() ) )
                #self.udp_packet_handler(data)
