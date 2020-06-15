from socscrollsave.ui.mainWindow_ui import *
from socscrollsave.core.worker import Worker
from socscrollsave.core.constants import Constants
from socscrollsave.common.logger import Logger as Log


TAG = "MainWindow"


class MainWindow(QtGui.QMainWindow):
    """
    Handles the ui elements and connects to worker service to execute processes.
    """
    def __init__(self, port=None, bd=115200, samples=500):
        """
        Initializes values for the UI.
        :param port: Default port name to be used. It will also disable scanning available ports.
        :type port: str.
        :param bd: Default baud rate to be used. It will be added to the common baud rate list if not available.
        :type bd: int.
        :param samples: Default samples per second to be shown in the plot.
        :type samples: int.
        """
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Shared variables, initial values
        self._plt = None
        self._timer_plot = None
        self.worker = Worker()
        self._configure_plot()
        self._configure_timers()
        self._configure_signals()
        self.ui.sBox_Samples.setValue(samples)

        # enable ui
        self._enable_ui(True)

    def start(self):
        """
        Starts the acquisition of the selected serial port.
        This function is connected to the clicked signal of the Start button.
        :return:
        """
        Log.i(TAG, "Clicked start")
        self.worker = Worker(samples=self.ui.sBox_Samples.value(),
                             export_enabled=self.ui.chBox_export.isChecked())
        if self.worker.start():
            self._timer_plot.start(Constants.plot_update_ms)
            self._enable_ui(False)


    def stop(self):
        """
        Stops the acquisition of the selected serial port.
        This function is connected to the clicked signal of the Stop button.
        :return:
        """
        Log.i(TAG, "Clicked stop")
        self._timer_plot.stop()
        self._enable_ui(True)
        self.worker.stop()

    def closeEvent(self, evnt):
        """
        Overrides the QTCloseEvent.
        This function is connected to the clicked signal of the close button of the window.
        :param evnt: QT evnt.
        :return:
        """
        if self.worker.is_running():
            Log.i(TAG, "Window closed without stopping capture, stopping it")
            self.stop()

    def _enable_ui(self, enabled):

        self.ui.pButton_Start.setEnabled(enabled)
        self.ui.pButton_Stop.setEnabled(not enabled)
        self.ui.chBox_export.setEnabled(enabled)



    def _configure_plot(self):
        """
        Configures specific elements of the PyQtGraph plots.
        :return:
        """
        self.ui.plt.setBackground(background=None)
        self.ui.plt.setAntialiasing(True)
        self._plt1 = self.ui.plt.addPlot(row=1, col=1)
        self._plt1.setLabel('bottom', Constants.plot_xlabel_title, Constants.plot_xlabel_unit)
        self._plt1.setLabel('left', "Temperature")
        self._plt1.setYRange(20, 30, padding=0)
        self._plt2 = self.ui.plt.addPlot(row=1, col=2)
        self._plt2.setLabel('bottom', Constants.plot_xlabel_title, Constants.plot_xlabel_unit)
        self._plt2.setLabel('left', "Pressure")
        self._plt2.setYRange(1020, 1030, padding=0)
        self._plt3 = self.ui.plt.addPlot(row=2, col=1)
        self._plt3.setLabel('bottom', Constants.plot_xlabel_title, Constants.plot_xlabel_unit)
        self._plt3.setLabel('left', "Altitude")
        self._plt3.setYRange(-100, 100, padding=0)
        self._plt4 = self.ui.plt.addPlot(row=2, col=2)
        self._plt4.setLabel('bottom', Constants.plot_xlabel_title, Constants.plot_xlabel_unit)
        self._plt4.setLabel('left', "Humidity")
        self._plt4.setYRange(20, 90, padding=0)

    def _configure_timers(self):
        """
        Configures specific elements of the QTimers.
        :return:
        """
        self._timer_plot = QtCore.QTimer(self)
        self._timer_plot.timeout.connect(self._update_plot)

    def _configure_signals(self):
        """
        Configures the connections between signals and UI elements.
        :return:
        """
        self.ui.pButton_Start.clicked.connect(self.start)
        self.ui.pButton_Stop.clicked.connect(self.stop)
        self.ui.sBox_Samples.valueChanged.connect(self._update_sample_size)


    def _update_sample_size(self):
        """
        Updates the sample size of the plot.
        This function is connected to the valueChanged signal of the sample Spin Box.
        :return:
        """
        if self.worker is not None:
            Log.i(TAG, "Changing sample size")
            self.worker.reset_buffers(self.ui.sBox_Samples.value())

    def _update_plot(self):
        """
        Updates and redraws the graphics in the plot.
        This function us connected to the timeout signal of a QTimer.
        :return:
        """
        self.worker.consume_queue()

        # plot data
        self._plt1.clear()
        self._plt1.plot(x=self.worker.get_time_buffer(),
                        y=self.worker.get_values_buffer(0),
                        pen=Constants.plot_colors[0])


        self._plt1.plot(x=self.worker.get_time_buffer(),
                        y=self.worker.get_values_buffer(4),
                        pen=Constants.plot_colors[4])


        self._plt2.clear()
        self._plt2.plot(x=self.worker.get_time_buffer(),
                        y=self.worker.get_values_buffer(1),
                        pen=Constants.plot_colors[1])


        self._plt3.clear()
        self._plt3.plot(x=self.worker.get_time_buffer(),
                        y=self.worker.get_values_buffer(2),
                        pen=Constants.plot_colors[2])

        self._plt4.clear()
        self._plt4.plot(x=self.worker.get_time_buffer(),
                        y=self.worker.get_values_buffer(3),
                        pen=Constants.plot_colors[3])


