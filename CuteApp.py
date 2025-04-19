import sys
import requests 

from bs4 import BeautifulSoup
from PySide6.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
)
from PySide6.QtCore    import Qt, QThread, Signal
from PySide6.QtGui     import QPixmap
from duckduckgo_search import DDGS #type:ignore
import requests
import random


class ImageFetcher(QThread):
    """
    Worker thread that:
      1) Queries DuckDuckGo for a batch of fox image URLs
      2) Chooses one at random
      3) Downloads the image bytes
    Emits pixmap_ready when done.
    """
    pixmap_ready = Signal(QPixmap)




   






    

    def run(self):
        try:
            # 1) Get a batch of fox image URLs
            with DDGS() as ddgs:
                results = ddgs.images(keywords="wild fox, fox, fox pups, cute fox, fox wildlife", max_results=50) 
              
                if not results:
                    raise ValueError("No images found")
                # 2) Choose one at random
            
                chosen = random.choice(results)
               
                url = chosen.get("image")
                if not url:
                    raise ValueError("No image URL in result")
            # 3) Download the image
            headers = {'User-Agent': 'Mozilla/5.0 (fox-viewer)'}
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            pix = QPixmap()
            pix.loadFromData(resp.content)
            self.pixmap_ready.emit(pix)
        except Exception:
            # On any error, emit an empty pixmap
            self.pixmap_ready.emit(QPixmap())


    




class CuteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Fox Viewer")
        self.resize(500, 550)
        self.setStyleSheet("background-color: black;")  # Set background color

        # Image display
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.image_label.setFixedSize(1000, 1000)
        self.image_label.setStyleSheet("background-color: black; color: white;")

        # Button to load a new image
        self.button = QPushButton("Find Fox")
        self.button.clicked.connect(self.load_image)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.worker = None
        self.load_image()

    def load_image(self):
        # Disable button while loading
        self.button.setEnabled(False)
        self.image_label.setText("Finding a Fox…")

        # Start worker thread
        self.worker = ImageFetcher()
        self.worker.pixmap_ready.connect(self.on_pixmap_ready)
        self.worker.start()

    def on_pixmap_ready(self, pix: QPixmap):
        # Display result (or placeholder text if empty)
        if not pix.isNull():
            self.image_label.setPixmap(pix.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
        else:
            self.image_label.setText("There was some kind of problem. \nPlease search again")
        self.button.setEnabled(True)
        self.worker = None


    

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CuteApp()
    win.show()
    sys.exit(app.exec())
     