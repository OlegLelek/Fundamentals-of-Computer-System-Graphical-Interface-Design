import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QPushButton, QComboBox,
    QFileDialog, QMessageBox, QLabel
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №3 — SQLite")
        self.resize(900, 600)

        self.db = None
        self.current_table = ""

        self.create_menu()
        self.create_interface()

    def create_menu(self):
        menu = self.menuBar().addMenu("Database")

        set_connection = menu.addAction("Set connection")
        set_connection.triggered.connect(self.set_connection)

        close_connection = menu.addAction("Close connection")
        close_connection.triggered.connect(self.close_connection)

    def create_interface(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        self.status_label = QLabel("Соединение с базой данных не установлено")
        self.status_label.setStyleSheet("color: #555; padding: 4px;")
        main_layout.addWidget(self.status_label)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Tab1 — результат SELECT * FROM sqlite_master
        self.tab1 = QTableWidget()
        self.tabs.addTab(self.tab1, "Tab1 — sqlite_master")

        # Tab2 — выборочный запрос имён объектов БД
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout(tab2_widget)
        self.btn1 = QPushButton("SELECT name FROM sqlite_master")
        self.btn1.clicked.connect(self.select_names)
        tab2_layout.addWidget(self.btn1)
        self.tab2 = QTableWidget()
        tab2_layout.addWidget(self.tab2)
        self.tabs.addTab(tab2_widget, "Tab2 — имена объектов")

        # Tab3 — выбор таблицы и её колонки
        tab3_widget = QWidget()
        tab3_layout = QVBoxLayout(tab3_widget)
        controls = QHBoxLayout()

        controls.addWidget(QLabel("Таблица:"))
        self.table_combo = QComboBox()
        self.table_combo.currentTextChanged.connect(self.on_table_changed)
        controls.addWidget(self.table_combo)

        controls.addWidget(QLabel("Колонка:"))
        self.column_combo = QComboBox()
        self.column_combo.currentTextChanged.connect(self.select_column)
        controls.addWidget(self.column_combo)

        tab3_layout.addLayout(controls)
        self.tab3 = QTableWidget()
        tab3_layout.addWidget(self.tab3)
        self.tabs.addTab(tab3_widget, "Tab3 — выбранная колонка")

        # Tab4 — структура выбранной таблицы
        tab4_widget = QWidget()
        tab4_layout = QVBoxLayout(tab4_widget)
        self.btn2 = QPushButton("Показать структуру выбранной таблицы")
        self.btn2.clicked.connect(self.show_table_structure)
        tab4_layout.addWidget(self.btn2)
        self.tab4 = QTableWidget()
        tab4_layout.addWidget(self.tab4)
        self.tabs.addTab(tab4_widget, "Tab4 — структура")

        # Tab5 — первые записи выбранной таблицы
        tab5_widget = QWidget()
        tab5_layout = QVBoxLayout(tab5_widget)
        self.btn3 = QPushButton("Показать первые записи выбранной таблицы")
        self.btn3.clicked.connect(self.show_table_data)
        tab5_layout.addWidget(self.btn3)
        self.tab5 = QTableWidget()
        tab5_layout.addWidget(self.tab5)
        self.tabs.addTab(tab5_widget, "Tab5 — данные")

    def set_connection(self):
        """Выбор SQLite-файла и установка соединения с базой данных."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите базу данных SQLite",
            "",
            "SQLite database (*.db *.sqlite *.sqlite3);;All files (*)"
        )
        if not filename:
            return

        self.close_connection(silent=True)

        self.db = QSqlDatabase.addDatabase("QSQLITE", "lab3_connection")
        self.db.setDatabaseName(filename)

        if not self.db.open():
            QMessageBox.critical(
                self,
                "Ошибка подключения",
                self.db.lastError().text()
            )
            self.db = None
            return

        self.status_label.setText(f"Подключено: {filename}")
        self.load_master_table()
        self.load_tables()

    def close_connection(self, silent=False):
        """Закрыть подключение и очистить таблицы и списки программы."""
        if self.db is not None:
            connection_name = self.db.connectionName()
            self.db.close()
            self.db = None
            QSqlDatabase.removeDatabase(connection_name)

        self.current_table = ""
        self.table_combo.clear()
        self.column_combo.clear()

        for table in (self.tab1, self.tab2, self.tab3, self.tab4, self.tab5):
            table.clear()
            table.setRowCount(0)
            table.setColumnCount(0)

        self.status_label.setText("Соединение с базой данных не установлено")
        if not silent:
            QMessageBox.information(self, "SQLite", "Соединение закрыто")

    def run_query(self, sql):
        """Выполнить SQL-запрос и вернуть заголовки и строки результата."""
        if self.db is None or not self.db.isOpen():
            QMessageBox.warning(self, "Нет подключения", "Сначала выберите базу данных")
            return [], []

        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            QMessageBox.critical(self, "Ошибка SQL", query.lastError().text())
            return [], []

        headers = [query.record().fieldName(i) for i in range(query.record().count())]
        rows = []
        while query.next():
            rows.append([query.value(i) for i in range(len(headers))])
        return headers, rows

    def fill_table(self, widget, headers, rows):
        """Вывести результат SQL-запроса в QTableWidget."""
        widget.clear()
        widget.setColumnCount(len(headers))
        widget.setRowCount(len(rows))
        widget.setHorizontalHeaderLabels(headers)

        for row_index, row in enumerate(rows):
            for column_index, value in enumerate(row):
                widget.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem("" if value is None else str(value))
                )

        widget.resizeColumnsToContents()

    def load_master_table(self):
        """Tab1: вывести системную таблицу sqlite_master."""
        headers, rows = self.run_query("SELECT * FROM sqlite_master")
        self.fill_table(self.tab1, headers, rows)

    def select_names(self):
        """Tab2: вывести имена таблиц и представлений базы данных."""
        headers, rows = self.run_query(
            "SELECT name FROM sqlite_master WHERE type IN ('table', 'view')"
        )
        self.fill_table(self.tab2, headers, rows)

    def load_tables(self):
        """Загрузить пользовательские таблицы базы в список 'Таблица'."""
        headers, rows = self.run_query(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )

        self.table_combo.blockSignals(True)
        self.table_combo.clear()
        for row in rows:
            self.table_combo.addItem(str(row[0]))
        self.table_combo.blockSignals(False)

        if rows:
            self.table_combo.setCurrentIndex(0)
            self.on_table_changed(self.table_combo.currentText())

    def on_table_changed(self, table_name):
        """Слот: пользователь выбрал таблицу — загрузить её колонки."""
        if not table_name:
            return
        self.current_table = table_name
        self.load_columns(table_name)

    def load_columns(self, table_name):
        """Загрузить названия колонок выбранной таблицы в список 'Колонка'."""
        if not table_name or self.db is None:
            return

        safe_table = table_name.replace('"', '""')
        headers, rows = self.run_query(f'PRAGMA table_info("{safe_table}")')

        self.column_combo.blockSignals(True)
        self.column_combo.clear()
        for row in rows:
            self.column_combo.addItem(str(row[1]))
        self.column_combo.blockSignals(False)

        if rows:
            self.select_column(self.column_combo.currentText())

    def select_column(self, column_name):
        """Tab3: вывести данные выбранной колонки выбранной таблицы."""
        if not self.current_table or not column_name:
            return

        safe_table = self.current_table.replace('"', '""')
        safe_column = column_name.replace('"', '""')
        headers, rows = self.run_query(
            f'SELECT "{safe_column}" FROM "{safe_table}"'
        )
        self.fill_table(self.tab3, headers, rows)

    def show_table_structure(self):
        """Tab4: показать структуру выбранной таблицы через PRAGMA table_info."""
        if not self.current_table:
            QMessageBox.warning(self, "Таблица не выбрана", "Сначала выберите таблицу")
            return

        safe_table = self.current_table.replace('"', '""')
        headers, rows = self.run_query(f'PRAGMA table_info("{safe_table}")')
        self.fill_table(self.tab4, headers, rows)

    def show_table_data(self):
        """Tab5: показать первые 100 записей выбранной таблицы."""
        if not self.current_table:
            QMessageBox.warning(self, "Таблица не выбрана", "Сначала выберите таблицу")
            return

        safe_table = self.current_table.replace('"', '""')
        headers, rows = self.run_query(f'SELECT * FROM "{safe_table}" LIMIT 100')
        self.fill_table(self.tab5, headers, rows)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
