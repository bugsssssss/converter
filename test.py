import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from moviepy.editor import VideoFileClip

class VideoConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Converter')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel('Select video files to convert:')
        self.layout.addWidget(self.label)

        self.convert_button = QPushButton('Convert Videos', self)
        self.convert_button.clicked.connect(self.convertVideos)
        self.layout.addWidget(self.convert_button)

        self.setLayout(self.layout)

    def convertVideos(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filepaths, _ = QFileDialog.getOpenFileNames(
            self, "Select Video Files", "", "Video Files (*.mp4 *.avi *.mov *.mkv *.flv *.wmv);;All Files (*)", options=options)

        if filepaths:
            try:
                # Set the static output directory
                try:
                    output_name = (self.input_file_path).split('/')[-1][:-4]

                except:
                    output_name = 'undefined'

                output_directory = f'/Users/nurbekabdurahmanov/Desktop/pyqt converter/converted/{output_name}.mp4'

                for filepath in filepaths:
                    # Construct the output filepath for each video
                    output_filepath = os.path.join(output_directory, os.path.basename(filepath.replace(' ', '_')) + "_converted.mp4")

                    # Convert video using moviepy
                    video = VideoFileClip(filepath)
                    video.write_videofile(output_filepath, codec='libx264', audio_codec='aac')
                    video.close()

                self.label.setText(f'Videos converted successfully.')
            except Exception as e:
                self.label.setText(f'Error converting videos: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoConverterApp()
    ex.show()
    sys.exit(app.exec_())
