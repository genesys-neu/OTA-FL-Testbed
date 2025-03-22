#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Qpsk Ofdm
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
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
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import sip



class QPSK_OFDM(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Qpsk Ofdm", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Qpsk Ofdm")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "QPSK_OFDM")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

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
        self.NFFT = NFFT = 32

        ##################################################
        # Blocks
        ##################################################

        self.zero_padding_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("addr=10.10.23.7", "", "master_clock_rate=200e6")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_time_source('external', 0)
        self.uhd_usrp_sink_0.set_samp_rate(480e3)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(900e6, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(480e3, 0)
        self.uhd_usrp_sink_0.set_gain(31.5, 0)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            480e3, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.fft_vxx_0_0 = fft.fft_vcc(NFFT, False, (), False, 1)
        self.fft_vxx_0 = fft.fft_vcc(NFFT, False, (), False, 1)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, NFFT)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, NFFT)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, NFFT)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, NFFT)
        self.blocks_stream_mux_1 = blocks.stream_mux(gr.sizeof_gr_complex*1, (trainingSignal_size, 400, 32, 256 * 103, 100))
        self.blocks_repeat_0_0_0_1_0 = blocks.repeat(gr.sizeof_gr_complex*1, (100* numTxAntennas))
        self.blocks_repeat_0_0_0_1 = blocks.repeat(gr.sizeof_gr_complex*1, (400 * numTxAntennas))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_cc(0.17)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(0.1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.17)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.PMT_T, 50)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/root/Suyash_OTA_FL/gr-OTA_FL/data/QPSK.bin', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/root/Suyash_OTA_FL/gr-OTA_FL/data/Ones.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.OTA_FL_read_gold_seq_0 = OTA_FL.read_gold_seq(<mako.runtime.TemplateNamespace object at 0x7fab79adea30>, )


        ##################################################
        # Connections
        ##################################################
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
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.zero_padding_0_0_0, 0), (self.blocks_repeat_0_0_0_1, 0))
        self.connect((self.zero_padding_0_0_0, 0), (self.blocks_repeat_0_0_0_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "QPSK_OFDM")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

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




def main(top_block_cls=QPSK_OFDM, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
