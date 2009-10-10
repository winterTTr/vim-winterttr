import vim
import urllib
import types
from pvWrap import CreateRandomName

pv_kmm_internal_register_table = {}

# register the function with a internal name
PV_VIM_KEY_MAP_REG_FUNCTION = """
let g:%(return_var_name)s = ""
function! %(function_name)s(internal_key,vim_mode_flag)
  exec 'python pyVim.pvKeyMapManager.kmmDispatch("%(id)s" , "'. a:internal_key . '","' . a:vim_mode_flag . '")'
  return g:%(return_var_name)s
endfunction
"""

# possible mode for the key map
PV_KMM_MODE_INSERT  = 0x01
PV_KMM_MODE_NORMAL  = 0x02
PV_KMM_MODE_SELECT  = 0x04
PV_KMM_MODE_VISUAL  = 0x08

pv_kmm_mode_map__vim_to_kmm = {
        'I' : PV_KMM_MODE_INSERT , 
        'N' : PV_KMM_MODE_NORMAL , 
        'S' : PV_KMM_MODE_SELECT ,
        'V' : PV_KMM_MODE_VISUAL 
        }

pv_kmm_mode_map__kmm_to_vim = {
        PV_KMM_MODE_INSERT : 'I' ,
        PV_KMM_MODE_NORMAL : 'N' , 
        PV_KMM_MODE_SELECT : 'S' ,
        PV_KMM_MODE_VISUAL : 'V' 
        }

pv_kmm_vim_keymap_command_map = {
        PV_KMM_MODE_NORMAL : 'nnoremap <silent> %(vim_key)s :call %(function_name)s("%(internal_key)s" , "N")<CR>' ,
        PV_KMM_MODE_INSERT : 'inoremap <silent> %(vim_key)s <C-R>=%(function_name)s("%(internal_key)s" , "I")<CR>' , 
        PV_KMM_MODE_SELECT : 'snoremap <silent> %(vim_key)s <ESC>`>a<C-R>=%(function_name)s("%(internal_key)s" , "S")<CR>' ,
        PV_KMM_MODE_VISUAL : 'xnoremap <silent> %(vim_key)s <ESC>`>a<C-R>=%(function_name)s("%(internal_key)s" , "V")<CR>'
        }

# function used to dispatch all the key to call this registered py functions
def kmmDispatch( id , kmm_key , vim_mode ):
    vim.command('let g:%s=""' % ( pv_kmm_internal_register_table[id].return_var_name ) )

    # call function
    ret = pv_kmm_internal_register_table[id].doKey( kmm_key ,  pv_kmm_mode_map__vim_to_kmm[vim_mode] )
    if ret == None: ret = ""

    # set return value
    vim.command('let g:%s="%s"' % ( pv_kmm_internal_register_table[id].return_var_name , str(ret) ) ) 

class pvkmmKeyName:
    def __init__( self ):
        self.vim_key = None

    def setVimKey( self , key ):
        if key.find('<') != -1 and key.find('>') != -1 :
            self.vim_key = key.lower()
        else:
            self.vim_key = key

    def getVimKey( self ):
        return self.vim_key

    def setKMMKey( self , key ):
        self.setVimKey ( urllib.unquote( key ) )

    def getKMMKey( self ):
        return urllib.quote( self.vim_key )

    def __eq__( self , other ):
        if type( other ) in types.StringTypes :
            other_key = pvkmmKeyName()
            other_key.setVimKey( other )
            return self.vim_key == other_key.vim_key

        if isinstance( other , pvkmmKeyName ):
            return self.vim_key == other.vim_key

        return False

    def __str__( self ):
        return self.vim_key
        

class pvKeyMapManager:
    def __init__( self ):
        self.id = CreateRandomName('KMM')

        self.function_name = self.id + '_FUNCTION'
        self.return_var_name = self.id + '_RET'

        vim.command( PV_VIM_KEY_MAP_REG_FUNCTION % {
            'id' : self.id , 
            'function_name' : self.function_name ,
            'return_var_name' : self.return_var_name } )

        pv_kmm_internal_register_table[self.id] =  self

        self.call_function_map = {}
        for mode in pv_kmm_vim_keymap_command_map.keys() :
            self.call_function_map[mode] = {}

    def release( self ):
        del pv_kmm_internal_register_table[self.id]


    def register( self , vim_key , kmm_mode , py_function ):
        if type( vim_key ) in types.StringTypes :
            key = pvkmmKeyName()
            key.setVimKey( vim_key )
        else :
            raise RuntimeError( 'not invalid key type' )

        try :
            command_format = pv_kmm_vim_keymap_command_map[ kmm_mode ]
        except:
            raise RuntimeError( 'invalid kmm mode' )

        vim.command( command_format % {
            'vim_key' : key.getVimKey() , 
            'function_name' : self.function_name , 
            'internal_key' : key.getKMMKey()
            })

        self.call_function_map[kmm_mode][key.getVimKey()] = py_function


    def doKey( self , kmm_key , kmm_mode ):
        # make key
        kwdict = {}
        kwdict['key'] = pvkmmKeyName()
        kwdict['key'].setKMMKey( kmm_key ) 
        kwdict['mode'] = kmm_mode

        if kwdict['mode'] in [ PV_KMM_MODE_SELECT , PV_KMM_MODE_VISUAL ]:
            kwdict['range'] = [ vim.eval( 'getpos("%s")' % x )[1:3] for x in [ "'<" , "'>" ] ]

        return self.call_function_map[kmm_mode][kwdict['key'].getVimKey()]( **kwdict )






