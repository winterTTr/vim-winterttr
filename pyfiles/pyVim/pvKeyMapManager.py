import vim
import urllib
from pvWrap import CreateRandomName

pv_kmm_internal_register_table = {}

PV_KMM_MODE_INSERT = 0x01
PV_KMM_MODE_NORMAL = 0x02

VIM_KEY_MAP_REG_FUNCTION = """
let g:%(return_var)s = ""
function! %(function_name)s(internal_key,mode)
  exec 'python pyVim.pvKeyMapManager.kmmDispatch("%(function_name)s" , "'. a:internal_key . '","' . a:mode . '")'
  return g:%(return_var)s
endfunction
"""

def kmmDispatch( id , internal_key , mode ):
    vim.command('let g:%s=""' % ( pv_kmm_internal_register_table[id].ret_var ) )
    ret = pv_kmm_internal_register_table[id].doKey( internal_key , mode )
    if ret == None: ret = ""
    vim.command('let g:%s="%s"' % ( pv_kmm_internal_register_table[id].ret_var , str(ret) ) ) 

class pvKeyMapManager:
    def __init__( self ):
        self.id = CreateRandomName('KMM_FUNCTION')
        self.ret_var = self.id + '_RET'

        vim.command( VIM_KEY_MAP_REG_FUNCTION % {
            'function_name' : self.id ,
            'return_var' : self.ret_var } )

        pv_kmm_internal_register_table[self.id] =  self

        self.key_map = {}
        self.key_map[PV_KMM_MODE_INSERT] = {}
        self.key_map[PV_KMM_MODE_NORMAL] = {}



    def release( self ):
        del pv_kmm_internal_register_table[self.id]


    def register( self , vim_key , mode , py_function ):
        internal_key = urllib.quote( vim_key )
        if mode == PV_KMM_MODE_INSERT :
            command_format = 'inoremap <silent> %(key)s <C-R>=%(function_name)s("%(internal_key)s" , "I")<CR>'
        elif mode == PV_KMM_MODE_NORMAL :
            command_format = 'nnoremap <silent> %(key)s :call %(function_name)s("%(internal_key)s" , "N")<CR>'
        else:
            raise RuntimeError( 'invalid kmm mode' )

        vim.command( command_format % {
            'key' : vim_key ,
            'function_name' : self.id , 
            'internal_key' : internal_key
            })

        self.key_map[mode][internal_key] = py_function


    def doKey( self , internal_key , mode ):
        vim_key = urllib.unquote(internal_key)
        mode = { 'I' : PV_KMM_MODE_INSERT ,
                 'N' : PV_KMM_MODE_NORMAL }[mode]
        return self.key_map[mode][internal_key]( vim_key , mode )






