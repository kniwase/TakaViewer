import tkinter, os, cv2, numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk
from niwaCV import niwaCV

#機能の定義
def do_nothing(): pass

def make_scrollbar(root, child):
    scrollbar_y = tkinter.Scrollbar(root, orient=tkinter.VERTICAL)
    scrollbar_x = tkinter.Scrollbar(root, orient=tkinter.HORIZONTAL)
    scrollbar_y.config(command=child.yview)
    scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    scrollbar_x.config(command=child.xview)
    scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    return scrollbar_x, scrollbar_y


#メインウィンドウの定義
class Main_wiondow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        #GUIの定義
        self.title('File List')
        #変数の定義
        self.image_win = Image_win(self)
        self.sel_dir_button = Sel_dir_button(self)
        self.file_list_box = File_list_box(self)

#フォルダ選択ボタンの定義
class Sel_dir_button(tkinter.Button):
    def __init__(self, main_win):
        super().__init__(main_win, text='Slect Folder')
        #変数の定義
        self.main_win = main_win
        #GUIの定義
        #   ファイル選択ボタンがクリックされたらフォルダ選択用関数が呼び出される
        self.bind('<Button-1>', self.select_dir)
        self.pack(side=tkinter.BOTTOM)

    #フォルダ選択用関数
    def select_dir(self, event):
        def _select_dir():
            directory = filedialog.askdirectory()
            files = [os.path.join(directory, f) for f in os.listdir(directory)]
            files = [f for f in files if os.path.isfile(f)]
            asd_files = [f for f in files if os.path.splitext(f)[1] == '.asd']
            return asd_files
        if self.main_win.file_list_box.size() != 0:
            self.main_win.file_list_box.delete(0, self.main_win.file_list_box.size())
        self.main_win.file_list_box.asd_files = _select_dir()
        for idx, f in enumerate(self.main_win.file_list_box.asd_files):
            self.main_win.file_list_box.insert(idx, os.path.basename(f))
        self.main_win.file_list_box.pack()

#ファイル選択ボックスの定義
class File_list_box(tkinter.Listbox):
    def __init__(self, main_win):
        #GUIの定義
        self.Listbox_scrollbar_x, self.Listbox_scrollbar_y = make_scrollbar(main_win, self)
        super().__init__(main_win, height=12, width=80, selectmode=tkinter.SINGLE, yscrollcommand=self.Listbox_scrollbar_y.set, xscrollcommand=self.Listbox_scrollbar_x.set)
        self.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        #   リストボックスがクリックされたらファイル選択用関数を呼び出す
        self.bind('<<ListboxSelect>>', self.select_file)
        #変数の定義
        self.main_win = main_win
        self.asd_files = None
        self.idx = None

    #ファイル選択用関数
    def select_file(self, event):
        self.idx = self.curselection()[0]
        self.main_win.image_win.load_asd(self.asd_files[self.idx])

#画像表示用ウィンドウの定義
class Image_win(tkinter.Toplevel):
    def __init__(self, main_win):
        super().__init__(main_win)
        self.title('Image')
        self.protocol("WM_DELETE_WINDOW", do_nothing)

    def load_asd(self, path):
        self.images = niwaCV.ASD_reader(path)
        self.frame_time = self.images.header['FrameTime']
        print(self.images.header['Comment'])
        self.idx = 0
        self.autoplay = None
        self.display_image(self.idx)

    def display_image(self, idx):
        pass


#メイン
main_win = Main_wiondow()
main_win.mainloop()
