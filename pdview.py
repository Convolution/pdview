import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, \
                            QTableWidget, QTableWidgetItem, QHeaderView, \
                            QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt


class pdvWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.row_height = 25
        self.col_width = 100
        self.max_rows = 500
        self.max_cols = 100 
        self.fmt_default = "{0}"
        self.fmt_int = "{:.0f}"
        self.fmt_float = "{:.5f}"
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
    
        with open('styleSheet.css', 'r') as f:
            styleSheet = f.read()

        self.setStyleSheet(styleSheet)
        self.tbview.setStyleSheet(styleSheet)
        self.tbview.setAlternatingRowColors(True)
        self.tbview.horizontalHeader().setAlternatingRowColors(True)
        self.tbview.horizontalHeader().setHighlightSections(True)
        self.tbview.verticalHeader().setHighlightSections(True)

    def set_int_fmt(fmt):
        fmt.format(123)  # Throws if this can't format an int
        self.fmt_int = fmt

    def set_float_fmt():
        fmt.format(np.pi)  # Throw if this can't format a float
        self.fmt_float = fmt

    def set_max_rows(self, nrows):
        self.max_rows = nrows

    def set_max_cols(self, ncols):
        self.max_cols = ncols

    def set_row_height(self, row_height):
        self.row_height = row_height

    def set_col_width(self, col_width):
        self.col_width = col_width

    def load_df(self, df):
        nrows = df.shape[0] if df.shape[0] < self.max_rows else self.max_rows
        ncols = df.shape[1] if df.shape[1] < self.max_cols else self.max_cols
        self.tbview.setRowCount(nrows)
        self.tbview.setColumnCount(ncols)
        self.tbview.setHorizontalHeaderLabels(df.columns[:nrows].astype('str'))
        self.tbview.setVerticalHeaderLabels(df.index[:ncols].astype('str'))

        for icol in range(ncols):
            self.tbview.setColumnWidth(icol, self.col_width)
        for irow in range(nrows):
            self.tbview.setRowHeight(irow, self.row_height)



        for irow in range(nrows):
            for icol in range(ncols):
                val = df.iloc[irow, icol]

                fmt_str = self.fmt_default

                if hasattr(val, 'dtype'):
                    if val.dtype in [np.int]:
                        fmt_str = self.fmt_int
                    elif val.dtype in [np.float]:
                        fmt_str = self.fmt_float

                self.tbview.setItem(irow, icol,
                                    QTableWidgetItem(fmt_str.format(val)))


class PDView():
    def __init__(self, df):
        self.app = QApplication([])
        self.ui = pdvWindow()
        self.ui.load_df(df)

    def set_int_fmt(self, fmt):
        self.ui.set_int_fmt(fmt)

    def set_float_fmt(self, float):
        self.ui.set_float_fmt(fmt)

    def set_max_rows(self, nrows):
        self.ui.set_max_rows(nrows)

    def set_max_cols(self, ncols):
        self.ui.set_max_cols(ncols)

    def set_row_height(self, row_height):
        self.ui.set_row_height(row_height)

    def set_col_width(self, col_width):
        self.ui.set_col_width(col_width)

    def show(self):
        self.ui.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    m = 100
    n = 100
    df = pd.DataFrame(
        np.random.rand(m, n),
        index=np.arange(0, m),
        columns=['col_' + str(x) for x in range(n)]
        )
    p = PDView(df)
    p.show()
