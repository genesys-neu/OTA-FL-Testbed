#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Dmrs Ofdm
# GNU Radio version: 3.10.10.0

from gnuradio import OTA_FL
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import sys
import os, threading
import subprocess
import datetime

class DMRS_OFDM(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dmrs Ofdm", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.tx_id_1 = tx_id_1 = 2
        self.tx_id_0 = tx_id_0 = 1
        self.trainingSignal_size = trainingSignal_size = 16456
        self.subcarrier_size = subcarrier_size = 1
        self.samp_rate_0 = samp_rate_0 = 400e3
        self.samp_rate = samp_rate = 400e3
        self.num_active_mod = num_active_mod = 6
        self.numTxAntennas = numTxAntennas = 1
        self.N_edge_zeros = N_edge_zeros = 4
        self.NFFT = NFFT = 256


        ##################################################
        # Blocks
        ##################################################

        self.zero_padding_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("addr=192.168.60.2", "", "master_clock_rate=200e6")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_time_source('external', 0)
        self.uhd_usrp_sink_0.set_samp_rate(3840e3)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(900e6, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(3840e3, 0)
        self.uhd_usrp_sink_0.set_gain(15, 0)
        self.fft_vxx_0_0 = fft.fft_vcc(NFFT, False, (), False, 1)
        self.fft_vxx_0 = fft.fft_vcc(NFFT, False, (), False, 1)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, NFFT)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, NFFT)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, NFFT)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, NFFT)
        self.blocks_stream_mux_1 = blocks.stream_mux(gr.sizeof_gr_complex*1, (trainingSignal_size, 400, NFFT, 37888, 100))
        self.blocks_repeat_0_0_0_1_0 = blocks.repeat(gr.sizeof_gr_complex*1, (100* numTxAntennas))
        self.blocks_repeat_0_0_0_1 = blocks.repeat(gr.sizeof_gr_complex*1, (400 * numTxAntennas))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_cc(0.0625)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(0.1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.0625)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.PMT_T, 50)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/genesys/Demo_BS/Suyash_OTA_FL/gr-OTA_FL/data/QPSK.bin', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/genesys/Demo_BS/Suyash_OTA_FL/gr-OTA_FL/data/Ones.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.OTA_FL_read_gold_seq_0 = OTA_FL.read_gold_seq("/home/genesys/Demo_BS/Suyash_OTA_FL/gr-OTA_FL/data/trainingSig1", )
        self.OTA_FL_Precoder_0 = OTA_FL.Precoder('', 1, '224.3.28.70', 10000, 1)

        ##################################################
	# Adding line for time sync purpose
	##################################################
        #	try:
        
        lock = threading.Lock()
        lock.acquire()

        '''client = ntplib.NTPClient()
        
        response = client.request('ntp.ubuntu.com')
        #os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
        #os.system(time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
        system_time_min = int(time.strftime('%M'))
        system_time_min = (system_time_min*60)

        print (system_time_min)
        system_time_sec = int(time.strftime('%S'))
        print (system_time_sec)
        system_time_str = (system_time_min + system_time_sec)
        wait_time = 60 - system_time_sec
        print ("Tranmission will start after {} seconds".format(wait_time))
        print(system_time_str)
        system_time = int(system_time_str)'''

        current_date = datetime.datetime.now()
        system_time_sec = int(current_date.strftime("%S"))
        #print("Test time = ", system_time_sec)

        system_time_min = int(time.strftime('%M'))
        system_time_min = (system_time_min*60)
        system_time_str = (system_time_min + system_time_sec)
        system_time = int(system_time_str)

        
        wait_time = 60 - system_time_sec
        #self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec_t(system_time +1))
        self.uhd_usrp_sink_0.set_time_next_pps(uhd.time_spec_t(system_time +1))
        self.uhd_usrp_sink_0.set_start_time(uhd.time_spec_t(system_time + wait_time))
        lock.release()
        print("Test time = ", wait_time)
        time.sleep(wait_time-2)
        print("Wait Over")


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.OTA_FL_Precoder_0, 'trigger'))
        self.connect((self.OTA_FL_Precoder_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.OTA_FL_read_gold_seq_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_stream_mux_1, 2))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_stream_mux_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_stream_mux_1, 3))
        self.connect((self.blocks_repeat_0_0_0_1, 0), (self.blocks_stream_mux_1, 1))
        self.connect((self.blocks_repeat_0_0_0_1_0, 0), (self.blocks_stream_mux_1, 4))
        self.connect((self.blocks_stream_mux_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.OTA_FL_Precoder_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.zero_padding_0_0_0, 0), (self.blocks_repeat_0_0_0_1, 0))
        self.connect((self.zero_padding_0_0_0, 0), (self.blocks_repeat_0_0_0_1_0, 0))


    def get_tx_id_1(self):
        return self.tx_id_1

    def set_tx_id_1(self, tx_id_1):
        self.tx_id_1 = tx_id_1

    def get_tx_id_0(self):
        return self.tx_id_0

    def set_tx_id_0(self, tx_id_0):
        self.tx_id_0 = tx_id_0

    def get_trainingSignal_size(self):
        return self.trainingSignal_size

    def set_trainingSignal_size(self, trainingSignal_size):
        self.trainingSignal_size = trainingSignal_size

    def get_subcarrier_size(self):
        return self.subcarrier_size

    def set_subcarrier_size(self, subcarrier_size):
        self.subcarrier_size = subcarrier_size

    def get_samp_rate_0(self):
        return self.samp_rate_0

    def set_samp_rate_0(self, samp_rate_0):
        self.samp_rate_0 = samp_rate_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_num_active_mod(self):
        return self.num_active_mod

    def set_num_active_mod(self, num_active_mod):
        self.num_active_mod = num_active_mod

    def get_numTxAntennas(self):
        return self.numTxAntennas

    def set_numTxAntennas(self, numTxAntennas):
        self.numTxAntennas = numTxAntennas
        self.blocks_repeat_0_0_0_1.set_interpolation((400 * self.numTxAntennas))
        self.blocks_repeat_0_0_0_1_0.set_interpolation((100* self.numTxAntennas))

    def get_N_edge_zeros(self):
        return self.N_edge_zeros

    def set_N_edge_zeros(self, N_edge_zeros):
        self.N_edge_zeros = N_edge_zeros

    def get_NFFT(self):
        return self.NFFT

    def set_NFFT(self, NFFT):
        self.NFFT = NFFT




def main(top_block_cls=DMRS_OFDM, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
