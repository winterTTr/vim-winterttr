import vim
from pyVim.pvWrap import pvWindowManager , pvWindow
from pyVim.pvExBuffer import pvListBuffer

from pyVim.pvKeyMapManager import pvKeyMapManager
from pyVim.pvKeyMapManager import PV_KMM_MODE_INSERT , PV_KMM_MODE_NORMAL

exVim_key_map_manager = pvKeyMapManager()
exVim_window_manager = pvWindowManager()

import re
re_match_last_word = re.compile( "(.*\W+|^)(?P<word>[\w_]+)$" )

class Application:
    def __init__( self ):
        self.panels_caption = ['content complete' , 'buffer list' , 'file explorer' ]
        self.panels = [ pvListBuffer() , pvListBuffer() , pvListBuffer() ]
        self.caption_buffer = pvListBuffer()

        self.initKeyMap()

    def initKeyMap( self ):
        exVim_key_map_manager.register( '<C-J>' , PV_KMM_MODE_INSERT , self.onMoveUpDown_Panel )
        exVim_key_map_manager.register( '<C-J>' , PV_KMM_MODE_NORMAL , self.onMoveUpDown_Panel )
        exVim_key_map_manager.register( '<C-K>' , PV_KMM_MODE_INSERT , self.onMoveUpDown_Panel )
        exVim_key_map_manager.register( '<C-K>' , PV_KMM_MODE_NORMAL , self.onMoveUpDown_Panel )

        exVim_key_map_manager.register( '<M-J>' , PV_KMM_MODE_NORMAL , self.onMoveUpDown_List )
        exVim_key_map_manager.register( '<M-K>' , PV_KMM_MODE_NORMAL , self.onMoveUpDown_List )

        exVim_key_map_manager.register( '<2-LeftMouse>' , PV_KMM_MODE_NORMAL , self.onDoubleClick_List )

        import string
        for letter in string.ascii_letters:
            exVim_key_map_manager.register( letter , PV_KMM_MODE_INSERT , self.onContentComplete )
        exVim_key_map_manager.register( '_' , PV_KMM_MODE_INSERT , self.onContentComplete )


    def start( self ):
        exVim_window_manager.makeWindows('( 30 , - )panel , ( -,10) list | (-,-)main ')

        defaul_selection = 0 
        self.caption_buffer.showBuffer( exVim_window_manager.getWindow('list') )
        self.caption_buffer.data = self.panels_caption
        self.caption_buffer.updateBuffer( selection = defaul_selection , resize = True )
        self.panels[defaul_selection].showBuffer( exVim_window_manager.getWindow('panel') )
        #self.panels[defaul_selection].data = [ '11' , '22' , '33' ]
        #self.panels[defaul_selection].updateBuffer( selection = 0 )


    def onMoveUpDown_Panel( self , key , mode ):
        buffer = self.panels[ self.caption_buffer.selection ]
        if isinstance( buffer , pvListBuffer ):
            if len( buffer.data) == 0 :
                return
            offset = 1 if key == "<C-J>" else -1
            buffer.updateBuffer(  selection = ( buffer.selection + offset ) % len( buffer.data )  )


    def onMoveUpDown_List( self , key , mode ):
        offset = 1 if key == "<M-J>" else -1
        buffer = self.caption_buffer
        buffer.updateBuffer( selection =  ( buffer.selection + offset ) % len( buffer.data )  )

        buffer_to_show = self.panels[ self.caption_buffer.selection ]
        buffer_to_show.showBuffer( exVim_window_manager.getWindow('panel') )
        buffer_to_show.updateBuffer()

    def onDoubleClick_List( self , key , mode ):
        current_win = pvWindow()
        if not current_win == exVim_window_manager.getWindow('list'):
            vim.command('normal viw')
            return

        # get selection position and update list
        cursor_line = vim.current.window.cursor[0]
        self.caption_buffer.updateBuffer( selection = cursor_line -1 )

        # update buffer
        buffer_to_show = self.panels[ self.caption_buffer.selection ]
        buffer_to_show.showBuffer( exVim_window_manager.getWindow('panel') )
        buffer_to_show.updateBuffer()


    def onContentComplete( self , key , mode ):
        if not pvWindow() == exVim_window_manager.getWindow('main'):
            return key
        
        # search base word
        cursor_line , cursor_column = vim.current.window.cursor
        line_left_cursor = vim.current.buffer[ cursor_line - 1 ][: cursor_column ] + str( key )
        word = re_match_last_word.match( line_left_cursor ).group('word')

        re_search_word = re.compile( '(?P<word>[\w_]*%s[\w_]*)' % word )

        search_set = set()
        for eachline in vim.current.buffer :
            for search_ret in re_search_word.finditer( eachline ):
                search_set.add(search_ret.group('word') )

        search_list = list(search_set)
        search_list.sort()

        vim.command('set noshowmode')
        print search_list

        return key

        

        
