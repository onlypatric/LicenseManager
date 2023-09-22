import sys
from PyQt6.QtWidgets import QApplication, QComboBox, QGroupBox, QTableWidgetItem, QTableWidget, QLineEdit, QHBoxLayout, QTextEdit, QLabel, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QPushButton
from admin_license_wrapper import AdminLicenseAPI  # Import your AdminLicenseAPI class

class LicenseManagerApp(QMainWindow):
    def __init__(self, admin_api: AdminLicenseAPI):
        super().__init__()
        self.admin_api = admin_api
        self.initUI()

    def initUI(self):
        self.setWindowTitle("License Manager")
        self.setGeometry(100, 100, 800, 600)

        # Create a tab widget with three tabs
        tab_widget = QTabWidget()
        tab_widget.addTab(self.createOverviewTab(), "Overview")

        # Add your second and third tabs here

        self.setCentralWidget(tab_widget)

    def createOverviewTab(self):
        # Create the Overview tab
        overview_tab = QWidget()
        layout = QVBoxLayout()

        # Create a table widget to display license information
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["UUID", "Devices", "Expiry Date","btn","extra"])
        self.refresh()
        layout.addWidget(self.table_widget)
        btn = QPushButton("Refresh")
        btn.clicked.connect(self.refresh)
        btn2 = QPushButton("Add license")
        btn2.clicked.connect(lambda _: (self.admin_api.create_license(),self.refresh()))
        layout.addWidget(btn)
        layout.addWidget(btn2)
        overview_tab.setLayout(layout)

        return overview_tab
    def refresh(self):
        self.table_widget.clear()
        licenses = self.admin_api.get_all_licenses()
        self.table_widget.setRowCount(0)
        # Populate the table with license data
        for row, license in enumerate(licenses["licenses"]):
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(license["uuid"]))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(len(license["devices"]))))
            self.table_widget.setItem(row, 2, QTableWidgetItem(license["expiryDate"]))

            # Add a button to view license details
            details_button = QPushButton("Details")
            details_button.clicked.connect(lambda _, uuid=license["uuid"]: self.showLicenseDetails(uuid))
            self.table_widget.setCellWidget(row, 3, details_button)

    def showLicenseDetails(self, uuid):
        # Fetch license details for the selected license
        license_details = self.admin_api.get_license_info(uuid)["license"]
        print(license_details)
        # Create a dialog to display license details (devices, banned devices)
        dialog = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Codice di attivazione licenza:"))
        license_text = QLabel(license_details["uuid"])
        layout.addWidget(license_text)
        layout.addWidget(QLabel(""))
        self.license_until = QLineEdit(license_details["until"] if license_details["until"] is not None else "")
        
        layout.addWidget(QLabel("Data di scadenza per licenza:"))
        self.license_until.setPlaceholderText("gg/mm/aaaa oppure lifetime")
        layout.addWidget(self.license_until)
        self.updateUntil = QPushButton("Aggiorna")
        self.updateUntil.clicked.connect(lambda _, uuid=license_details["uuid"], date=self.license_until.text: (self.admin_api.set_expiry_date(uuid, date()),self.refresh()))
        layout.addWidget(self.updateUntil)

        layout.addWidget(QLabel("Controlli: "))
        self.deleteButton = QPushButton("Elimina")
        self.deleteButton.clicked.connect(lambda _, uuid=license_details["uuid"]: (self.admin_api.delete_license(uuid),dialog.close(),self.refresh()))
        layout.addWidget(self.deleteButton)

        layout.addWidget(QLabel("Dispositivi registrati:"))
        self.combobox = QComboBox()
        self.combobox.addItems(license_details["devices"])
        layout.addWidget(self.combobox)
        self.banDevice = QPushButton("Revoca accesso")
        self.banDevice.clicked.connect(lambda _, uuid=license_details["uuid"], device=self.combobox.currentText: self.admin_api.ban_device(uuid, device()))
        layout.addWidget(self.banDevice)

        dialog.setLayout(layout)
        dialog.setWindowTitle(f"License Details - {uuid}")
        dialog.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    admin_api = AdminLicenseAPI("http://localhost:8000")  # Replace with your API base URL
    window = LicenseManagerApp(admin_api)
    window.show()
    sys.exit(app.exec())
