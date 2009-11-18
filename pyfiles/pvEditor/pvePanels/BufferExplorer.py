import vim
import os
import re

from _PanelBase_ import PanelBase

from pyVim.pvListBuffer import pvListBuffer , pvListBufferObserver
from pyVim.pvUtil import pvString

from pyVim.pvWrap import pvBuffer , PV_BUF_TYPE_ATTACH
from pyVim.pvKeyMap import pvKeyMapEvent , pvKeyMapObserver , pvKeyMapManager
from pyVim.pvKeyMap import PV_KM_MODE_NORMAL



class _class_( PanelBase , pvListBufferObserver , pvKeyMapObserver ):
    def __init__( self , win_mgr ):
        self.__win_mgr = win_mgr
        self.__name = u"Buffer Explorer"

        self.__buffer = pvListBuffer()
        self.__buffer.registerObserver( self )

        refresh_event = pvKeyMapEvent( "<F5>" , PV_KM_MODE_NORMAL , self.__buffer )
        pvKeyMapManager.registerObserver( refresh_event , self )

        dbuffer_event = pvKeyMapEvent( "D" , PV_KM_MODE_NORMAL , self.__buffer )
        pvKeyMapManager.registerObserver( dbuffer_event , self )


    # from |PanelBase|
    def OnName( self ):
        str = pvString()
        str.UnicodeString = self.__name
        return str

    def OnPanelSelected( self , item ):
        if item.UnicodeString != self.__name :
            return

        self.__buffer.showBuffer( self.__win_mgr.getWindow('panel') )
        self.__buffer.updateBuffer( selection = self.analyzeBufferInfo() )

        self.__win_mgr.getWindow('panel').setFocus()


    def analyzeBufferInfo( self ):
        # get main window buffer
        buf_no = self.__win_mgr.getWindow('main').bufferid
        update_selection = 0

        # init the buffer info
        self.__buffer.items = []
        buffer_format = '%(bufferid)3d|[%(buffername)s]%(modifymark)1s'

        for buffer in vim.buffers :
            #  buffer exist
            #if vim.eval("bufexists(%d)" % ( buffer.number , ) ) != '0' :

            # get properties
            ## buffer id
            buffer_id = buffer.number
            ## buffer_name
            buffer_basename = os.path.basename( buffer.name if buffer.name else "<NO NAME>" )
            ## internal status
            is_listed = vim.eval('getbufvar(%d,"&buflisted")' % buffer_id ) != '0'
            is_modifiable = vim.eval('getbufvar(%d,"&modifiable")' % buffer_id ) != '0'
            is_readonly = vim.eval('getbufvar(%d,"&readonly")' % buffer_id ) != '0'
            is_modified = vim.eval('getbufvar(%d,"&modified")' % buffer_id ) != '0'

            if is_listed :
                if buffer_id == buf_no :
                    update_selection = len ( self.__buffer.items ) 
                str = pvString()
                str.MultibyteString = buffer_format % {
                        'bufferid' : buffer_id ,
                        'buffername' : buffer_basename , 
                        'modifymark' : '*' if is_modified else ' ' }
                self.__buffer.items.append( str )

        return update_selection


    def OnSelectItemChanged( self , item ):
        try :
            buffer_id = int( re.match('^(?P<id>\s*\d+)\|.*$' , item.MultibyteString ).group('id') )
        except:
            return

        # show the buffer on main panel
        show_buffer = pvBuffer( PV_BUF_TYPE_ATTACH )
        show_buffer.attach( buffer_id )
        show_buffer.showBuffer( self.__win_mgr.getWindow('main') )

        self.__win_mgr.getWindow('main').setFocus()

        # sync the cwd
        if show_buffer.name != None :
            dir_path , file_name = os.path.split( show_buffer.name )
            if os.path.isdir( dir_path ): os.chdir( dir_path )


    def OnHandleKeyEvent( self , **kwdict ):
        if kwdict['key'] == '<F5>':
            self.__buffer.updateBuffer( selection = self.analyzeBufferInfo() )
        elif kwdict['key'] == 'D' :
            if len ( self.__buffer.items ) == 1:
                return
            current_item_index = vim.current.window.cursor[0] - 1
            current_item = self.__buffer.items[ current_item_index ]

            # if delete the current selected one , just move down on item
            if current_item_index == self.__buffer.selection :
                self.__buffer.updateBuffer( selection = self.__buffer.selection + 1 )


            # if delete , move the selection
            if self.__buffer.selection > current_item_index :
                after_selection = self.__buffer.selection - 1
            else:
                after_selection = self.__buffer.selection

            # analyze the buffer id
            try :
                buffer_id = int ( re.match('^(?P<id>\s*\d+)\|.*$' , current_item.MultibyteString ).group('id') )
            except:
                return

            # delete buffer
            delete_buffer = pvBuffer( PV_BUF_TYPE_ATTACH )
            delete_buffer.attach( buffer_id )
            delete_buffer.wipeout()
            # delete list item
            del self.__buffer.items[current_item_index]

            self.__buffer.updateBuffer( selection = after_selection )

            





