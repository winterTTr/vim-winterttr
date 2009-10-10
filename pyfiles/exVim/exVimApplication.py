import vim
from pyVim.pvWrap import pvWindowManager , pvWindow
from pyVim.pvExBuffer import pvListBuffer

from pyVim.pvKeyMapManager import pvKeyMapManager
from pyVim.pvKeyMapManager import PV_KMM_MODE_INSERT , PV_KMM_MODE_NORMAL , PV_KMM_MODE_SELECT

exVim_key_map_manager = pvKeyMapManager()
exVim_window_manager = pvWindowManager()

import re
re_match_last_word = re.compile( "(.*\W+|^)(?P<word>[\w_]+)$" )

class Application:
    def __init__( self ):
        self.panels_caption = ['content complete' , 'buffer list' , 'file explorer' ]
        self.panels = [ pvListBuffer() , pvListBuffer() , pvListBuffer() ]
        self.caption_buffer = pvListBuffer()


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
        exVim_key_map_manager.register( '<backspace>' , PV_KMM_MODE_INSERT , self.onContentComplete )

        exVim_key_map_manager.register( '<C-Space>' , PV_KMM_MODE_INSERT , self.onReplaceWithSelection )
        exVim_key_map_manager.register( '<C-Space>' , PV_KMM_MODE_SELECT , self.onAcceptExtendWord )

    def start( self ):
        vim.command( 'set noshowmode' )
        exVim_window_manager.makeWindows('( 30 , - )panel , ( -,10) list | (-,-)main ')
        self.initKeyMap()

        defaul_selection = 0 
        self.caption_buffer.showBuffer( exVim_window_manager.getWindow('list') )
        self.caption_buffer.data = self.panels_caption
        self.caption_buffer.updateBuffer( selection = defaul_selection , resize = True )
        self.panels[defaul_selection].showBuffer( exVim_window_manager.getWindow('panel') )


    def onMoveUpDown_Panel( self , **kwdict ):
        buffer = self.panels[ self.caption_buffer.selection ]
        if isinstance( buffer , pvListBuffer ):
            if len( buffer.data) == 0 :
                return
            offset = 1 if kwdict['key'] == "<C-J>" else -1
            buffer.updateBuffer(  selection = ( buffer.selection + offset ) % len( buffer.data )  )


    def onMoveUpDown_List( self , **kwdict ):
        offset = 1 if kwdict['key'] == "<M-J>" else -1
        buffer = self.caption_buffer
        buffer.updateBuffer( selection =  ( buffer.selection + offset ) % len( buffer.data )  )

        buffer_to_show = self.panels[ self.caption_buffer.selection ]
        buffer_to_show.showBuffer( exVim_window_manager.getWindow('panel') )
        buffer_to_show.updateBuffer()

    def onDoubleClick_List( self , **kwdict ):
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


    def onContentComplete( self , **kwdict ):
        return_key = '\\' + str( kwdict['key'] ) if kwdict['key'] == '<Backspace>' else str ( kwdict['key'] )

        # check if the main window
        if not pvWindow() == exVim_window_manager.getWindow('main'):
            return return_key

        # check if the [content complete] panels is open
        if not self.panels[0].isShown(): return return_key
        
        # get line left cursor 
        cursor_line , cursor_column = vim.current.window.cursor
        line_left_cursor = vim.current.buffer[ cursor_line - 1 ][: cursor_column ] 
        # if input a valid letter , append it
        if not kwdict['key'] == '<Backspace>' :
            line_left_cursor += str( kwdict['key'] )

        try :
            base_word = re_match_last_word.match( line_left_cursor ).group('word')
        except:
            return return_key

        if kwdict['key'] == '<Backspace>' :
            word = base_word[:-1]
            remove_list = [ base_word ]
        else:
            word = base_word
            remove_list = []

        if len( word ) < 3 : return return_key

        # find the possible words

        def searchWord( re_search_str , decrease_list = [] ):
            search_dict = {}
            re_search = re.compile( re_search_str )
            for eachline in vim.current.buffer :
                for search_ret in re_search.finditer( eachline ):
                    find_word = search_ret.group('word')
                    search_dict.__setitem__( find_word , search_dict.get( find_word , 0 ) + 1 )

            for x in decrease_list :
                if search_dict.has_key( x ):
                    if search_dict[x] == 1 :
                        del search_dict[x]
                    else:
                        search_dict[x] -= 1
                        
            revert_dict = {}
            for key in search_dict.keys() :
                if revert_dict.has_key( search_dict[key] ):
                    revert_dict[ search_dict[key] ].append( key )
                else:
                    revert_dict[ search_dict[key] ] = [ key ]

            for key in revert_dict.keys():
                revert_dict[key].sort()

            return revert_dict

        ## search  start with the 'word'  and middle with
        search_dict__start_with = searchWord( '(?P<word>%s[\w_]+)' % word , remove_list )
        search_dict__middle_with = searchWord( '(?P<word>[\w_]+%s[\w_]*)' % word )

        # to list
        def searchDict2List( data_dict ):
            return_list = []
            key_list = data_dict.keys()
            key_list.sort( lambda x , y : x < y )
            for x in key_list :
                return_list.extend( data_dict[x] )
            return return_list

        self.panels[0].data = []
        self.panels[0].data.extend( searchDict2List( search_dict__start_with ) )
        if len (  self.panels[0].data ) == 1 :
            final_word = self.panels[0].data[0]
            add_len = len( final_word ) - len( word )
            if add_len == 1 :
                return_key = '\<C-W>%s\<C-O>v\<C-G>' %  final_word 
            else:
                return_key = '\<C-W>%s\<C-O>v%dh\<C-G>' % (  final_word , add_len - 1 )
            print final_word , word , add_len , return_key

        self.panels[0].data.extend( searchDict2List( search_dict__middle_with ) )
        self.panels[0].updateBuffer( selection = 0 )

        return return_key


    def onReplaceWithSelection( self , **kwdict ):
        complete_buffer = self.panels[0]

        # no data to complete
        if len( complete_buffer.data ) == 0 : return

        # valiable when inputting in the main panel
        if not pvWindow() == exVim_window_manager.getWindow('main'): return

        # valiable if the [content complete] panel is show
        if not complete_buffer.isShown() : return

        # delete word on cursor
        return ('\<C-W>%s' % complete_buffer.data[ complete_buffer.selection ] )

    def onAcceptExtendWord( self , **kwdict ):
        return ""
        
