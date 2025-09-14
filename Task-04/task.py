import sys, csv, mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QGridLayout,
    QTextEdit, QLineEdit, QFileDialog
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineScope – Dashboard")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("background-color: #121212; color: white; padding: 20px;")

        # Connect to MySQL
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="varshith12345", database="cinescope"
        )
        self.cursor = self.conn.cursor()

        self.search_mode = "title"  # Default search
        self.last_result = []
        self.selected_columns = ["title", "year", "genre", "rating", "director", "stars"]

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        header = QLabel("🎬 CineScope Dashboard")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        split_layout = QHBoxLayout()
        left_container = QVBoxLayout()

        # Search By buttons
        search_heading = QLabel("Search By")
        search_heading.setFont(QFont("Arial", 18, QFont.Bold))
        left_container.addWidget(search_heading)

        search_buttons = [("Title", "title"), ("Genre", "genre"), ("Year", "year"), ("Director", "director")]
        search_grid = QGridLayout()
        for index, (label, mode) in enumerate(search_buttons):
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, m=mode: self.set_search_mode(m))
            search_grid.addWidget(btn, index // 2, index % 2)
        left_container.addLayout(search_grid)

        # Search box + buttons
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter search term")
        left_container.addWidget(self.query_input)

        btn_layout = QHBoxLayout()
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.execute_search)
        btn_layout.addWidget(search_btn)

        export_btn = QPushButton("Export CSV")
        export_btn.clicked.connect(self.export_csv)
        btn_layout.addWidget(export_btn)
        left_container.addLayout(btn_layout)

        # Right side (Table + Console)
        self.table = QTableWidget()
        self.output_console = QTextEdit()
        self.output_console.setFixedHeight(100)

        right_side_layout = QVBoxLayout()
        right_side_layout.addWidget(self.table)
        right_side_layout.addWidget(self.output_console)

        split_layout.addLayout(left_container, 2)
        split_layout.addLayout(right_side_layout, 8)
        main_layout.addLayout(split_layout)
        self.setLayout(main_layout)

    def set_search_mode(self, mode):
        self.search_mode = mode
        self.output_console.append(f"Search mode set to: {mode}")

    def execute_search(self):
        term = self.query_input.text()
        cols = ", ".join(self.selected_columns)
        query = f"SELECT {cols} FROM movies WHERE {self.search_mode} LIKE %s"
        self.cursor.execute(query, (f"%{term}%",))
        self.last_result = self.cursor.fetchall()

        self.table.setRowCount(len(self.last_result))
        self.table.setColumnCount(len(self.selected_columns))
        self.table.setHorizontalHeaderLabels([c.title() for c in self.selected_columns])

        for r, row in enumerate(self.last_result):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

        if len(self.last_result) == 0:
            self.output_console.append("⚠ No results found.")
        else:
            self.output_console.append(f"✅ Found {len(self.last_result)} results.")

    def export_csv(self):
        if not self.last_result:
            self.output_console.append("⚠ No data to export.")
            return
        fname, _ = QFileDialog.getSaveFileName(self, "Save CSV", "export.csv", "CSV Files (*.csv)")
        if fname:
            with open(fname, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.selected_columns)
                writer.writerows(self.last_result)
            self.output_console.append(f"✅ Exported {len(self.last_result)} rows to {fname}")

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dash = Dashboard()
    dash.show()
    sys.exit(app.exec())
