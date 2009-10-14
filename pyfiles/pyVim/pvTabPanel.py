from pvExBuffer import pvListBuffer , pvListBufferItem

class pvTabPanelItem( pvListBufferItem ):
    def getBuffer( self ):
        raise RuntimeError('no implement')

    # from pvListBufferItem
    # should implement the __str__ method


class pvTabPanelManager:
    def __init__( self , list_window , panel_window ):
        # make the window manager , used to split window
        self.list_win = list_window
        self.panel_win = panel_window

        # init the buffer show in 'list'
        self.buffer = pvListBuffer()
        self.panel_list = self.buffer.getItemList()

        self.buffer.showBuffer( self.list_win )
        self.buffer.updateBuffer()

    def addPanel( self , panel ):
        # check if the name already exist
        if panel in self.panel_list :
            return False

        # save the data to info list and update UI
        self.panel_list.append( panel )
        self.buffer.updateBuffer( resize = True )

        if len( self.panel_list ) == 1 :
            buffer = panel.getBuffer()
            buffer.showBuffer( self.panel_win )
            buffer.updateBuffer() 

        return True

    def removePanel( self , name_or_panel ):
        try :
            item_index = self.panel_list.index( panel_or_name )
        except:
            return
        # remoev , but save the ref to panel
        panel = self.panel_list.pop( item_index )
        self.buffer.updateBuffer( selection = 0 , resize = len( self.panel_list ) != 0 )
        self.switchPanel( self.panel_list[0] )
        return panel

    def switchPanel( self , name_or_panel ):
        try :
            item_index = self.panel_list.index( name_or_panel )
        except:
            return
        self.buffer.updateBuffer( selection = item_index , resize = True )

        panel_buffer = self.panel_list[item_index].getBuffer()
        panel_buffer.showBuffer( self.panel_win )
        panel_buffer.updateBuffer()

    def getCurrentPanelItem( self ):
        return self.panel_list[ self.buffer.getSelection() ]

    def getListWindow( self ):
        return self.list_win

    def getPanelWindow( self ):
        return self.panel_win






