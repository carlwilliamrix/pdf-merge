## Simple PDF Merge App
Native Apple App UI is not working and Web Services should probably not be trusted with sensitive information.

#### How to package the App
Can be packed as Desktop Application. Using pyinstaller here but py2app can also work.
1. pip install pyinstaller
2. pyinstaller --onefile --windowed --name "PDFMerger" pdf-merger-main.py
