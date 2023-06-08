from PyQt5.QtWidgets import QDialog, QLineEdit, QDialogButtonBox, QFormLayout

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.user = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Username", self.user)
        layout.addRow("Password", self.password)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.user.text(), self.password.text())