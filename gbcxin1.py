import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QRadioButton
from PySide6.QtGui import QIcon
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("gbcxin1v0.1")
offsets_3 = [0x200000, 0x400000, 0x600000]
offsets_4 = [0x100000, 0x200000, 0x400000, 0x600000]
offsets_7 = [0x100000 * i for i in range(1, 8)]
wordtrans = {
    "GBC X In 1 Binary Merger (by ChisBread)": "GBC X In 1 合卡工具(by ChisBread)",
    "Welcome to GBC X In 1 Binary Merger\nPlease select a menu binary and up to N game binaries to merge": "欢迎使用 GBC X In 1 合卡工具\n请选择一个菜单文件和最多 N 个游戏文件进行合并",
    "No files selected": "未选择文件",
    "3 in 1(2Mx3)": "3 合 1(2Mx3)",
    "4 in 1(1Mx1+2Mx3)": "4 合 1(1Mx1+2Mx3)",
    "7 in 1(1Mx7)": "7 合 1(1Mx7)",
    "Select Menu Binary": "选择菜单文件",
    "Select Game Files": "选择游戏文件",
    "Confirm and Merge": "确认并合并",
    "Menu binary: %s": "菜单文件: %s",
    "Game binary %s: %s": "游戏文件 %s: %s",
    "No menu binary selected": "未选择菜单文件",
    "No game binaries selected": "未选择游戏文件",
    "Save merged binary": "保存合并文件",
    "Merged": "已合并",
    "files into": "个文件到",
    "Select menu binary": "选择菜单文件",
    "Select game binaries": "选择游戏文件",
    "Binary files (*)": "二进制文件 (*)",
    "Save merged binary": "保存合并文件",
    "Merged %s files into %s": "已合并 %s 个文件到 %s",
}
def i18n(word):
    # 识别当前系统语言
    try:
        lang = "en"
        if sys.platform == 'win32':
            import ctypes
            lang = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            if lang == 2052:
                lang = "zh"

        else:
            import os
            lang = os.environ.get('LANG', 'en').split('_')[0]
    except:
        lang = "en"

    if lang == 'zh':
        return wordtrans.get(word, word)
    return word

class BinaryMerger(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(i18n('GBC X In 1 Binary Merger (by ChisBread)'))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        if sys.platform == 'win32':
            if getattr(sys, 'frozen', False):
                applicationPath = sys._MEIPASS
            elif __file__:
                applicationPath = os.path.dirname(__file__)
            icon_path = os.path.join(applicationPath, '.\\img\\icon-cheese-32.ico')
            self.setWindowIcon(QIcon(icon_path))

        self.hello = QLabel(i18n("Welcome to GBC X In 1 Binary Merger\nPlease select a menu binary and up to N game binaries to merge"))
        self.layout.addWidget(self.hello)

        self.splitter = QLabel("-------------------------------------------------------------------------")
        self.layout.addWidget(self.splitter)

        self.label = QLabel(i18n("No files selected"))
        self.layout.addWidget(self.label)

        self.merge3 = QRadioButton(i18n("3 in 1(2Mx3)"))
        self.layout.addWidget(self.merge3)

        self.merge4 = QRadioButton(i18n("4 in 1(1Mx1+2Mx3)"))
        self.layout.addWidget(self.merge4)

        self.merge7 = QRadioButton(i18n("7 in 1(1Mx7)"))
        self.layout.addWidget(self.merge7)

        self.menuButton = QPushButton(i18n("Select Menu Binary"))
        self.menuButton.clicked.connect(self.select_menu)
        self.layout.addWidget(self.menuButton)

        self.button = QPushButton(i18n("Select Game Files"))
        self.button.clicked.connect(self.select_files)
        self.layout.addWidget(self.button)

        self.confirmButton = QPushButton(i18n("Confirm and Merge"))
        self.confirmButton.clicked.connect(self.confirm_merge)
        self.layout.addWidget(self.confirmButton)

        self.menuFile = None
        self.gameFiles = None
        self.adjustSize()
    def update_label(self):
        lines = []
        if self.menuFile:
            lines.append(i18n("Menu binary: %s") % self.menuFile)
        else:
            lines.append(i18n("No menu binary selected"))
        if self.gameFiles:
            for i, file in enumerate(self.gameFiles):
                lines.append(i18n("Game binary %s: %s") % (i + 1, file))
        else:
            lines.append(i18n("No game binaries selected"))
        self.label.setText('\n'.join(lines))

    def select_menu(self):
        file, _ = QFileDialog.getOpenFileName(self, i18n('Select menu binary'), '', i18n('Binary files (*)'))
        if file:
            self.menuFile = file
            self.update_label()

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            i18n('Select game binaries'),
            '',
            i18n('Binary files (*)'),
            options=QFileDialog.DontUseNativeDialog
            )
        if files:
            self.gameFiles = files
            self.update_label()

    def confirm_merge(self):
        if self.menuFile and self.gameFiles:
            if self.merge3.isChecked():
                self.merge_files(self.gameFiles, 3)
            elif self.merge4.isChecked():
                self.merge_files(self.gameFiles, 4)
            elif self.merge7.isChecked():
                self.merge_files(self.gameFiles, 7)

    def merge_files(self, files, merge_type):
        if merge_type == 3:
            offsets = offsets_3
        elif merge_type == 4:
            offsets = offsets_4
        elif merge_type == 7:
            offsets = offsets_7

        output_file, _ = QFileDialog.getSaveFileName(self, i18n('Save merged binary'), '', i18n('Binary files (*)'))

        if output_file:
            with open(output_file, 'wb') as outfile:
                with open(self.menuFile, 'rb') as menufile:
                    outfile.write(menufile.read())
                for i, file in enumerate(files):
                    with open(file, 'rb') as infile:
                        outfile.seek(offsets[i])
                        outfile.write(infile.read())

            self.label.setText(i18n("Merged %s files into %s") % (len(files), output_file))

app = QApplication(sys.argv)

window = BinaryMerger()
window.show()

sys.exit(app.exec())
