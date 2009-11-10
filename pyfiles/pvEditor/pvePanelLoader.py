from pyVim.pvListBuffer import pvListBuffer , pvListBufferObserver


class PanelManager(object):
    def __init__( self , win_mgr ):
        self.win_mgr = win_mgr

        # init the buffer show in 'caption window'
        self.buffer = pvListBuffer()
        self.buffer.showBuffer( self.win_mgr.getWindow('list') )
        self.buffer.updateBuffer( format = '< %-20s >' , hilight = 'Visual' , resize = True )

    def loadPanels( self ):
        from pvePanels import FileExplorer
        fe = FileExplorer._Panel_( self.win_mgr )
        self.buffer.items.append( fe.name )
        self.buffer.registerObserver( fe )
        self.buffer.updateBuffer()

    #def addPanel( self , panel ):
    #    # check if the name already exist
    #    if panel in self.panel_list :
    #        return False

    #    # save the data to info list and update UI
    #    self.panel_list.append( panel )
    #    self.buffer.updateBuffer( resize = True )

    #    if len( self.panel_list ) == 1 :
    #        buffer = panel.getBuffer()
    #        buffer.showBuffer( self.panel_win )
    #        buffer.updateBuffer() 

    #    return True

    #def removePanel( self , name_or_panel ):
    #    try :
    #        item_index = self.panel_list.index( panel_or_name )
    #    except:
    #        return
    #    # remoev , but save the ref to panel
    #    panel = self.panel_list.pop( item_index )
    #    self.buffer.updateBuffer( selection = 0 , resize = len( self.panel_list ) != 0 )
    #    self.switchPanel( self.panel_list[0] )
    #    return panel

    #def switchPanel( self , name_or_panel ):
    #    
    #    try :
    #        item_index = self.panel_list.index( name_or_panel )
    #    except:
    #        return


    #    self.buffer.updateBuffer( selection = item_index , resize = True )

    #    panel_buffer = self.panel_list[item_index].getBuffer()
    #    panel_buffer.showBuffer( self.panel_win )
    #    panel_buffer.updateBuffer()

    #def getCurrentPanel( self ):
    #    return self.panel_list[ self.buffer.getSelection() ]

    #def searchPanel( self , panel_or_name ):
    #    try :
    #        item_index = self.panel_list.index( panel_or_name )
    #    except:
    #        return None
    #    return self.panel_list[ item_index ]

    #def getTabBuffer( self ):
    #    return self.buffer

    #def getTabWindow( self ):
    #    return self.list_win

    #def getPanelWindow( self ):
    #    return self.panel_win






