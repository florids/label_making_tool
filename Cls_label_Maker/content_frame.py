import os
import wx
import sys

from Open_dir import Open_Dir as OD

class Main_Edit_Frame(wx.Frame):
    def __init__(self, parent, id,UpdateUI = None):
        wx.Frame.__init__(self, parent, id, 'Cls_Label_Maker', size=(1200, 900))  #1600, 900
        self.UpdateUI = UpdateUI                    #更新
        self.InitUI()                               # 绘制UI界面
        self.max_row = 10                           #设置文本框的行和列
        self.max_line = 4
        self.cur_point = 10                         #设置当前页面指针，用来控制获取当前页面数据列表，由于初始化界面会显示最大10张数据，因此指针从10开始
        self.click_count = 0                        #记录点击下一页事件次数，用来控制保存当前页面标签


    def InitUI(self):
        # 创建面板
        self.panel = wx.Panel(self)
        self.first_page = 1                             #控制初始化界面数据的保存，仅在最开始使用一次
        self.input_list_ = []                           #保存所有文本框内容
        self.init_inputbox()                            #初始化界面排版
        self.sizer = wx.GridBagSizer(10, 20)            # 列间隔为10，行间隔为20
        self.init_sizer()                               #初始化排版图像部分的背景填充

        # 创建确定和取消按钮，并绑定事件
        self.bt_confirm = wx.Button(self.panel, label='保存', pos=(700, 700),style=wx.TE_PROCESS_ENTER)           #用鼠标或者是enter皆可。
        self.bt_cancel = wx.Button(self.panel, label='清空', pos=(700, 740),style=wx.TE_PROCESS_ENTER)
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.Onclick_save_res)                                               #为按钮设置后台事件响应
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickCancel)
        self.bt_next = wx.Button(self.panel, label='下一页', pos=(700,780),style=wx.TE_PROCESS_ENTER)
        self.bt_next.Bind(wx.EVT_BUTTON, self.OnclickNext_Page)

        self.bt_exit = wx.Button(self.panel, label='退出', pos=(1000, 740))
        self.bt_exit.Bind(wx.EVT_BUTTON, self.OnclickBack)
        self.start_loc_w = 400                                                                                   #标签说明部分在界面中的位置显示
        self.start_loc_h = 50
        self.use_config = wx.StaticText(self.panel, label="标注工具使用说明：待标注完毕后，需先进行保存，再点击下一页。", pos=(self.start_loc_w, 20))   #静态文本显示
        self.lane_config = wx.StaticText(self.panel, label="标签说明", pos=(self.start_loc_w, self.start_loc_h))   #静态文本显示
        self.lane_cls_0 = wx.StaticText(self.panel, label="车道线：1  非车道线： 0", pos=(self.start_loc_w, self.start_loc_h+30))   #静态文本显示
        self.lane_cls_1 = wx.StaticText(self.panel, label="车道线颜色：白色：0  黄色：1", pos=(self.start_loc_w, self.start_loc_h+60))  # 静态文本显示
        self.lane_cls_2 = wx.StaticText(self.panel, label="车道线类型：实线：0  虚线：1  左虚右实：2  左实右虚：3  双实线：4  双虚线：5  其他：6", pos=(self.start_loc_w, self.start_loc_h+90))
        self.lane_cls_2 = wx.StaticText(self.panel, label="辅助线类型：马路牙子：0  导流线：1  减速线：2  潮汐车道线：3  可变车道线：4  其他车道线：5", pos=(self.start_loc_w, self.start_loc_h+120))

        self.dir_name = r""                                     #初始化导入数据文件路径，接收上一界面中传入的路径
        self.csv_name = r""                                     #同上
        self.cur_img_list = []                                  #当前页面的图像列表
        self.img_list = []                                      #总传入数据的文件名list
        self.img_list = self.on_tree_select()
        self.num = len(self.img_list) / 10                      #最大点击事件次数，用来控制最大页数
        if len(self.img_list) < 10:                             #初始化界面需要考虑到数据太少的情况。
            self.first_page_list = self.img_list
            self.show_img(self.img_list)
        else:
            self.first_page_list = self.img_list[:10]
            self.show_img(self.img_list[:10])

    def init_inputbox(self):
        self.max_line = 4
        self.max_row = 10
        self.start_loc_w = 400   #初始化页面文字位置
        self.start_loc_h = 20
        label_list = ["是否车道线： ","车道线颜色： ","车道线类型： ","辅助线类型： "]
        for j in range(self.max_row):
            input_list = []
            for i in range(self.max_line):              #遍历生成10*4文本框
                self.input_label = wx.StaticText(self.panel, label=str(label_list[i]), pos=(self.start_loc_w+200*i, 200+40*j))
                self.input_item = wx.TextCtrl(self.panel, pos=(self.start_loc_w+100+(200*i), 200+40*j), size=(50, 25), style=wx.TE_LEFT)
                self.input_item.SetValue("1")           #设置初始值为1
                input_list.append(self.input_item)
            self.input_list_.append(input_list)         #添加至list中

    def Onclick_save_res(self, event):
        save_csv_file = self.csv_name
        with open(save_csv_file,"a+") as f:
            # print("num:",self.num,self.click_count)
            if self.click_count < self.num:
                if self.first_page:    #初始化首页界面时，会先加载10张图像，需要先保存这10张图像的标签
                    for i, img_path in enumerate(self.first_page_list):
                        f.write(img_path + "\t" + str(self.input_list_[i][0].GetValue()) + "\t" + str(
                            self.input_list_[i][1].GetValue()) + "\t" + str(
                            self.input_list_[i][2].GetValue()) + "\t" + str(self.input_list_[i][3].GetValue()) + "\n")
                    self.first_page = 0
                else:     #点击下一页后，保存后续页面的图像标签
                    for i,img_path in enumerate(self.cur_img_list):
                        # print("第二次")
                        # # print(img_path + "\t" + str(self.input_list_[i][0].GetValue()) + "\t" + str(self.input_list_[i][1].GetValue()) + "\t" + str(self.input_list_[i][2].GetValue()) + "\t"  + str(self.input_list_[i][3].GetValue()) + "\n")
                        f.write(img_path + "\t" + str(self.input_list_[i][0].GetValue()) + "\t" + str(self.input_list_[i][1].GetValue()) + "\t" + str(self.input_list_[i][2].GetValue()) + "\t"  + str(self.input_list_[i][3].GetValue()) + "\n")
            else:   #当下一页的点击次数大于总的点击次数时，说明文件已经读取完了，因此进行提示
                message = "无法保存，当前页没有图像"
                wx.MessageBox(message)  # 弹出提示框
    def OnclickCancel(self, event):
        for i in range(self.max_line):   #清空时不考虑其他，直接将所有文本框内容清空
            for j in range(self.max_line):
                self.input_list_[i][j].SetValue("")
    def OnclickNext_Page(self,event):                                  #点击下一页，会出现新的图片list以及新的标注
        self.cur_point,self.cur_img_list = self.Get_img_list()         #获取当前页面的数据列表
        self.show_img(self.cur_img_list)                               #将数据展示到当前页面
        self.click_count += 1                                          #记录下一页的点击次数
        print("click_count: ",self.click_count)
        if self.click_count > self.num:                                #点击次数超过可点击总数，进行提示
            message = "已经到底啦"
            wx.MessageBox(message)                                     # 弹出提示框

    def OnclickBack(self, event):  #退出
        self.Destroy()
        sys.exit(0)

    def Get_img_list(self):  #获取当前页图像list
        if self.cur_point + 10 > len(self.img_list):        #当浏览至最后一页时，如果不够一页数据，则加载剩下数据
            self.cur_img_list = self.img_list[self.cur_point:len(self.img_list)]
            self.cur_point = len(self.img_list)
        else:      #正常加载满一页数据
            self.cur_img_list = self.img_list[self.cur_point:self.cur_point+10]
            self.cur_point += 10
        print("cur_point ",self.cur_point)
        return self.cur_point,self.cur_img_list

    def show_img(self,img_path_list):  #将图像展示到self.panel上
        length_cur_list = len(img_path_list)
        print("len_cur_path_list: ",length_cur_list)
        if length_cur_list == 10:         #当加载页面数据达到最大加载数时，则全部加载
            for i in range(length_cur_list):
                image = wx.Image(img_path_list[i], wx.BITMAP_TYPE_ANY).Rescale(250, 75).ConvertToBitmap()
                self.bmp_list[i].SetBitmap(wx.Bitmap(image))
        else:     #当数据不够一页时，则只加载剩下部分，其余位置为默认背景
            for i in range(length_cur_list):
                image = wx.Image(img_path_list[i], wx.BITMAP_TYPE_ANY).Rescale(250, 75).ConvertToBitmap()
                self.bmp_list[i].SetBitmap(wx.Bitmap(image))
            for i in range(length_cur_list,10):
                image = self.image1
                self.bmp_list[i].SetBitmap(wx.Bitmap(image))

    def on_tree_select(self):  #获取数据路径和标签保存路径
        od_ = OD(parent=None, id=1, call=None, UpdateUI=self.UpdateUI)   #获取上一页面传入的路径
        self.dir_name,self.csv_name = od_.__call__()
        print("dir_name: ",self.dir_name,self.csv_name)

        for img_path_ in os.listdir(self.dir_name):
            img_path = os.path.join(self.dir_name,img_path_)
            self.img_list.append(img_path)
        return self.img_list
    def Clear_page(self):
        self.input_item.SetValue("")
    def init_sizer(self):
        # self.bmp_list = []
        self.background_size_w,self.background_size_h = 250,75   #设置背景框尺寸
        self.image1 = wx.EmptyImage(self.background_size_w, self.background_size_h)   #生成背景框

        #初始化，将背景框填入位置
        self.bmp1 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp1, pos=(0, 1), flag=wx.ALL, border=5)
        self.bmp2 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp2, pos=(1, 1), flag=wx.ALL, border=5)
        self.bmp3 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp3, pos=(2, 1), flag=wx.ALL, border=5)
        self.bmp4 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp4, pos=(3, 1), flag=wx.ALL, border=5)
        self.bmp5 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp5, pos=(4, 1), flag=wx.ALL, border=5)
        self.bmp6 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp6, pos=(5, 1), flag=wx.ALL, border=5)
        self.bmp7 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp7, pos=(6, 1), flag=wx.ALL, border=5)
        self.bmp8 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp8, pos=(7, 1), flag=wx.ALL, border=5)
        self.bmp9 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp9, pos=(8, 1), flag=wx.ALL, border=5)
        self.bmp10 = wx.StaticBitmap(self.panel, -1, self.image1)  # 转化为wx.StaticBitmap()形式
        self.sizer.Add(self.bmp10, pos=(9, 1), flag=wx.ALL, border=5)
        self.bmp_list = [self.bmp1,self.bmp2,self.bmp3,self.bmp4,self.bmp5,self.bmp6,self.bmp7,self.bmp8,self.bmp9,self.bmp10]
        #同上
        self.text0 = wx.StaticText(self.panel, label="第1张图")
        self.sizer.Add(self.text0, pos=(0, 0), flag=wx.ALL, border=5)
        self.text1 = wx.StaticText(self.panel, label="第2张图")
        self.sizer.Add(self.text1, pos=(1, 0), flag=wx.ALL, border=5)
        self.text2 = wx.StaticText(self.panel, label="第3张图")
        self.sizer.Add(self.text2, pos=(2, 0), flag=wx.ALL, border=5)
        self.text3 = wx.StaticText(self.panel, label="第4张图")
        self.sizer.Add(self.text3, pos=(3, 0), flag=wx.ALL, border=5)
        self.text4 = wx.StaticText(self.panel, label="第5张图")
        self.sizer.Add(self.text4, pos=(4, 0), flag=wx.ALL, border=5)
        self.text5 = wx.StaticText(self.panel, label="第6张图")
        self.sizer.Add(self.text5, pos=(5, 0), flag=wx.ALL, border=5)
        self.text6 = wx.StaticText(self.panel, label="第7张图")
        self.sizer.Add(self.text6, pos=(6, 0), flag=wx.ALL, border=5)
        self.text7 = wx.StaticText(self.panel, label="第8张图")
        self.sizer.Add(self.text7, pos=(7, 0), flag=wx.ALL, border=5)
        self.text8 = wx.StaticText(self.panel, label="第9张图")
        self.sizer.Add(self.text8, pos=(8, 0), flag=wx.ALL, border=5)
        self.text9 = wx.StaticText(self.panel, label="第10张图")
        self.sizer.Add(self.text9, pos=(9, 0), flag=wx.ALL, border=5)
        #自适应尺寸
        self.panel.SetSizerAndFit(self.sizer)

