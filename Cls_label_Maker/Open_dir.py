import wx
import os
import sys
import pathlib

# global dir_name
# global csv_name


class Open_Dir(wx.Frame):
    def __init__(self, parent, id, call,UpdateUI = None):
        wx.Frame.__init__(self, parent, id, '打开目录', size=(500, 250))
        self.UpdateUI = UpdateUI
        self.InitUI()  # 绘制UI界面
        self.call = call
        # self.dir_name = r""
        # self.csv_name = r""
        # self.csv_name = None
        # self.root_dir = root_dir
    def InitUI(self):
        # 创建面板
        panel = wx.Panel(self)
        # 创建确定和取消按钮，并绑定事件
        self.bt_confirm = wx.Button(panel, label='确定', pos=(105, 130),style=wx.TE_PROCESS_ENTER)
        self.bt_cancel = wx.Button(panel, label='取消', pos=(195, 130),style=wx.TE_PROCESS_ENTER)
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickCancel)
        self.bt_back = wx.Button(panel, label='退出', pos=(285, 130),style=wx.TE_PROCESS_ENTER)
        self.bt_back.Bind(wx.EVT_BUTTON, self.OnclickBack)

        self.open_dir =wx.StaticText(panel, label="输入文件目录", pos=(50, 50))   #静态文本显示
        self.dir_path = wx.TextCtrl(panel, pos=(130, 50), size=(235, 25), style=wx.TE_LEFT)    #输入文本框,256表示框在中间


        # # 创建一个垂直布局的主容器，并将其设置为窗体的主布局管理器
        # main_sizer = wx.BoxSizer(wx.VERTICAL)
        # self.SetSizer(main_sizer)
        #
        # # 创建一个水平布局的容器，用于将树状组件和预览窗格放置在同一行
        # hbox = wx.BoxSizer(wx.HORIZONTAL)
        # main_sizer.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        #
        # # 创建一个树状组件，用于显示指定目录中的所有文件
        # self.tree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        # self.root = self.tree.AddRoot("Root")
        # hbox.Add(self.tree, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # 创建一个按钮，用于打开文件夹选择对话框
        # button = wx.Button(self, wx.ID_ANY, "Open Folder")
        # hbox.Add(button, proportion=0, flag=wx.ALL, border=5)

        # 将按钮的单击事件绑定到处理函数self.on_open_folder()上
        # button.Bind(wx.EVT_BUTTON, self.OnclickSubmit)

        # # 将树状组件的选中事件绑定到处理函数self.on_tree_select()上
        # self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_select, self.tree)

        self.save_csv = wx.StaticText(panel, label="标签保存路径", pos=(50, 80))  # 静态文本显示
        self.csv_path = wx.TextCtrl(panel, pos=(130, 80), size=(235, 25), style=wx.TE_LEFT)  # 输入文本框

    def OnclickSubmit(self, event):
        # message = ""
        global dir_name
        self.dir_name = self.dir_path.GetValue()
        dir_name = self.dir_path.GetValue()
        # print("dir_name: ",self.dir_name)
        if self.dir_name == "":
            message = "目录名不能为空"
            wx.MessageBox(message)  # 弹出提示框
        else:
            if not os.path.isdir(self.dir_name):
                message = "不是目录"
                wx.MessageBox(message)  # 弹出提示框
            else:
                pass
                #创建新页面，并显示主编辑界面
                # self.UpdateUI(2)
                # self.call(dir_name)
                # dialog = wx.DirDialog(self, "Select a folder")
                # return self.dir_name
        message = ""
        global csv_name
        self.csv_name = self.csv_path.GetValue()
        csv_name = self.csv_path.GetValue()
        # print(self.csv_name,csv_name)
        if self.csv_name == "":
            message = "标签保存路径不能为空"
            wx.MessageBox(message)  # 弹出提示框
        else:
            suffix_name = ['csv', 'txt']
            # print(self.csv_name.split('.')[-1])
            if self.csv_name.split('.')[-1] not in suffix_name:  # not in self.csv_name:
                message = "路径不正确，请重新输入"
                wx.MessageBox(message)  # 弹出提示框
            else:
                # if not os.path.isfile(self.csv_name):
                pathlib.Path(self.csv_name).touch()
                # 创建新页面，并显示主编辑界面
                self.UpdateUI(2)
                # self.call(self.csv_path.SetValue())
                self.Destroy()
    def Onclickchose_path(self,event):
        message = ""
        global csv_name
        self.csv_name = self.csv_path.GetValue()
        csv_name = self.csv_path.GetValue()
        # print(self.csv_name,csv_name)
        if self.csv_name == "":
            message = "标签保存路径不能为空"
            wx.MessageBox(message)  # 弹出提示框
        else:
            suffix_name = ['csv','txt']
            # print(self.csv_name.split('.')[-1])
            if self.csv_name.split('.')[-1] not in suffix_name: # not in self.csv_name:
                message = "路径不正确，请重新输入"
                wx.MessageBox(message)  # 弹出提示框
            else:
                # if not os.path.isfile(self.csv_name):
                pathlib.Path(self.csv_name).touch()
                # 创建新页面，并显示主编辑界面
                self.UpdateUI(2)
                # self.call(self.csv_path.SetValue())
                self.Destroy()
    def OnclickCancel(self, event):
        self.dir_path.SetValue("")  #
    def OnclickBack(self, event):
        # sys.exit(0)
        self.Destroy()
    def __call__(self):
        global dir_name
        global csv_name
        # print("name: ",dir_name,csv_name)
        return dir_name,csv_name



