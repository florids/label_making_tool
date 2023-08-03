import wx
import sys
import json


class LoginFrame(wx.Frame):
    def __init__(self, parent, id,UpdateUI = None):
        wx.Frame.__init__(self, parent, id, '用户登录', size=(500, 250))
        self.UpdateUI = UpdateUI
        self.InitUI()  # 绘制UI界面
    def InitUI(self):
            # 创建面板
            panel = wx.Panel(self)
            # 创建确定和取消按钮，并绑定事件
            self.bt_confirm = wx.Button(panel, label='确定', pos=(105, 130))
            self.bt_cancel = wx.Button(panel, label='清空', pos=(195, 130))
            self.bt_back = wx.Button(panel, label='退出', pos=(285, 130))
            self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
            self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickCancel)
            self.bt_back.Bind(wx.EVT_BUTTON, self.OnclickBack)

            self.title = wx.StaticText(panel, label="请输入用户名和密码", pos=(140, 20))
            self.label_user = wx.StaticText(panel, label="用户名", pos=(50, 50))
            self.label_pwd = wx.StaticText(panel, label="密 码", pos=(50, 90))
            self.text_user = wx.TextCtrl(panel, pos=(100, 50), size=(235, 25), style=wx.TE_LEFT)
            self.text_password = wx.TextCtrl(panel, pos=(100, 90), size=(235, 25), style=wx.TE_PASSWORD)
            #self.label_make = wx.TextCtrl(panel,pos=(200,50),size=(235,25))

    def OnclickSubmit(self, event):
        message = ""
        json_path = r"user.json"
        with open(json_path,"r") as f:
            user_message = json.load(f)
        username = self.text_user.GetValue()
        password = self.text_password.GetValue()
        # user_list = ['mr','yf','dyw','lhl','wxn','srx']
        # password_list = ['mrsoft','yf','dyw','lhl','wxn','srx']
        user_dic = {'mr':'mrsoft','yf':'yf','dyw':'dyw','lhl':'lhl','wxn':'wxn','srx':'srx'}
        if username == "" or password == "":
            message = "用户名或密码不能为空"
            wx.MessageBox(message)  # 弹出提示框
        elif username in user_dic.keys() and password == user_dic[username]:
        # else:
        #     # for i in range(len(user_message)):
        #     login = True
        #     while login:
        #         # for user_account in user_message[i]['account']:
        #         #     if
        #         # print(user_message[i]['account'])
        #         if username not in user_message[i]['account']:
        #             message = "此用户名不存在"
        #             wx.MessageBox(message)  # 弹出提示框
        #         if username in user_message[i]['account'] and password == user_message[i][username]:
        #             self.UpdateUI(1)  # 更新UI-Frame
        #             login = False
        #         elif username in user_message[i]['account'] and password != user_message[i][username]:
        #             message = "用户名和密码不匹配"
        #             wx.MessageBox(message)  # 弹出提示框
        # elif username in json.load(json_path)
            self.UpdateUI(1)  # 更新UI-Frame
        else:
            message = "用户名和密码不匹配"
            wx.MessageBox(message)  # 弹出提示框


    def OnclickCancel(self, event):
        self.text_user.SetValue("")  # 清空用户框
        self.text_password.SetValue("")  # 清空密码框
    def OnclickBack(self, event):
        sys.exit(0)
