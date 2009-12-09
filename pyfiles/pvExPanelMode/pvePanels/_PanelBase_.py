from pyVim.pvListBuffer import pvListBufferObserver

class PanelBase(object):
    @property
    def name(self):
        return self.OnName()

    def OnName(self):
        raise NotImplementedError("PanelBase::OnName")

    def OnPanelSelected( self , panel_name ):
        raise NotImplementedError("PanelBase::OnPanelSelected")
