import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from moviepy.editor import VideoFileClip
import os


class VideoConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Video Converter')
        self.setGeometry(200, 200, 600, 400)

        self.input_label = QLabel('Input Video:')
        self.output_label = QLabel('Output Path:')
        self.status_label = QLabel('Status: Ready')

        self.input_file_path = None
        self.output_file_path = None

        self.btn_browse_input = QPushButton('Browse Input', self)
        self.btn_browse_input.clicked.connect(self.browse_input)

        self.btn_browse_output = QPushButton('Browse Output', self)
        self.btn_browse_output.clicked.connect(self.browse_output)

        self.btn_convert = QPushButton('Convert', self)
        self.btn_convert.clicked.connect(self.convert_video)

        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.btn_browse_input)
        layout.addWidget(self.output_label)
        layout.addWidget(self.btn_browse_output)
        layout.addWidget(self.status_label)
        layout.addWidget(self.btn_convert)

        self.setLayout(layout)

    def browse_input(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi *.mov)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setOptions(options)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.input_file_path = selected_files[0]
                self.input_label.setText(
                    f'Input Video: {self.input_file_path}')
                self.status_label.setText('Status: Ready')

    def browse_output(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly | QFileDialog.ShowDirsOnly
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOptions(options)

        if file_dialog.exec_():
            selected_directory = file_dialog.selectedFiles()
            if selected_directory:
                self.output_file_path = selected_directory[0]
                self.output_label.setText(
                    f'Output Path: {self.output_file_path}')
                self.status_label.setText('Status: Ready')

    def convert_video(self):

        if not self.input_file_path:
            self.status_label.setText('Status: Please select input file.')
            return

        if not self.output_file_path:
            self.status_label.setText(
                'Status: Please select output directory.')
            return

        try:
            # Set the output file path using the selected output directory
            output_name = os.path.splitext(
                os.path.basename(self.input_file_path))[0]
            output_directory = os.path.join(
                self.output_file_path, f'{output_name}_converted.mp4')

            video_clip = VideoFileClip(self.input_file_path)
            video_clip.write_videofile(output_directory, codec='libx264', audio_codec='aac', ffmpeg_params=[
                                       '-c:v', 'h264_nvenc', '-b:v', '5M'])
            self.status_label.setText('Status: Conversion Successful!')
        except Exception as e:
            self.status_label.setText(f'Status: Error - {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter_app = VideoConverterApp()
    converter_app.show()
    sys.exit(app.exec_())
