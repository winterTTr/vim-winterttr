import vim
import os
import re

from _PanelBase_ import PanelBase

from pyVim.pvListBuffer import pvListBuffer , pvListBufferObserver
from pyVim.pvUtil import pvString

from pyVim.pvWrap import pvBuffer , PV_BUF_TYPE_ATTACH



class _class_( PanelBase , pvListBufferObserver ):
    def __init__( self , win_mgr ):
        self.__win_mgr = win_mgr

        self.__buffer = pvListBuffer()
        self.__buffer.registerObserver( self )

        self.__name = u"Buffer Explorer"

    # from |PanelBase|
    def OnName( self ):
        str = pvString()
        str.UnicodeString = self.__name
        return str

    def OnPanelSelected( self , item ):
        if item.UnicodeString != self.__name :
            return

        self.__buffer.showBuffer( self.__win_mgr.getWindow('panel') )
        self.analyzeBufferInfo()
        self.__buffer.updateBuffer()


    def analyzeBufferInfo( self ):
        self.__buffer.items = []
        buffer_format = '%(bufferid)3d|[%(buffername)s]%(modifymark)1s'

        buffer_count = int( vim.eval("bufnr('$')") )
        for index in xrange( buffer_count ):
            if vim.eval("bufexists(%d)" % ( index +1 , ) ) != '0' :
                # buffer id
                buffer_id = index + 1
                # buffer_name
                buffer_name = vim.eval('bufname(%d)' % buffer_id )
                buffer_name = buffer_name if buffer_name else "<NO NAME>"
                buffer_basename = os.path.basename( buffer_name )
                # property 
                is_listed = vim.eval('getbufvar(%d,"&buflisted")' % buffer_id ) != '0'
                is_modifiable = vim.eval('getbufvar(%d,"&modifiable")' % buffer_id ) != '0'
                is_readonly = vim.eval('getbufvar(%d,"&readonly")' % buffer_id ) != '0'
                is_modified = vim.eval('getbufvar(%d,"&modified")' % buffer_id ) != '0'

                if is_listed :
                    str = pvString()
                    str.MultibyteString = buffer_format % {
                            'bufferid' : buffer_id ,
                            'buffername' : buffer_basename , 
                            'modifymark' : '*' if is_modified else ' ' }
                    self.__buffer.items.append( str )


    def OnSelectItemChanged( self , item ):
        try :
            buffer_id = int( re.match('^(?P<id>\s*\d+)\|.*$' , item.MultibyteString ).group('id') )
        except:
            return

        show_buffer = pvBuffer( PV_BUF_TYPE_ATTACH )
        show_buffer.attach( buffer_id )
        show_buffer.showBuffer( self.__win_mgr.getWindow('main') )



