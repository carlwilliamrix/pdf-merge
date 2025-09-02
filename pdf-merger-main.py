import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton,
    QFileDialog, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt
from PyPDF2 import PdfMerger


class PDFListWidget(QListWidget):
    def __init__(self, log_callback):
        super().__init__()
        self.setAcceptDrops(True)
        self.log = log_callback

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            # only accept if at least one URL is a PDF
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(".pdf"):
                    self.addItem(file_path)
                    self.log(f"URL {url.toLocalFile()}")
                    return
        self.log("File ignored, not a PDF?")
        event.ignore()

class PDFMergerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger (Drag & Drop)")
        self.resize(600, 450)

        layout = QVBoxLayout()

        # console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText("Console output will appear here...")

        # list for files (below console so you see logs immediately)
        self.listWidget = PDFListWidget(self.log)
        self.listWidget.setStyleSheet("""
                    QListWidget {
                        background-color: #808080;
                        border: 1px solid #ccc;
                        font-size: 14px;
                    }
                    QListWidget::item {
                        padding: 4px;
                    }
                    QListWidget::item:selected {
                        background-color: #0078d7;
                        color: white;
                    }
                """)
        layout.addWidget(self.listWidget)

        # Add merge button
        self.mergeBtn = QPushButton("Merge PDFs")
        self.mergeBtn.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.mergeBtn)
        layout.addWidget(self.console)

        self.setLayout(layout)

    # For debugging
    def log(self, message: str):
        print(message)
        self.console.append(message)

    def merge_pdfs(self):
        if self.listWidget.count() < 2:
            msg = "Please add at least 2 PDF files."
            QMessageBox.warning(self, "Error", msg)
            self.log(f"[ERROR] {msg}")
            return

        out_path, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "", "PDF Files (*.pdf)"
        )
        if not out_path:
            self.log("[INFO] Merge cancelled by user.")
            return

        merger = PdfMerger()
        try:
            for i in range(self.listWidget.count()):
                path = self.listWidget.item(i).text()
                self.log(f"[INFO] Adding {path}")
                merger.append(path)

            merger.write(out_path)
            merger.close()

            msg = f"Merged PDF saved: {out_path}"
            QMessageBox.information(self, "Success", msg)
            self.log(f"[SUCCESS] {msg}")

        except Exception as e:
            msg = f"Failed to merge PDFs: {str(e)}"
            QMessageBox.critical(self, "Error", msg)
            self.log(f"[ERROR] {msg}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFMergerUI()
    window.show()
    sys.exit(app.exec())
