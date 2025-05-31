import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt, QDateTime, QRunnable, QThreadPool, QTimer, QTime
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem, QFont, QColor
from PyQt5.QtWidgets import QMessageBox, QDialog, QLabel, QDesktopWidget, QFileDialog
import os
import time
import requests
import speedtest
import pandas as pd
import traceback

class FramelessWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Construct the path to the .ui file dynamically
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(script_dir, "RegFBUI.ui")
        
        # Load the UI file
        try:
            uic.loadUi(ui_file, self)
        except Exception as e:
            print(f"Error loading UI file: {e}")
            sys.exit(1)
        
        # Initialize the timer for counting elapsed time
        self.start_time = QDateTime.currentDateTime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_elapsed_time)
        self.timer.start(1000)  # Update every second
        # Customize the label appearance
        self.txtLabelPeriodOpen.setStyleSheet("color: white; font-size: 11pt; font-weight: bold;")

        # Set the window flags to remove the title bar and borders
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Calculate center position
        self.center()
        
        # Connect buttons to their slots
        try:
            self.btnClose.clicked.connect(self.on_close)
            self.btnMinimize.clicked.connect(self.on_minimize)
            self.btnInfo.clicked.connect(self.on_info)
            self.btnCheckIP.clicked.connect(self.on_check_ip)
            self.btnCheckSpeed.clicked.connect(self.on_check_speed)
            self.btnStartReg.clicked.connect(self.on_start_reg)
            self.btnSaveReg.clicked.connect(self.on_save_reg)
            self.btnClearReg.clicked.connect(self.on_clear_fields)

        except Exception as e:
            print(f"Error connecting buttons: {e}")
            sys.exit(1)
            
        # Initialize the table
        self.setup_table()


    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.drag_pos
        self.move(self.pos() + delta)
        self.drag_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        pass
    
    def center(self):
        # Get the desktop resolution
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_close(self):
        try:
            reply = QMessageBox.question(self, 'Exit Confirmation',
                                         'Are you sure you want to exit?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.close()
        except Exception as e:
            print(f"Error on close button click: {e}")

    def on_minimize(self):
        try:
            self.showMinimized()
        except Exception as e:
            print(f"Error on minimize button click: {e}")

    def on_info(self):
        try:
            info_text = """
            <html>
                <body style='font-size: 9pt; color: white; background-color: gray;'>
                    <h1>Owner Info</h1>
                    <hr>
                    <p>Name: Gmail Registration Form</p>
                    <p>Create By: Phekdey PHORN | ផន ភក្ដី</p>
                    <p>Contact: 089 755 770</p>
                    <p>Code: Python</p>
                    <p>Create Date: 13-Aug-2024</p>
                    <p>Update Date: 14-Aug-2024</p>
                    <p>Price: Free</p>
                    <p>Version: 1.0</p>
                    <br>
                    <h1>User Info</h1>
                    <hr>
                    <p>Machine ID: {current}</p>
                    <p>License Key: {current}</p>
                    <p>Create Key: {current}</p>
                    <p>Expiry Key: {current}</p>
                </body>
            </html>
            """
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Info")
            msg_box.setText(info_text)
            msg_box.setStyleSheet("QLabel{min-width: 500px;}")
            return_button = msg_box.addButton("Back Home", QMessageBox.AcceptRole)
            return_button.setStyleSheet("color: white;")
            return_button.setCursor(Qt.PointingHandCursor)
            msg_box.exec_()
            return_button.clicked.connect(msg_box.close)
        except Exception as e:
            print(f"Error on info button click: {e}")


    def on_check_ip(self):
        try:
            # Confirmation message
            reply = QMessageBox.question(self, 'Confirm IP Check',
                                        'Do you want to check your IP information?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                response = requests.get("https://ipinfo.io")
                data = response.json()
                # Extract and format IP information
                ip_address = data.get('ip', 'N/A')
                city = data.get('city', 'N/A')
                region = data.get('region', 'N/A')
                country = data.get('country', 'N/A')
                location = data.get('loc', 'N/A')
                organization = data.get('org', 'N/A')
                timezone = data.get('timezone', 'N/A')
                # Format the display text
                ip_info_text = (
                    f"IP Address: {ip_address}\n"
                    f"City: {city}\n"
                    f"Region: {region}\n"
                    f"Country: {country}\n"
                    f"Location (Lat, Long): {location}\n"
                    f"Organization: {organization}\n"
                    f"Timezone: {timezone}"
                )
                self.txtIpAddress.setText(ip_info_text)
        except Exception as e:
            self.txtIpAddress.setText("Error fetching IP info. Try again!")


    def on_check_speed(self):
        try:
            # Confirmation message
            reply = QMessageBox.question(self, 'Confirm Speed Test',
                                        'Do you want to check your internet speed?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                st = speedtest.Speedtest()
                st.get_best_server()
                download_speed = st.download() / 1_000_000  # Convert to Mbps
                upload_speed = st.upload() / 1_000_000      # Convert to Mbps
                ping = st.results.ping
                # Format the display text
                speed_info_text = (
                    f"Download Speed: {download_speed:.2f} Mbps\n"
                    f"Upload Speed: {upload_speed:.2f} Mbps\n"
                    f"Ping: {ping} ms"
                )
                self.txtSpeedInternet.setText(speed_info_text)
        except Exception as e:
            self.txtSpeedInternet.setText("Error performing speed test.")
    
    
    def update_elapsed_time(self):
        # Calculate the time difference from the start time
        current_time = QDateTime.currentDateTime()
        elapsed = self.start_time.secsTo(current_time)
        # Calculate days, hours, minutes, and seconds
        days = elapsed // 86400  # 86400 seconds in a day
        hours = (elapsed % 86400) // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        # Format the elapsed time as dd:hh:mm:ss
        elapsed_text = f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"
        # Update the label text
        self.txtLabelPeriodOpen.setText(elapsed_text)
        
        
    def setup_table(self):
        # Create a model with 13 columns
        self.model = QStandardItemModel(0, 13)  # Start with 0 rows and 13 columns
        self.model.setHorizontalHeaderLabels([
            "No", "First Name", "Last Name", "Username", "Uid", "Age", 
            "Dob", "Gender", "Phone", "Mail", "Password", "Status", "Create Date"
        ])
        
        # Set the model on the table view
        self.tableRegFB.setModel(self.model)
        # Create a font object with the desired style
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        # Apply the font to all headers
        for col in range(self.model.columnCount()):
            item = self.model.horizontalHeaderItem(col)
            if item:  # Ensure item exists
                item.setFont(font)
                item.setForeground(QColor('black'))  # Set text color to black
        self.tableRegFB.resizeColumnsToContents()

    def on_start_reg(self):
        # Sample data
        data = [
            [1, "John", "Doe", "johndoe", "1001", 25, "1999-07-15", "Male", "1234567890", "john@example.com", "password123", "Active", "2024-08-23"],
            [2, "Jane", "Smith", "janesmith", "1002", 30, "1994-05-21", "Female", "0987654321", "jane@example.com", "password456", "Pending", "2024-08-23"],
            [3, "Alice", "Johnson", "alicej", "1003", 28, "1996-12-10", "Female", "1122334455", "alice@example.com", "password789", "Active", "2024-08-23"],
        ]
        # Create a font object with the desired style
        font = QFont()
        font.setBold(False)
        font.setPointSize(10)
        # Populate the model with data
        for row_data in data:
            items = []
            for col_data in row_data:
                item = QStandardItem(str(col_data))
                item.setFont(font)
                item.setForeground(QColor('white'))  # Set text color to black
                items.append(item)
            self.model.appendRow(items)
        # Resize columns to fit the content
        self.tableRegFB.resizeColumnsToContents()


    def on_save_reg(self):
        try:
            # Check if the table has data
            if self.model.rowCount() == 0:
                QMessageBox.warning(self, 'No Data', 'The table is empty. There is nothing to save.')
                return
            # Confirm export type with custom buttons
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Export Data')
            msg_box.setText('Which file format do you want to export the data to?')
            button_excel = msg_box.addButton('Excel', QMessageBox.YesRole)
            button_text = msg_box.addButton('Text', QMessageBox.NoRole)
            button_cancel = msg_box.addButton(QMessageBox.Cancel)
            msg_box.exec_()
            # Determine which button was clicked
            if msg_box.clickedButton() == button_excel:
                file_format = 'Excel'
            elif msg_box.clickedButton() == button_text:
                file_format = 'Text'
            else:
                return  # User canceled the action
            # Ask for a file location to save
            if file_format == 'Excel':
                file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx);;All Files (*)")
            else:
                file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
            if not file_name:
                return  # User canceled the save dialog
            # Extract data from the table
            row_count = self.model.rowCount()
            col_count = self.model.columnCount()
            # Prepare data to save
            data = []
            for row in range(row_count):
                row_data = []
                for col in range(col_count):
                    item = self.model.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            # Save to the selected format
            if file_format == 'Excel':
                try:
                    df = pd.DataFrame(data, columns=[self.model.horizontalHeaderItem(i).text() for i in range(col_count)])
                    df.to_excel(file_name, index=False)
                except Exception as e:
                    QMessageBox.critical(self, 'Export Error', f'Failed to export to Excel.\nError: {str(e)}')
                    print(traceback.format_exc())
                    return
            else:  # Text format
                try:
                    with open(file_name, 'w') as f:
                        headers = [self.model.horizontalHeaderItem(i).text() for i in range(col_count)]
                        f.write('\t'.join(headers) + '\n')
                        for row_data in data:
                            f.write('\t'.join(row_data) + '\n')
                except Exception as e:
                    QMessageBox.critical(self, 'Export Error', f'Failed to export to Text file.\nError: {str(e)}')
                    print(traceback.format_exc())
                    return
            QMessageBox.information(self, 'Export Successful', f'Data exported successfully to {file_name}')
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', f'An unexpected error occurred.\nError: {str(e)}')
            print(traceback.format_exc())


    def clear_all_fields(self):
        # Clear QTextEdit fields
        for widget in self.findChildren(QtWidgets.QTextEdit):
            widget.clear()
        # Uncheck QCheckBox fields
        for widget in self.findChildren(QtWidgets.QCheckBox):
            widget.setChecked(False)
        # Set QComboBox to first index
        for widget in self.findChildren(QtWidgets.QComboBox):
            widget.setCurrentIndex(0)
        # Clear QTableView data
        self.model.removeRows(0, self.model.rowCount())

    def clear_table_data(self):
        # Clear QTableView data
        self.model.removeRows(0, self.model.rowCount())
        
    def on_clear_fields(self):
        try:
            # Confirmation message
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Confirm Clear')
            msg_box.setText('What do you want to clear?')
            # Add buttons for different actions
            button_clear_all = msg_box.addButton('Clear All', QMessageBox.YesRole)
            button_clear_table_only = msg_box.addButton('Clear Table Only', QMessageBox.NoRole)
            button_cancel = msg_box.addButton(QMessageBox.Cancel)
            msg_box.exec_()
            # Determine which button was clicked
            if msg_box.clickedButton() == button_clear_all:
                self.clear_all_fields()
                QMessageBox.information(self, 'Clear Fields', 'All fields and table data have been cleared successfully.')
            elif msg_box.clickedButton() == button_clear_table_only:
                self.clear_table_data()
                QMessageBox.information(self, 'Clear Fields', 'Table data has been cleared successfully.')
            else:
                QMessageBox.information(self, 'Clear Fields', 'Action canceled. No fields were cleared.')
        except Exception as e:
            QMessageBox.critical(self, 'Clear Fields Error', f'Failed to clear fields.\nError: {str(e)}')
            print(traceback.format_exc())





app = QtWidgets.QApplication(sys.argv)

# Create the frameless window
window = FramelessWindow()
window.show()
app.exec()



