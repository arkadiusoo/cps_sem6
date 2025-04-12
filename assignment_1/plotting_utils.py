from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setMinimumHeight(300)
        self.allow_dblclick = True
        self.mpl_connect("button_press_event", self.open_in_window)

    def signal_plot(self, continuous_data, sampled_data, signal_type="Ciągły", title="Wykres sygnału"):
        self.ax.clear()

        y_cont, t_cont = zip(*continuous_data) if continuous_data else ([], [])
        y_samp, t_samp = zip(*sampled_data) if sampled_data else ([], [])

        self.ax.plot(t_cont, y_cont, label="Funkcja oryginalna", color='blue')
        if signal_type == "Dyskretny":
            self.ax.plot(t_samp, y_samp, 'ro', label="Próbkowanie")

        self.ax.set_title(title)
        self.ax.set_xlabel("Czas [s]")
        self.ax.set_ylabel("Amplituda")
        self.ax.grid()
        self.fig.tight_layout()
        self.draw()

    def plot_histogram(self, values, bins=10, title="Histogram amplitudy"):
        self.ax.clear()
        self.ax.hist(values, bins=bins, color="darkorange", edgecolor="black")
        self.ax.set_title(title)
        self.ax.set_xlabel("Amplituda")
        self.ax.set_ylabel("Liczba wystąpień")
        self.ax.grid()
        self.fig.tight_layout()
        self.draw()

    def open_in_window(self, event):
        if event.dblclick and self.allow_dblclick:
            title = self.ax.get_title()
            window = PlotWindow(title, self.fig)
            window.show()
            self._external_window = window


class PlotWindow(QWidget):
    def __init__(self, title: str, fig, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(800, 600)

        layout = QVBoxLayout(self)
        new_fig = Figure(figsize=(10, 6))
        new_ax = new_fig.add_subplot(111)

        for ax in fig.axes:
            for line in ax.get_lines():
                new_ax.plot(
                    line.get_xdata(),
                    line.get_ydata(),
                    label=line.get_label(),
                    color=line.get_color(),
                    linestyle=line.get_linestyle(),
                    marker=line.get_marker()
                )

        new_ax.set_title(ax.get_title())
        new_ax.set_xlabel(ax.get_xlabel())
        new_ax.set_ylabel(ax.get_ylabel())
        new_ax.grid(True)

        canvas = FigureCanvas(new_fig)
        layout.addWidget(canvas)
