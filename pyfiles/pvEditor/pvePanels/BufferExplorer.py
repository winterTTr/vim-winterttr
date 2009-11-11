import vim

from _PanelBase_ import PanelBase

from pyVim.pvListBuffer import pvListBuffer , pvListBufferObserver
from pyVim.pvUtil import pvString



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
        buffer_format = '%(bufferid)3d|%(buffername)s'

        buffer_count = int( vim.eval("bufnr('$')") )
        for index in xrange( buffer_count ):
            buffer_id = index + 1
            if vim.eval("bufexists(%d)" % buffer_id ) != '0' :
                is_listed = vim.eval('getbufvar(%d,"&buflisted")' % buffer_id ) != '0'
                str = pvString()
                str.MultibyteString = buffer_format % {
                        'bufferid' : buffer_id ,
                        'buffername' : vim.eval('bufname(%d)' % buffer_id ) }
                self.__buffer.items.append( str )

                #is_modifiable = vim.eval('getbufvar(%d,"&modifiable")' % buffer_id ) != '0'
                #is_readonly = vim.eval('getbufvar(%d,"&readonly")' % buffer_id ) != '0'

    def OnSelectItemChanged( self , item ):
        pass





