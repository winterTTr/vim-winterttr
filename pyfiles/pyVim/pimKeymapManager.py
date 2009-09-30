import vim

KMM_KEY_MODE_NORMAL = 0x01
KMM_KEY_MODE_INSERT = 0x02


pim_keymap_dispatcher_init = """

let g:Pim_KeymapFunc_Dict = {}

function! Pim_KeymapFunc_Dict.InsertMode(internal_key,complete_mode) dict
    execute 'py PimGlobalKeymapManager.Dispatch("'. a:internal_key .'",' . complete_mode .')'
    if 0 ==  a:complete_mode
        return ""
    else
        return "\<C-P>"
    endif
endfunction
"""

vim.command( functionStr )

class PimKeymapManager:
    def __init__(self):
        self.buflist = []

        # register global key map function
        vim.command( pim_keymap_dispatcher__insert )

    def Dispatch( keyStr , mode ):
        bufferId = int( vim.eval('bufnr("%")') ) 

    def RegisterKey( vimKeyName , vimKeyMode ):
        import re
        matchObj = re.match('\<(?P<internal_key>.*)\>' , vimKeyName )
        if not matchObj:
            raise "Invalid keymap , should be like <c-n>"

        internalKeyname = matchObj.group('internal_key')
        keymapCmd = 'nnoremap <buffer> %s :py global_keymap_manager.RunKeymap("%s")<CR>' % ( vimKeyname , internalKeyname)
        vim.command(keymapCmd)





PimGlobalKeymapManager = PimKeymapManager()




