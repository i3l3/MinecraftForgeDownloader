import os
import requests
import sys
from urllib.request import urlretrieve

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QCheckBox, QInputDialog


def setDeleteFileBool(state):
    deleteFileBool = True
    if state == Qt.Checked:
        deleteFileBool = True
    else:
        deleteFileBool = False
    return


class ForgeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        MCversionList = ['1.1', '1.2.3', '1.2.4', '1.2.5', '1.3.2', '1.4.0', '1.4.1', '1.4.2', '1.4.3', '1.4.4',
                         '1.4.5', '1.4.6', '1.4.7', '1.5', '1.5.1', '1.5.2', '1.6.1', '1.6.2', '1.6.3', '1.6.4',
                         '1.7.2', '1.7.10', '1.7.10_pre4', '1.8', '1.8.8', '1.8.9', '1.9', '1.9.4', '1.10', '1.10.2',
                         '1.11', '1.11.2', '1.12', '1.12.1', '1.12.2', '1.13.2', '1.14.2', '1.14.3', '1.14.4', '1.15',
                         '1.15.1', '1.15.2', '1.16.1','1.16.2', '1.16.3', '1.16.4', '1.16.5', '1.17.1']
        MCversionLabel = QLabel('Minecraft Version', self)
        MCversionLabel.move(50, 50)
        version = QComboBox(self)
        for i in MCversionList:
            version.addItem(i)
        version.move(160, 50)
        version.setCurrentText('1.17.1')

        downloadButton = QPushButton('Download!', self)
        downloadButton.move(100, 100)

        deleteFile = QCheckBox('Delete Zip File After Download', self)
        deleteFile.move(50, 80)
        deleteFile.toggle()

        deleteFile.stateChanged.connect(lambda: setDeleteFileBool(deleteFile))
        downloadButton.clicked.connect(lambda: self.download(version.currentText()))
        self.setWindowTitle('ForgeMDKDownloader')
        self.move(300, 300)
        self.resize(300, 210)
        self.show()

    def download(self, version):
        global url
        print('Forge Version: {}'.format(version))
        print('File Downloading...')
        html = requests.get('https://files.minecraftforge.net/net/minecraftforge/forge/index_{}.html'.format(version))
        html = html.text
        if version in ['1.13.2', '1.14.2', '1.14.3', '1.14.4', '1.15', '1.15.1', '1.15.2',
                       '1.16.1', '1.16.2', '1.16.3', '1.16.4', '1.16.5', '1.17.1']:
            html = html.split('<ul class="download-links">')[1]
            html = html.split('</ul>')[0]
            html = html.replace('                                            ', '')
            html = html.split('<li>')[3]
            html = html.split('</li>')[0].replace('    ', '')
            html = html.split('<a')[2]
            html = html.split('href="')[1]
            url = html.split('" title="Direct Download">')[0]
        elif version in ['1.12', '1.12.1']:
            html = html.split('<div class="download">')[1]
            html = html.split('</div>')[5]
            html = html.split('href="')[1]
            html = html.split('" title="Mdk"')[0]
            url = html.split('&url=')[1]
        elif version == '1.12.2':
            html = html.split('<div class="link">')[1]
            html = html.split('&url=')[1]
            url = html.split('" title="Mdk">')[0]
        elif version == '1.11.2':
            html = html.split('<div class="links">')[1]
            html = html.replace('                                            ', '')
            html = html.split('<div class="link">')[2]
            html = html.split('" title="Mdk">')[0]
            url = html.split('&url=')[1]
        elif version == '1.11':
            html = html.split('<div class="link">')[3]
            html = html.split('" title="Mdk"')[0]
            url = html.split('&url=')[1]
        elif version in ['1.10.2', '1.9.4']:
            html = html.split('<div class="links">')[1]
            html = html.replace('                                            ', '')
            html = html.split('<div class="link">')[2]
            html = html.split('" title="Mdk">')[0]
            url = html.split('&url=')[1]
        elif version in ['1.10', '1.9']:
            html = html.split('<div class="links">')[1]
            html = html.replace('                                            ', '')
            html = html.split('<div class="link">')[3]
            html = html.split('" title="Mdk">')[0]
            url = html.split('&url=')[1]
        print(url)
        urlretrieve(url, './forge-{}-mdk.zip'.format(version))
        print('Download Done.')
        print('File Unzipping...')
        os.system('powershell.exe Expand-Archive ./forge-{}-mdk.zip'.format(version))
        print('File Unzipping Done.')
        if setDeleteFileBool:
            print('Zip File Deleting...')
            os.system('powershell.exe del .\\forge-{}-mdk.zip'.format(version))
            print('Zip File Deleting Done.')
        print('Folder Renaming...')
        folderName, ok = QInputDialog.getText(self, 'Folder Name', 'Please enter your MDK folder name:')
        if ok:
            print(folderName)
            os.rename('./forge-{}-mdk'.format(version), folderName)
        print('Folder Renaming Done.')
        IDEs = ['IntelliJ', 'Eclipse']
        IDE, ok = QInputDialog.getItem(
            self, 'Select IDE', 'Select IDE what you prefer:', IDEs)
        if ok:
            if IDE == 'IntelliJ':
                self.getIntellijRuns(folderName)
            elif IDE == 'Eclipse':
                self.getEclipseRuns(folderName)

    def getIntellijRuns(self, dir):
        print('Project Setting...')
        os.chdir('.\\' + dir)
        os.system('.\\gradlew genIntellijRuns')
        print('Project Setting Done.')

    def getEclipseRuns(self, dir):
        print('Project Setting...')
        os.chdir('.\\' + dir)
        os.system('.\\gradlew genEclipseRuns')
        os.system('.\\gradlew eclipse')
        print('Project Setting Done.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = ForgeDownloader()
    sys.exit(app.exec_())
