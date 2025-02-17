import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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

        # Information display
        self.info_label = QLabel()
        layout.addWidget(self.info_label)

        # Connect signals
        self.freq_spin.valueChanged.connect(self.update_plot)
        self.amp_spin.valueChanged.connect(self.update_plot)
        self.samp_freq_spin.valueChanged.connect(self.update_plot)
        self.quant_spin.valueChanged.connect(self.update_plot)

        # Initial plot
        self.update_plot()

    def update_plot(self):
        self.figure.clear()

        # Signal parameters
        freq = self.freq_spin.value()
        amp = self.amp_spin.value()
        fs = self.samp_freq_spin.value()
        bits = self.quant_spin.value()

        # Time vector for analog signal
        t = np.linspace(0, 0.5, 1000)
        analog_signal = amp * np.sin(2 * np.pi * freq * t)

        # Sampling
        ts = np.arange(0, 0.5, 1/fs)
        sampled_signal = amp * np.sin(2 * np.pi * freq * ts)

        # Quantization
        levels = 2**bits
        quantized_signal = np.round(sampled_signal * (levels-1)/2) * 2/(levels-1)

        # Plotting
        ax1 = self.figure.add_subplot(311)
        ax1.plot(t, analog_signal, 'b-', label='Analog Signal')
        ax1.plot(ts, sampled_signal, 'r.', label='Sampled Points')
        ax1.set_title('Analog Signal and Sampling')
        ax1.grid(True)
        ax1.legend()

        ax2 = self.figure.add_subplot(312)
        ax2.plot(ts, sampled_signal, 'b-', label='Original Samples')
        ax2.plot(ts, quantized_signal, 'r--', label='Quantized Signal')
        ax2.set_title('Quantization')
        ax2.grid(True)
        ax2.legend()

        ax3 = self.figure.add_subplot(313)
        ax3.stem(ts, quantized_signal, label='Digital Signal')
        ax3.set_title('Digital Signal')
        ax3.grid(True)
        ax3.legend()

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
                    f"Quantization levels: {levels}")
        self.info_label.setText(info_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DSPApp()
    window.show()
    sys.exit(app.exec())