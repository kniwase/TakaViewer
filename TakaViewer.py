import tkinter, os, cv2, numpy as np
from tkinter import filedialog, PhotoImage
from PIL import Image, ImageTk
from pyhsafm import afmimproc as aip

#機能の定義
def do_nothing(): pass

def make_scrollbar(root, child):
    scrollbar_y = tkinter.Scrollbar(root, orient=tkinter.VERTICAL)
    scrollbar_x = tkinter.Scrollbar(root, orient=tkinter.HORIZONTAL)
    scrollbar_y.config(command=child.yview)
    scrollbar_x.config(command=child.xview)
    scrollbar_y.grid(row=0, column=1, rowspan=2)
    scrollbar_x.grid(row=1, column=0, columnspan=2)
    return scrollbar_x, scrollbar_y


#メインウィンドウの定義
class Main_wiondow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        #GUIの定義
        self.title('File List')
        #変数の定義
        self.image_win = Image_win(self)
        self.scalebar_win = None

        self.file_list_box = File_list_box(self)
        self.sel_dir_button = Sel_dir_button(self)
        self.image_slidebar = Image_slidebar(self)
        self.autoplay_button = Autoplay_button(self)
        self.scalebar_button = Scalebar_button(self)

        self.file_list_box.grid(row=0, column=0, rowspan=10, columnspan=15, sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
        self.sel_dir_button.grid(row=10, column=1, columnspan=4, sticky=tkinter.W+tkinter.E)

        self.image_slidebar.grid(row=11, column=0, columnspan=14, rowspan=2, sticky=tkinter.W+tkinter.E)
        self.autoplay_button.grid(row=11, column=14, columnspan=1)
        self.scalebar_button.grid(row=12, column=14, columnspan=1)


#フォルダ選択ボタンの定義
class Sel_dir_button(tkinter.Button):
    def __init__(self, main_win):
        super().__init__(main_win, text='Slect Folder', command=self.select_dir)
        self.main_win = main_win

    #フォルダ選択用関数
    def select_dir(self):
        directory = filedialog.askdirectory()
        if directory != '':
            if self.main_win.file_list_box.size() != 0:
                self.main_win.file_list_box.delete(0, self.main_win.file_list_box.size())
            files = [os.path.join(directory, f) for f in os.listdir(directory)]
            files = [f for f in files if os.path.isfile(f)]
            asd_files = [f for f in files if os.path.splitext(f)[1] == '.asd']
            self.main_win.file_list_box.asd_files = asd_files
            for idx, f in enumerate(self.main_win.file_list_box.asd_files):
                self.main_win.file_list_box.insert(idx, os.path.basename(f))

#ファイル選択ボックスの定義
class File_list_box(tkinter.Listbox):
    def __init__(self, main_win):
        #GUIの定義
        self.Listbox_scrollbar_x, self.Listbox_scrollbar_y = make_scrollbar(main_win, self)
        super().__init__(main_win, height=12, width=80, selectmode=tkinter.SINGLE, yscrollcommand=self.Listbox_scrollbar_y.set, xscrollcommand=self.Listbox_scrollbar_x.set)
        #   リストボックスがクリックされたらファイル選択用関数を呼び出す
        self.bind('<<ListboxSelect>>', self.select_file)
        #変数の定義
        self.main_win = main_win
        self.asd_files = None
        self.idx = None

    #ファイル選択用関数
    def select_file(self, event):
        self.idx = self.curselection()[0]
        self.current_asd_file_name = self.asd_files[self.idx]
        self.main_win.image_win.load_asd(self.asd_files[self.idx])

#画像選択スライドバーの定義
class Image_slidebar(tkinter.Scale):
    def __init__(self, main_win):
        self.main_win = main_win
        super().__init__(main_win, variable=self.main_win.image_win.idx, orient=tkinter.HORIZONTAL, to=0)

#画像表示用ウィンドウの定義
class Image_win(tkinter.Toplevel):
    def __init__(self, main_win):
        super().__init__(main_win)
        self.main_win = main_win
        self.title('Image')
        self.protocol("WM_DELETE_WINDOW", self.iconify)
        self.img_canvas = tkinter.Canvas(self)
        self.img_canvas.pack()
        self.autopaly_id = None
        self.idx = tkinter.IntVar()
        self.idx.set(0)
        self.idx.trace("w", self.display_image)

    def convert_image(self, img_aip):
        img_opencv = img_aip.getOpenCVimage()
        shape = img_opencv.shape
        img_PIL = Image.fromarray(cv2.cvtColor(img_opencv, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(img_PIL)
        return img_tk, shape

    def load_asd(self, path):
        self.images = aip.ASD_reader(path)
        self.frame_time = self.images.header['FrameTime']
        self.main_win.image_slidebar.config(to=len(self.images)-1)
        self.img, shape = self.convert_image(self.images[0])
        self.img_showing = self.img_canvas.create_image(0, 0, image=self.img, anchor=tkinter.NW)
        self.img_canvas.config(width=shape[1], height=shape[0])
        self.config()
        self.idx.set(0)

    def display_image(self, *args):
        self.img, shape = self.convert_image(self.images[self.idx.get()])
        self.img_canvas.itemconfig(self.img_showing, image=self.img)

    def autoplay_image_start(self):
        if self.idx.get() < len(self.images)-1:
            self.autopaly_id = self.after(int(self.frame_time), self.autoplay_image)

    def autoplay_image(self):
        if self.idx.get() < len(self.images)-1:
            self.idx.set(self.idx.get()+1)
            self.autopaly_id = self.after(int(self.frame_time), self.autoplay_image)

    def autoplay_image_cancel(self):
        if self.autopaly_id != None:
            self.after_cancel(self.autopaly_id)
            self.autopaly_id = None

#スケールバー設定ウィンドウ表示ボタンの定義
class Scalebar_button(tkinter.Button):
    def __init__(self, main_win):
        super().__init__(main_win, text='Make Scalebar', command=self.scalebar_button)
        self.main_win = main_win

    def scalebar_button(self):
        if self.main_win.scalebar_win is None:
            self.main_win.scalebar_win = Scalebar_win(self.main_win)
        else:
            self.main_win.scalebar_win.destroy()
            self.main_win.scalebar_win = None

#スケールバー用ウィンドウ表示ボタンの定義
class Show_scalebar_button(tkinter.Button):
    def __init__(self, upper_win):
        super().__init__(master=upper_win, text='Get Scalebar', command=self.show_scalebar_img)
        self.upper_win = upper_win

    #スケールバー表示関数
    def show_scalebar_img(self):
        x = self.upper_win.x.get()
        y = self.upper_win.y.get()
        interval = self.upper_win.interval.get()
        y_axis_title = self.upper_win.y_axis_title.get()
        heightCorrection = self.upper_win.heightCorrection.get()

        import matplotlib.pyplot as plt
        plt = self.upper_win.main_win.scalebar_win.make_scalebar_img(plt, x, y, interval, y_axis_title, heightCorrection)
        file_name = os.path.splitext(os.path.basename(self.upper_win.main_win.file_list_box.current_asd_file_name))[0]
        plt.title('%s_%05d' % (file_name, self.upper_win.main_win.image_win.idx.get()))
        plt.show()

#スライドバーの定義
class X_value_slidebar(tkinter.Scale):
    def __init__(self, upper_win):
        self.upper_win = upper_win
        super().__init__(master=upper_win, variable=self.upper_win.x, orient=tkinter.HORIZONTAL, from_=10, to=250)

class Y_value_slidebar(tkinter.Scale):
    def __init__(self, upper_win):
        self.upper_win = upper_win
        super().__init__(master=upper_win, variable=self.upper_win.y, orient=tkinter.HORIZONTAL, from_=50, to=1000)

class Interval_value_slidebar(tkinter.Scale):
    def __init__(self, upper_win):
        self.upper_win = upper_win
        super().__init__(master=upper_win, variable=self.upper_win.interval, orient=tkinter.HORIZONTAL, from_=0.1, to=5.0, resolution=0.1)

#スケールバー用ウィンドウの定義
class Scalebar_win(tkinter.Toplevel):
    def __init__(self, main_win):
        super().__init__(master=main_win)
        self.main_win = main_win
        self.title('Scalebar Settings')
        self.protocol("WM_DELETE_WINDOW", self.iconify)
        self.x = tkinter.IntVar()
        self.y = tkinter.IntVar()
        self.interval = tkinter.DoubleVar()
        self.heightCorrection = tkinter.BooleanVar()
        self.x.set(100)
        self.y.set(500)
        self.interval.set(1.0)
        self.heightCorrection.set(True)

        self.x_label = tkinter.Label(master=self, text='X-axis size')
        self.x_value_slidebar = X_value_slidebar(self)
        self.y_label = tkinter.Label(master=self, text='Y-axis size')
        self.y_value_slidebar = Y_value_slidebar(self)
        self.scale_label = tkinter.Label(master=self, text='Scale interval')
        self.interval_value_slidebar = Interval_value_slidebar(self)

        self.y_axis_label = tkinter.Label(master=self, text='Y-axis title')
        self.y_axis_title = tkinter.Entry(master=self)
        self.y_axis_title.insert(tkinter.END, 'Height [nm]')

        self.heightCorrection_checkBox = tkinter.Checkbutton(master=self, text='Height Correction', variable=self.heightCorrection)

        self.show_scalebar_button = Show_scalebar_button(self)

        self.x_label.pack()
        self.x_value_slidebar.pack()
        self.y_label.pack()
        self.y_value_slidebar.pack()
        self.scale_label.pack()
        self.interval_value_slidebar.pack()
        self.y_axis_label.pack()
        self.y_axis_title.pack()
        self.heightCorrection_checkBox.pack()
        self.show_scalebar_button.pack()

    def getNearestIdx(self, l, n):
        return np.abs(np.asarray(l) - n).argmin()

    def make_scalebar_img(self, plt, x, y, interval, label, heightCorrection):
        scalebar_img = np.array([np.linspace(255, 0, y).astype(np.uint8) for _ in range(x)]).transpose()
        scalebar_img_color = np.zeros((*scalebar_img.shape, 3), np.uint8)
        scalebar_img_color[:,:,0] = np.ones(scalebar_img.shape, np.uint8)*19
        scalebar_img_color[:,:,1] = scalebar_img
        scalebar_img_color[:,:,2] = np.ones(scalebar_img.shape, np.uint8)*255
        scalebar_img_color = cv2.cvtColor(scalebar_img_color, cv2.COLOR_HLS2RGB)

        plt.imshow(scalebar_img_color)
        plt.tick_params(labelbottom="off",bottom="off")
        plt.ylabel(label)

        current_img = self.main_win.image_win.images[self.main_win.image_win.idx.get()]
        if heightCorrection:
            current_img = aip.heightCorrection(current_img)
        zdata = current_img.zdata

        zdata_linspace = np.linspace(zdata[0], zdata[1], y)
        y_scale = list(np.arange(0, zdata[0], -interval))[::-1] + list(np.arange(0, zdata[1], interval))
        y_position = [(y-1) - self.getNearestIdx(zdata_linspace, y_s) for y_s in y_scale]

        plt.yticks(y_position, [str(h) for h in y_scale])
        return plt

#自動再生ボタンの定義
class Autoplay_button(tkinter.Button):
    def __init__(self, main_win):
        super().__init__(main_win, text='Autoplay', command=self.autoplay)
        self.main_win = main_win

    def autoplay(self):
        if self.main_win.image_win.autopaly_id == None:
            self.main_win.image_win.autoplay_image_start()
            self.config(text='Stop')
        else:
            self.main_win.image_win.autoplay_image_cancel()
            self.config(text='Autoplay')

#メイン
main_win = Main_wiondow()
main_win.mainloop()
