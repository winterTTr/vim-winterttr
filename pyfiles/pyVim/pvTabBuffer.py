import vim
import re


from pvWrap import pvBuffer
from pvWrap import GenerateRandomName
from pvWrap import PV_BUF_TYPE_READONLY , PV_BUF_TYPE_NORMAL

from pvKeyMap import pvKeyMapEvent , pvKeyMapObserver , pvKeyMapManager
from pvKeyMap import PV_KM_MODE_NORMAL


import logging
_logger = logging.getLogger('pyVim.pvTabBuffer')


class pvTabBufferObserver(object):
    def OnSelectTabChanged( self , item ):
        raise NotImplementedError("pvTabBufferObserver::OnSelectTabChanged")


class pvTabBuffer( pvBuffer , pvKeyMapObserver ):
    def __init__( self ):
        _logger.debug('pvTabBuffer::__init__() create buffer')
        super( pvTabBuffer , self ).__init__( PV_BUF_TYPE_READONLY , GenerateRandomName( 'PV_TABBUF_' ) )
        self.items = []
        self.selection = 0
        self.hilight = 'Visual'

        self.ob_list = []
        self.registerCommand( 'setlocal wrap')
        self.registerCommand( 'setlocal nonumber')
        self.registerCommand( 'setlocal nolinebreak' )
        self.registerCommand( 'setlocal foldcolumn=0')

        _logger.debug('pvTabBuffer::__init__() register DoubleClick event')
        db_click_event = pvKeyMapEvent( '<2-LeftMouse>' , PV_KM_MODE_NORMAL , self )
        pvKeyMapManager.registerObserver( db_click_event , self )

        _logger.debug('pvTabBuffer::__init__() register <Enter> event')
        enter_event = pvKeyMapEvent( '<Enter>' , PV_KM_MODE_NORMAL , self )
        pvKeyMapManager.registerObserver( enter_event , self )


    def registerObserver( self , ob ):
        self.ob_list.append( ob )

    def removeObserver( self , ob ):
        self.ob_list.remove( ob )

    def OnNotifyObserver( self ):
        if self.items :
            for ob in self.ob_list:
                ob.OnSelectTabChanged( self.items[self.selection] )

    def OnHandleKeyEvent( self , **kwdict ):
        _logger.debug('pvTabBuffer::OnHandleKeyEvent() refresh buffer')
        self.updateBuffer()

    def OnUpdate( self , **kwdict ):
        if 'selection' in kwdict:
            if self.items :
                self.selection = kwdict['selection'] % len( self.items )
            else:
                self.selection = 0
        else:
            # search item by position
            self.selection = self.searchIndexByCursor()
            if self.selection == -1:
                self.selection = 0
                return
        selection = self.selection


        # generate the data
        show_data_list = [ self.__makeTabItem( index , value ) for index , value in enumerate( self.items ) ]
        _logger.debug('pvTabBuffer::OnUpdate() show data[%s]' % str( show_data_list ) )
        self.buffer[0] = ' '.join( show_data_list )

        # hilight the item
        if len( show_data_list ) != 0 :
            hilight_str = show_data_list[self.selection]
            self.registerCommand('match %s /\V%s/' % ( 'Visual' ,  hilight_str ) )

        self.registerCommand( 'resize %d' % ( len ( self.buffer[0] ) / vim.current.window.width + 1 , ) ) 


    def __makeTabItem( self , index , value ):
        _format = "[%s]" if index == self.selection else "[%s]"
        return _format % ( value.MultibyteString , )


    def searchIndexByCursor( self ):
        if self.items is [] :
            return 0

        cursor_row = vim.current.window.cursor[1]
        search_item_re = re.compile( '\[.*?\]' )
        
        search_index = 0 
        for each in search_item_re.finditer( self.buffer[0] ):
            if each.start() <= cursor_row < each.end():
                return search_index
            search_index += 1
        else:
            return -1










