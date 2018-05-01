import tkinter, os, cv2, numpy as np
from tkinter import filedialog
from niwaCV import niwaCV

def do_nothing():
    pass

#フォルダ選択用関数
def select_dir(event):
    def _select_dir():
        directory = filedialog.askdirectory()
        files = [os.path.join(directory, f) for f in os.listdir(directory)]
        files = [f for f in files if os.path.isfile(f)]
        asd_files = [f for f in files if os.path.splitext(f)[1] == '.asd']
        return asd_files

    if file_list_box.size() != 0:
        file_list_box.delete(0, file_list_box.size())
    file_list_box.asd_files = _select_dir()
    for idx, f in enumerate(file_list_box.asd_files):
        file_list_box.insert(idx, os.path.basename(f))
    file_list_box.pack()

#ファイル選択用関数
def select_file(event):
    idx = file_list_box.curselection()[0]
    print(file_list_box.asd_files[idx])

#メインウィンドウの定義
#   メインウィンドウはファイル選択ボックスのあるウィンドウ
class Main_wiondow(tkinter.Tk):
    def __init__(self):
        super(Main_wiondow, self).__init__()
        self.title('File List')

#フォルダ選択ボタンの定義
class Sel_dir_button(tkinter.Button):
    def __init__(self, main_win):
        super(Sel_dir_button, self).__init__(main_win, text='Slect Folder')
        self.bind('<Button-1>', select_dir)
        self.pack(side=tkinter.BOTTOM)

#ファイル選択ボックスの定義
class File_list_box(tkinter.Listbox):
    def __init__(self, main_win):
        self.Listbox_scrollbar_y = tkinter.Scrollbar(main_win, orient=tkinter.VERTICAL)
        self.Listbox_scrollbar_x = tkinter.Scrollbar(main_win, orient=tkinter.HORIZONTAL)
        super(File_list_box, self).__init__(main_win, height=12, width=80, selectmode=tkinter.SINGLE, yscrollcommand=self.Listbox_scrollbar_y.set, xscrollcommand=self.Listbox_scrollbar_x.set)
        self.Listbox_scrollbar_y.config(command=self.yview)
        self.Listbox_scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.Listbox_scrollbar_x.config(command=self.xview)
        self.Listbox_scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        self.bind('<<ListboxSelect>>', select_file)

#画像表示用ウィンドウの定義
class Image_win(tkinter.Toplevel):
    def __init__(self, main_win):
        super(Image_win, self).__init__(main_win)
        self.title('Image')
        self.protocol("WM_DELETE_WINDOW", do_nothing)

main_win = Main_wiondow()
sel_dir_button = Sel_dir_button(main_win)
file_list_box = File_list_box(main_win)


if 'image_win' in globals():
    pass
else:
    image_win = Image_win(main_win)

#メインループ
main_win.mainloop()
