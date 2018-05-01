import tkinter, os, cv2, numpy as np
from tkinter import filedialog
from niwaCV import niwaCV

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
main_win = tkinter.Tk()
main_win.title('File List')

#フォルダ選択ボタンの定義
button = tkinter.Button(main_win ,text='Slect Folder')
button.bind('<Button-1>', select_dir)
button.pack(side=tkinter.BOTTOM)

#ファイル選択ボックスの定義
Listbox_scrollbar_y = tkinter.Scrollbar(main_win, orient=tkinter.VERTICAL)
Listbox_scrollbar_x = tkinter.Scrollbar(main_win, orient=tkinter.HORIZONTAL)
file_list_box = tkinter.Listbox(main_win, height=12, width=80, selectmode=tkinter.SINGLE, yscrollcommand=Listbox_scrollbar_y.set, xscrollcommand=Listbox_scrollbar_x.set)
Listbox_scrollbar_y.config(command=file_list_box.yview)
Listbox_scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
Listbox_scrollbar_x.config(command=file_list_box.xview)
Listbox_scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)
file_list_box.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
file_list_box.bind('<<ListboxSelect>>', select_file)

#メインループ
main_win.mainloop()
