import vim
import os
import re

# for log
import logging
_logger = logging.getLogger('pve.BufferExplorer')


# basic buffer
from pyvim.pvWrap import pvBuffer , PV_BUF_TYPE_ATTACH
from pyvim.pvWrap import pvWindow
# tab buffer
from pyvim.pvTab import pvTabBuffer , pvTabBufferObserver
from pyvim.pvUtil import pvString
# for key map
from pyvim.pvKeymap import pvKeymapEvent , pvKeymapObserver , pvKeymapManager
from pyvim.pvKeymap import PV_KM_MODE_NORMAL
# for autocmd
from pyvim.pvAutocmd import pvAutocmdEvent , pvAutocmdObserver , pvAutocmdManager




class TabbedBufferExplorer( pvTabBufferObserver , pvKeymapObserver , pvAutocmdObserver ):
    def __init__( self , target_win ):
        self.__target_win = target_win


        _logger.debug('TabbedBufferExplorer::__init__() make tab buffer')
        self.__buffer = pvTabBuffer()
        _logger.debug('TabbedBufferExplorer::__init__() register self to tabbuffer observer')
        self.__buffer.registerObserver( self )

        self.__key_event = []
        self.__key_event.append( pvKeymapEvent( "<F5>" , PV_KM_MODE_NORMAL , self.__buffer ) )
        self.__key_event.append( pvKeymapEvent( "D" , PV_KM_MODE_NORMAL , self.__buffer ) )

        self.__auto_event = []
        self.__auto_event.append( pvAutocmdEvent( 'BufEnter' , '*' ) )
        self.__auto_event.append( pvAutocmdEvent( 'BufDelete' , '*') )

        #register event
        for event in self.__key_event: pvKeymapManager.registerObserver( event , self )
        for event in self.__auto_event : pvAutocmdManager.registerObserver( event , self )


    def destroy( self ):
        #unregister event
        for event in self.__auto_event : pvAutocmdManager.removeObserver( event , self )
        for event in self.__key_event: pvKeymapManager.removeObserver( event , self )
        self.__buffer.removeObserver( self )
        # remove observer
        self.__buffer.wipeout()



    def analyzeBufferInfo( self ):
        _logger.debug('TabbedBufferExplorer::analyzeBufferInfo()')
        # get main window buffer
        buf_no = self.__target_win.bufferid
        update_selection = 0

        # init the buffer info
        self.__buffer.items = []
        buffer_format = '%(bufferid)3d|%(buffername)s'

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

    def showBuffer( self , show_win ):
        _logger.debug('TabbedBufferExplorer::show()')
        self.__buffer.showBuffer( show_win )
        self.__buffer.updateBuffer( selection = self.analyzeBufferInfo() , notify = False )
        self.__target_win.setFocus()


    def OnSelectTabChanged( self , item ):
        _logger.debug('TabbedBufferExplorer::OnSelectTabChanged()')
        try :
            buffer_id = int( re.match('^(?P<id>\s*\d+)\|.*$' , item.MultibyteString ).group('id') )
        except:
            # not find valid buffer id, just do nothing
            return

        # buffer show at main window is just the buffer to show, do
        # nothing
        if buffer_id == self.__target_win.bufferid: 
            self.__target_win.setFocus()
            return

        # show the buffer on main panel
        show_buffer = pvBuffer( PV_BUF_TYPE_ATTACH )
        show_buffer.attach( buffer_id )
        show_buffer.showBuffer( self.__target_win )

        self.__target_win.setFocus()

        # sync the cwd
        if show_buffer.name != None :
            dir_path , file_name = os.path.split( show_buffer.name )
            if os.path.isdir( dir_path ): os.chdir( dir_path )


    def OnHandleKeymapEvent( self , **kwdict ):
        _logger.debug('TabbedBufferExplorer::OnHandleKeymapEvent()')
        if kwdict['key'] == '<F5>':
            self.__buffer.updateBuffer( selection = self.analyzeBufferInfo() , notify = False )
        elif kwdict['key'] == 'D' :
            # on buffer , can't delete it
            if len ( self.__buffer.items ) == 1: return
            # check if select a valid item
            current_item_index = self.__buffer.searchIndexByCursor()
            if current_item_index == -1 : return
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

            self.__buffer.updateBuffer( selection = after_selection , notify = False )


    def OnHandleAutocmdEvent( self , **kwdict ):
        _logger.debug('TabbedBufferExplorer::OnHandleAutocmdEvent()')
        if ( kwdict['event'] == 'bufenter' and self.__target_win == pvWindow() )\
                or kwdict['event'] == 'bufdelete' :
                self.__buffer.updateBuffer( selection = self.analyzeBufferInfo() , notify = False )

            





