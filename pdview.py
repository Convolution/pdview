import sys
import os
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, \
                            QTableWidget, QTableWidgetItem, QHeaderView, \
                            QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt


class PDViewWindow(QWidget):
    def __init__(self, df):
        super().__init__()
        self.row_height = 25
        self.col_width = 100
        self.max_rows = 100
        self.max_cols = 100
        self.row_start = 0
        self.row_stop = 0
        self.fmt_default = "{0}"
        self.fmt_int = "{:.0f}"
        self.fmt_float = "{:.5f}"
        self.df = df
        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 640, 480)
        self.vbox = QVBoxLayout(self)
        self.tbview = QTableWidget(self)

        self.buttonBox = QHBoxLayout()
        self.nextButton = QPushButton(text="Next")
        self.prevButton = QPushButton(text="Previous")
        self.buttonBox.addWidget(self.prevButton)
        self.buttonBox.addWidget(self.nextButton)

        self.vbox.addWidget(self.tbview)
        self.vbox.addLayout(self.buttonBox)

        stylesheet_uri = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'stylesheet.css')

        with open(stylesheet_uri, 'r') as f:
            styleSheet = f.read()

        # Configure the table widget
        self.setStyleSheet(styleSheet)
        self.tbview.setStyleSheet(styleSheet)
        self.tbview.setAlternatingRowColors(True)
        self.tbview.horizontalHeader().setAlternatingRowColors(True)
        self.tbview.horizontalHeader().setHighlightSections(True)
        self.tbview.verticalHeader().setHighlightSections(True)

        self.tbview.setRowCount(self.max_rows)
        self.tbview.setColumnCount(self.max_cols)

        # Connect the buttons
        self.nextButton.clicked.connect(self.load_next)
        self.prevButton.clicked.connect(self.load_prev)

    def set_df(self, df):
        self.df = df

    def set_int_fmt(self, fmt):
        fmt.format(123)  # Throws if this can't format an int
        self.fmt_int = fmt

    def set_float_fmt(self, fmt):
        fmt.format(np.pi)  # Throw if this can't format a float
        self.fmt_float = fmt

    def set_max_rows(self, nrows):
        self.max_rows = nrows
        self.tbview.setRowCount(self.max_rows)

    def set_max_cols(self, ncols):
        self.max_cols = ncols
        self.tbview.setColumnCount(self.max_cols)

    def set_row_height(self, row_height):
        self.row_height = row_height

    def set_col_width(self, col_width):
        self.col_width = col_width

    def load_df(self):
        df = self.df
        if df is None:
            return

        if self.row_start >= df.shape[0]:  # End of df reached
            return

        self.row_stop = df.shape[0] \
                if df.shape[0] - self.row_start < self.max_rows \
                else self.row_start + self.max_rows

        self.col_stop = df.shape[1] \
                if df.shape[1] < self.max_cols else self.max_cols

        # Table headers and dimensions
        self.tbview.setRowCount(self.row_stop - self.row_start)
        self.tbview.setColumnCount(self.col_stop)
        self.tbview.setHorizontalHeaderLabels(df.columns[:self.col_stop].astype('str'))
        self.tbview.setVerticalHeaderLabels(df.index[self.row_start:self.row_stop].astype('str'))

        for icol in range(self.col_stop):
            self.tbview.setColumnWidth(icol, self.col_width)
        for irow in range(self.row_stop):
            self.tbview.setRowHeight(irow, self.row_height)

        # Copy df values to the cells
        for irow in range(self.max_rows):
            for icol in range(self.max_cols):
                self.tbview.setItem(irow, icol, QTableWidgetItem())


        for irow in range(self.row_start, self.row_stop):
            for icol in range(self.col_stop):
                val = df.iloc[irow, icol]

                fmt_str = self.fmt_default

                if hasattr(val, 'dtype'):
                    if val.dtype in [np.int]:
                        fmt_str = self.fmt_int
                    elif val.dtype in [np.float]:
                        fmt_str = self.fmt_float
                try:
                    self.tbview.item(irow - self.row_start, icol).setText(fmt_str.format(val))
                except:
                    from ipdb import set_trace
                    set_trace()

        self.tbview.update()

    def load_prev(self):
        if self.row_start > 0:
            self.row_start -= self.max_rows
        self.load_df()

    def load_next(self):
        if self.row_stop < self.df.shape[0]:
            self.row_start = self.row_stop
        self.load_df()


def pdview(df, max_rows=100, max_cols=100, row_height=25, col_width=100,
           float_fmt="{:.3f}", int_fmt="{:.0f}", default_fmt="{0}"):
    app = QApplication([])
    ui = PDViewWindow(df)

    ui.set_max_rows(max_rows)
    ui.set_max_cols(max_cols)
    ui.set_row_height(row_height)
    ui.set_col_width(col_width)
    ui.set_int_fmt(int_fmt)
    ui.set_float_fmt(float_fmt)
    ui.load_df()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    m = 1000
    n = 10
    df = pd.DataFrame(
        np.random.rand(m, n),
        index=np.arange(0, m),
        columns=['C' + str(x) for x in range(n)]
        )
    pdview(df)

