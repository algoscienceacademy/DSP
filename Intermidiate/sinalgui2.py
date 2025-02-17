import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
                              QComboBox, QPushButton, QFileDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import scipy.fft

class DSPApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Signal Processing")
        self.setGeometry(100, 100, 1200, 800)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create plot
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create controls
        controls_layout = QHBoxLayout()
        layout.addLayout(controls_layout)

        # Signal parameters
        signal_group = QVBoxLayout()
        controls_layout.addLayout(signal_group)

        # Signal type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Signal Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Sine", "Square", "Triangle"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        signal_group.addLayout(type_layout)

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

        # Phase control
        phase_layout = QHBoxLayout()
        phase_label = QLabel("Phase (degrees):")
        self.phase_spin = QDoubleSpinBox()
        self.phase_spin.setRange(0, 360)
        self.phase_spin.setValue(0)
        phase_layout.addWidget(phase_label)
        phase_layout.addWidget(self.phase_spin)
        signal_group.addLayout(phase_layout)

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

        # Information display
        self.info_label = QLabel()
        layout.addWidget(self.info_label)

        # Add Save/Load buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Signal")
        self.load_button = QPushButton("Load Signal")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        layout.addLayout(button_layout)

        # Connect signals
        self.freq_spin.valueChanged.connect(self.update_plot)
        self.amp_spin.valueChanged.connect(self.update_plot)
        self.samp_freq_spin.valueChanged.connect(self.update_plot)
        self.quant_spin.valueChanged.connect(self.update_plot)
        self.type_combo.currentTextChanged.connect(self.update_plot)
        self.phase_spin.valueChanged.connect(self.update_plot)
        self.save_button.clicked.connect(self.save_signal)
        self.load_button.clicked.connect(self.load_signal)

        # Initial plot
        self.update_plot()

    def generate_signal(self, t, freq, amp, phase_deg):
        phase_rad = np.deg2rad(phase_deg)
        signal_type = self.type_combo.currentText()
        
        if signal_type == "Sine":
            return amp * np.sin(2 * np.pi * freq * t + phase_rad)
        elif signal_type == "Square":
            return amp * np.sign(np.sin(2 * np.pi * freq * t + phase_rad))
        else:  # Triangle
            return amp * (2/np.pi) * np.arcsin(np.sin(2 * np.pi * freq * t + phase_rad))

    def update_plot(self):
        self.figure.clear()
        
        # Signal parameters
        freq = self.freq_spin.value()
        amp = self.amp_spin.value()
        fs = self.samp_freq_spin.value()
        bits = self.quant_spin.value()
        phase = self.phase_spin.value()

        # Time vector for analog signal
        t = np.linspace(0, 0.5, 1000)
        analog_signal = self.generate_signal(t, freq, amp, phase)

        # Sampling
        ts = np.arange(0, 0.5, 1/fs)
        sampled_signal = self.generate_signal(ts, freq, amp, phase)

        # Add some noise to sampled signal
        noise = np.random.normal(0, 0.1, len(sampled_signal))
        noisy_signal = sampled_signal + noise

        # Quantization
        levels = 2**bits
        quantized_signal = np.round(noisy_signal * (levels-1)/2) * 2/(levels-1)

        # Calculate SNR
        signal_power = np.mean(sampled_signal**2)
        noise_power = np.mean((noisy_signal - sampled_signal)**2)
        snr_db = 10 * np.log10(signal_power/noise_power)

        # FFT Analysis
        fft_result = scipy.fft.fft(quantized_signal)
        freq_axis = scipy.fft.fftfreq(len(ts), 1/fs)

        # Plotting (now 2x2 grid)
        ax1 = self.figure.add_subplot(221)
        ax1.plot(t, analog_signal, 'b-', label='Analog Signal')
        ax1.plot(ts, sampled_signal, 'r.', label='Sampled Points')
        ax1.set_title('Analog Signal and Sampling')
        ax1.grid(True)
        ax1.legend()

        ax2 = self.figure.add_subplot(222)
        ax2.plot(ts, noisy_signal, 'b-', label='Noisy Signal')
        ax2.plot(ts, quantized_signal, 'r--', label='Quantized Signal')
        ax2.set_title('Quantization')
        ax2.grid(True)
        ax2.legend()

        ax3 = self.figure.add_subplot(223)
        ax3.stem(ts, quantized_signal, label='Digital Signal')
        ax3.set_title('Digital Signal')
        ax3.grid(True)
        ax3.legend()

        ax4 = self.figure.add_subplot(224)
        ax4.plot(freq_axis[:len(freq_axis)//2], 
                np.abs(fft_result)[:len(freq_axis)//2], 
                label='FFT')
        ax4.set_title('Frequency Spectrum')
        ax4.grid(True)
        ax4.legend()

        self.canvas.draw()

        # Update information
        nyquist = fs/2
        if freq > nyquist:
            alias_freq = abs(freq - fs * round(freq/fs))
            alias_info = f"Aliasing detected! Alias frequency: {alias_freq:.1f} Hz"
        else:
            alias_info = "No aliasing"

        info_text = (f"Nyquist frequency: {nyquist} Hz\n"
                    f"{alias_info}\n"
                    f"Quantization levels: {levels}\n"
                    f"SNR: {snr_db:.2f} dB")
        self.info_label.setText(info_text)

    def save_signal(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Signal", "", "NPY files (*.npy)")
        if filename:
            ts = np.arange(0, 0.5, 1/self.samp_freq_spin.value())
            signal = self.generate_signal(ts, self.freq_spin.value(), 
                                       self.amp_spin.value(), 
                                       self.phase_spin.value())
            np.save(filename, signal)

    def load_signal(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Signal", "", "NPY files (*.npy)")
        if filename:
            loaded_signal = np.load(filename)
            # TODO: Implement signal loading and parameter estimation
            self.update_plot()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DSPApp()
    window.show()
    sys.exit(app.exec())
