import loginFrame
import content_frame
import Open_dir


#通过gui管理类来实现不同页面之间的调用
class GuiManager():
    def __init__(self, UpdateUI):
        self.UpdateUI = UpdateUI
        self.frameDict = {}  # 用来装载已经创建的Frame对象
        self.value = []


    def GetFrame(self, type):
        frame = self.frameDict.get(type)

        if frame is None:
            frame = self.CreateFrame(type)
            self.frameDict[type] = frame

        return frame

    def CreateFrame(self, type):
        if type == 0:
            return loginFrame.LoginFrame(parent=None, id=type, UpdateUI=self.UpdateUI)
        elif type == 1:
            return Open_dir.Open_Dir(parent=None, id=type, call="", UpdateUI=self.UpdateUI)
        elif type == 2:
            return content_frame.Main_Edit_Frame(parent=None, id=type,UpdateUI=self.UpdateUI)