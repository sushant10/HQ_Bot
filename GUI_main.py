import wx

class HQ_Bot(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(HQ_Bot, self).__init__(*args, **kw) 
        
        self.InitUI()
        
    def InitUI(self):   

        pnl = wx.Panel(self)
        #cbtn = wx.Button(pnl, label='Close', pos=(560, 600))
		#cbtn.Bind(wx.EVT_BUTTON, self.OnClose)

        self.SetSize((650, 650))
        self.SetTitle('wx.Button')
        self.Centre()
        self.Show(True)          
        
    def OnClose(self, e):
        self.Close(True)                  
        
def main():
    
    ex = wx.App()
    HQ_Bot(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()   