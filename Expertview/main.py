import sys
import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import scipy.signal
import scipy.io.wavfile
import pandas as pd

class DSPApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Signal Processing")
        self.setGeometry(100, 100, 1200, 800)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Add tabs for different views
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Time domain tab
        time_tab = QWidget()
        time_layout = QVBoxLayout(time_tab)
        self.time_figure = Figure(figsize=(12, 8))
        self.time_canvas = FigureCanvas(self.time_figure)
        time_layout.addWidget(self.time_canvas)
        self.tab_widget.addTab(time_tab, "Time Domain")

        # Frequency domain tab
        freq_tab = QWidget()
        freq_layout = QVBoxLayout(freq_tab)
        self.freq_figure = Figure(figsize=(12, 8))
        self.freq_canvas = FigureCanvas(self.freq_figure)
        freq_layout.addWidget(self.freq_canvas)
        self.tab_widget.addTab(freq_tab, "Frequency Domain")

        # Add Digital Analysis tab
        digital_tab = QWidget()
        digital_layout = QVBoxLayout(digital_tab)
        self.digital_figure = Figure(figsize=(12, 8))
        self.digital_canvas = FigureCanvas(self.digital_figure)
        digital_layout.addWidget(self.digital_canvas)
        self.tab_widget.addTab(digital_tab, "Digital Analysis")

        # Create controls
        controls_layout = QHBoxLayout()
        layout.addLayout(controls_layout)

        # Signal parameters
        signal_group = QVBoxLayout()
        controls_layout.addLayout(signal_group)

        # Frequency control
        freq_layout = QHBoxLayout()
        freq_label = QLabel("Signal Frequency (Hz):")
        self.freq_spin = QSpinBox()
        self.freq_spin.setRange(1, 1000)
        self.freq_spin.setValue(10)
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(self.freq_spin)
        signal_group.addLayout(freq_layout)

        # Amplitude control
        amp_layout = QHBoxLayout()
        amp_label = QLabel("Amplitude:")
        self.amp_spin = QDoubleSpinBox()
        self.amp_spin.setRange(0.1, 10.0)
        self.amp_spin.setValue(1.0)
        amp_layout.addWidget(amp_label)
        amp_layout.addWidget(self.amp_spin)
        signal_group.addLayout(amp_layout)

        # Sampling frequency control
        sampling_group = QVBoxLayout()
        controls_layout.addLayout(sampling_group)

        samp_freq_layout = QHBoxLayout()
        samp_freq_label = QLabel("Sampling Frequency (Hz):")
        self.samp_freq_spin = QSpinBox()
        self.samp_freq_spin.setRange(1, 2000)
        self.samp_freq_spin.setValue(100)
        samp_freq_layout.addWidget(samp_freq_label)
        samp_freq_layout.addWidget(self.samp_freq_spin)
        sampling_group.addLayout(samp_freq_layout)

        # Quantization levels control
        quant_layout = QHBoxLayout()
        quant_label = QLabel("Quantization Bits:")
        self.quant_spin = QSpinBox()
        self.quant_spin.setRange(1, 16)
        self.quant_spin.setValue(8)
        quant_layout.addWidget(quant_label)
        quant_layout.addWidget(self.quant_spin)
        sampling_group.addLayout(quant_layout)

        # Add advanced controls
        advanced_group = QVBoxLayout()
        controls_layout.addLayout(advanced_group)

        # Window function selection
        window_layout = QHBoxLayout()
        window_label = QLabel("Window Function:")
        self.window_combo = QComboBox()
        self.window_combo.addItems(["None", "Hamming", "Hanning", "Blackman"])
        window_layout.addWidget(window_label)
        window_layout.addWidget(self.window_combo)
        advanced_group.addLayout(window_layout)

        # Filter controls
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter Type:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["None", "Lowpass", "Highpass", "Bandpass"])
        self.cutoff_spin = QSpinBox()
        self.cutoff_spin.setRange(1, 1000)
        self.cutoff_spin.setValue(50)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(QLabel("Cutoff (Hz):"))
        filter_layout.addWidget(self.cutoff_spin)
        advanced_group.addLayout(filter_layout)

        # Animation controls
        anim_layout = QHBoxLayout()
        self.animate_btn = QPushButton("Toggle Animation")
        self.animate_btn.setCheckable(True)
        anim_layout.addWidget(self.animate_btn)
        advanced_group.addLayout(anim_layout)

        # Export controls
        export_layout = QHBoxLayout()
        self.export_btn = QPushButton("Export")
        self.export_combo = QComboBox()
        self.export_combo.addItems(["WAV", "CSV", "NPY", "MAT"])
        export_layout.addWidget(self.export_btn)
        export_layout.addWidget(self.export_combo)
        advanced_group.addLayout(export_layout)

        # Add Digital Signal Controls
        digital_group = QVBoxLayout()
        controls_layout.addLayout(digital_group)

        # PCM encoding type
        pcm_layout = QHBoxLayout()
        pcm_label = QLabel("PCM Encoding:")
        self.pcm_combo = QComboBox()
        self.pcm_combo.addItems(["Unipolar", "Polar NRZ", "Bipolar RZ"])
        pcm_layout.addWidget(pcm_label)
        pcm_layout.addWidget(self.pcm_combo)
        digital_group.addLayout(pcm_layout)

        # Digital Filter Order
        filter_order_layout = QHBoxLayout()
        filter_order_label = QLabel("Filter Order:")
        self.filter_order_spin = QSpinBox()
        self.filter_order_spin.setRange(1, 8)
        self.filter_order_spin.setValue(4)
        filter_order_layout.addWidget(filter_order_label)
        filter_order_layout.addWidget(self.filter_order_spin)
        digital_group.addLayout(filter_order_layout)

        # Information display
        self.info_label = QLabel()
        layout.addWidget(self.info_label)

        # Connect signals
        self.freq_spin.valueChanged.connect(self.update_plot)
        self.amp_spin.valueChanged.connect(self.update_plot)
        self.samp_freq_spin.valueChanged.connect(self.update_plot)
        self.quant_spin.valueChanged.connect(self.update_plot)
        self.window_combo.currentTextChanged.connect(self.update_plot)
        self.filter_combo.currentTextChanged.connect(self.update_plot)
        self.cutoff_spin.valueChanged.connect(self.update_plot)
        self.animate_btn.toggled.connect(self.toggle_animation)
        self.export_btn.clicked.connect(self.export_signal)
        self.pcm_combo.currentTextChanged.connect(self.update_plot)
        self.filter_order_spin.valueChanged.connect(self.update_plot)

        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.animation_phase = 0

        # Initial plot
        self.update_plot()

    def apply_window(self, signal):
        window_type = self.window_combo.currentText()
        if window_type == "None":
            return signal
        N = len(signal)
        if window_type == "Hamming":
            window = np.hamming(N)
        elif window_type == "Hanning":
            window = np.hanning(N)
        else:  # Blackman
            window = np.blackman(N)
        return signal * window

    def apply_filter(self, signal, fs):
        filter_type = self.filter_combo.currentText()
        if filter_type == "None":
            return signal
        
        cutoff = self.cutoff_spin.value()
        nyquist = fs / 2
        normalized_cutoff = cutoff / nyquist

        if filter_type == "Lowpass":
            b, a = scipy.signal.butter(4, normalized_cutoff, btype='low')
        elif filter_type == "Highpass":
            b, a = scipy.signal.butter(4, normalized_cutoff, btype='high')
        else:  # Bandpass
            b, a = scipy.signal.butter(4, [normalized_cutoff*0.5, normalized_cutoff], btype='band')
        
        return scipy.signal.filtfilt(b, a, signal)

    def update_animation(self):
        self.animation_phase += 0.1
        self.update_plot()

    def toggle_animation(self, checked):
        if checked:
            self.timer.start(50)
        else:
            self.timer.stop()

    def update_plot(self):
        # Clear both figures
        self.time_figure.clear()
        self.freq_figure.clear()

        # Generate and process signal
        freq = self.freq_spin.value()
        amp = self.amp_spin.value()
        fs = self.samp_freq_spin.value()
        bits = self.quant_spin.value()

        # Time vectors
        t = np.linspace(0, 0.5, 1000)
        ts = np.arange(0, 0.5, 1/fs)

        # Generate signal with animation phase
        if self.animate_btn.isChecked():
            analog_signal = amp * np.sin(2 * np.pi * freq * t + self.animation_phase)
            sampled_signal = amp * np.sin(2 * np.pi * freq * ts + self.animation_phase)
        else:
            analog_signal = amp * np.sin(2 * np.pi * freq * t)
            sampled_signal = amp * np.sin(2 * np.pi * freq * ts)

        # Apply window and filter
        processed_signal = self.apply_window(sampled_signal)
        processed_signal = self.apply_filter(processed_signal, fs)

        # Quantization
        levels = 2**bits
        quantized_signal = np.round(processed_signal * (levels-1)/2) * 2/(levels-1)

        # Time domain plotting
        ax1 = self.time_figure.add_subplot(211)
        ax1.plot(t, analog_signal, 'b-', label='Analog Signal')
        ax1.plot(ts, sampled_signal, 'r.', label='Sampled Points')
        ax1.set_title('Time Domain Analysis')
        ax1.grid(True)
        ax1.legend()

        ax2 = self.time_figure.add_subplot(212)
        ax2.plot(ts, processed_signal, 'g-', label='Processed Signal')
        ax2.plot(ts, quantized_signal, 'r--', label='Quantized Signal')
        ax2.grid(True)
        ax2.legend()

        # Frequency domain plotting
        fft_result = np.fft.fft(quantized_signal)
        freq_axis = np.fft.fftfreq(len(ts), 1/fs)

        ax3 = self.freq_figure.add_subplot(211)
        ax3.magnitude_spectrum(quantized_signal, Fs=fs)
        ax3.set_title('Magnitude Spectrum')

        ax4 = self.freq_figure.add_subplot(212)
        ax4.phase_spectrum(quantized_signal, Fs=fs)
        ax4.set_title('Phase Spectrum')

        self.time_canvas.draw()
        self.freq_canvas.draw()

        # Digital signal processing
        digital_signal = self.encode_pcm(quantized_signal)
        
        # Binary representation
        binary_values = np.round((digital_signal + 1) * ((2**bits - 1) / 2)).astype(int)
        binary_strings = [format(val, f'0{bits}b') for val in binary_values]

        # Digital domain plotting
        self.digital_figure.clear()
        
        # PCM waveform
        ax_pcm = self.digital_figure.add_subplot(311)
        ax_pcm.step(ts, digital_signal, 'g-', label='PCM Signal')
        ax_pcm.set_title(f'PCM Encoding ({self.pcm_combo.currentText()})')
        ax_pcm.grid(True)
        ax_pcm.legend()

        # Binary representation
        ax_bin = self.digital_figure.add_subplot(312)
        binary_display = binary_strings[:20]  # Show first 20 samples
        ax_bin.text(0.1, 0.5, ' '.join(binary_display), fontfamily='monospace')
        ax_bin.set_title('Binary Representation (first 20 samples)')
        ax_bin.axis('off')

        # Eye diagram
        ax_eye = self.digital_figure.add_subplot(313)
        self.plot_eye_diagram(digital_signal, fs, ax_eye)
        
        self.digital_canvas.draw()

        # Update information display
        nyquist = fs/2
        if freq > nyquist:
            alias_freq = abs(freq - fs * round(freq/fs))
            alias_info = f"Aliasing detected! Alias frequency: {alias_freq:.1f} Hz"
        else:
            alias_info = "No aliasing"

        info_text = (f"Nyquist frequency: {nyquist} Hz\n"
                    f"{alias_info}\n"
                    f"Quantization levels: {levels}\n"
                    f"Average bit rate: {freq * bits} bps")
        self.info_label.setText(info_text)

    def encode_pcm(self, quantized_signal):
        encoding = self.pcm_combo.currentText()
        digital_signal = np.zeros_like(quantized_signal)
        
        if encoding == "Unipolar":
            digital_signal = (quantized_signal + 1) / 2
        elif encoding == "Polar NRZ":
            digital_signal = quantized_signal
        else:  # Bipolar RZ
            for i in range(len(quantized_signal)):
                if quantized_signal[i] > 0:
                    digital_signal[i] = 1 if i % 2 == 0 else -1
                elif quantized_signal[i] < 0:
                    digital_signal[i] = -1 if i % 2 == 0 else 1
        
        return digital_signal

    def plot_eye_diagram(self, signal, fs, ax):
        # Create eye diagram
        samples_per_symbol = int(fs / (self.freq_spin.value() * 2))
        num_symbols = len(signal) // samples_per_symbol
        
        for i in range(num_symbols - 1):
            start_idx = i * samples_per_symbol
            end_idx = start_idx + samples_per_symbol * 2
            if end_idx <= len(signal):
                t = np.linspace(0, 2, samples_per_symbol * 2)
                ax.plot(t, signal[start_idx:end_idx], 'b-', alpha=0.1)
        
        ax.set_title('Eye Diagram')
        ax.grid(True)
        ax.set_xlabel('Symbol Period')
        ax.set_ylabel('Amplitude')

    def export_signal(self):
        export_type = self.export_combo.currentText()
        filename, _ = QFileDialog.getSaveFileName(self, "Export Signal", "",
            f"Signal files (*.{export_type.lower()})")
        
        if not filename:
            return

        # Generate signal data
        fs = self.samp_freq_spin.value()
        ts = np.arange(0, 0.5, 1/fs)
        signal = self.generate_processed_signal(ts)

        if export_type == "WAV":
            scipy.io.wavfile.write(filename, fs, signal.astype(np.float32))
        elif export_type == "CSV":
            pd.DataFrame({'time': ts, 'amplitude': signal}).to_csv(filename, index=False)
        elif export_type == "NPY":
            np.save(filename, signal)
        else:  # MAT
            scipy.io.savemat(filename, {'signal': signal, 'fs': fs})

    def generate_processed_signal(self, t):
        freq = self.freq_spin.value()
        amp = self.amp_spin.value()
        signal = amp * np.sin(2 * np.pi * freq * t)
        signal = self.apply_window(signal)
        signal = self.apply_filter(signal, self.samp_freq_spin.value())
        # Apply digital filter
        order = self.filter_order_spin.value()
        b = np.ones(order) / order  # Moving average filter
        signal = np.convolve(signal, b, mode='same')
        return signal

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DSPApp()
    window.show()
    sys.exit(app.exec())