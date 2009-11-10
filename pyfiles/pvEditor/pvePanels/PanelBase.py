from pyVim.pvListBuffer import pvListBufferObserver

class PanelBase(pvListBufferObserver):
    @property
    def name(self):
        return self.OnName()

    def OnName(self):
        raise NotImplementedError("PanelBase::OnName")

    def OnSelectItemChanged( self , item ):
        raise NotImplementedError("PanelBase::OnSelectItemChanged")
