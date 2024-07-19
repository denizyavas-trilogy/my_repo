import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader


class PDFSyncHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.pdf'):
            self.process_pdf(event.src_path)

    def process_pdf(self, path):
        try:
            reader = PdfReader(path)
            num_pages = len(reader.pages)
            print(f'Processed {path}:')
            print(f'Number of pages: {num_pages}')
            # Here you can add more processing, like extracting text, syncing to another location, etc.
        except Exception as e:
            print(f'Failed to process {path}: {e}')


def start_monitoring(path):
    event_handler = PDFSyncHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    path = '/Users/denizyavas/Downloads/Inv \ INV-218723244-20240501.pdf'  # Change this to the directory you want to monitor

