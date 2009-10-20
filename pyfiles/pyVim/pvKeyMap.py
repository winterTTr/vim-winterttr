import vim
import urllib
import types
from pvWrap import CreateRandomName

# register the dispatch funciton for vim
vim.command( """
if !exists("*PV_KEY_MAP_DISPATCH")
    function PV_KEY_MAP_DISPATCH(appid,internal_key,vim_mode_flag)
      exec 'python pyVim.pvKeyMap.pvKeyMapDispatch("' .a:appid . '" , "'. a:internal_key . '","' . a:vim_mode_flag . '")'
      return @v
    endfunction
endif
""" )

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
        PV_KMM_MODE_NORMAL : 'nnoremap <silent> %(vim_key)s :call PV_KEY_MAP_DISPATCH("%(appid)s" , "%(internal_key)s" , "N")<CR>' ,
        PV_KMM_MODE_INSERT : 'inoremap <silent> %(vim_key)s <C-R>=PV_KEY_MAP_DISPATCH("%(appid)s" ,"%(internal_key)s" , "I")<CR>' , 
        PV_KMM_MODE_SELECT : 'snoremap <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(appid)s" ,"%(internal_key)s" , "S")<CR>' ,
        PV_KMM_MODE_VISUAL : 'xnoremap <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(appid)s" ,"%(internal_key)s" , "V")<CR>'
        }

# function used to dispatch all the key to call this registered py functions
def pvKeyMapDispatch( appid , internal_key , vim_mode ):
    vim.command('let @v=""')

    # call function
    ret = pvKeyMapManager( appid , False ).doKey( internal_key ,  pv_kmm_mode_map__vim_to_kmm[vim_mode] )
    if ret == None: ret = ""

    # set return value
    vim.command('let @v="%s"' % str(ret) ) 

class pvKeyName(object):
    def __init__( self ):
        self.vim_key = None

    def getVimKey( self ):
        return self.vim_key

    def setVimKey( self , key ):
        if key.find('<') != -1 and key.find('>') != -1 :
            self.vim_key = key.lower()
        else:
            self.vim_key = key

    vim_name = property( getVimKey , setVimKey )


    def setKMMKey( self , key ):
        self.vim_name =  urllib.unquote( key )

    def getKMMKey( self ):
        return urllib.quote( self.vim_key )

    internal_name = property( getKMMKey , setKMMKey )

    def __eq__( self , other ):
        if type( other ) in types.StringTypes :
            other_key = pvKeyName()
            other_key.vim_name = other
            return self.vim_name == other_key.vim_name

        if isinstance( other , pvKeyName ):
            return self.vim_name == other.vim_name

        return False

    def __str__( self ):
        return self.vim_name

class pvKeyMapResolver(object):
    def checkValidation( self , **kwdict ):
        return True
        
    def runAction( self ):
        raise NotImplementedError('pvKeyMapResolver::runAction')

class pvKeyMapManager(object):
    __internal_map = {}

    def __new__( cls , appid , create = True ):
        if ( not create ) or ( appid in cls.__internal_map ):
            return cls.__internal_map[appid]

        cls.__internal_map[appid] = object.__new__( cls )
        cls.__internal_map[appid].init( appid )
        return cls.__internal_map[appid]

    def init( self  , appid ):
        self.appid = appid
        self.call_function_map = {}
        for mode in pv_kmm_vim_keymap_command_map:
            self.call_function_map[mode] = {}

    def register( self , vim_key , kmm_mode , resolver ):
        key = pvKeyName()
        key.vim_name = vim_key

        vim.command( pv_kmm_vim_keymap_command_map[ kmm_mode ] % {
            'appid' : self.appid , 
            'vim_key' : key.vim_name , 
            'internal_key' : key.internal_name
            })

        self.call_function_map[kmm_mode][key.vim_name] = resolver


    def doKey( self , kmm_key , kmm_mode ):
        # make key
        kwdict = {}
        kwdict['key'] = pvKeyName()
        kwdict['key'].internal_name = kmm_key
        kwdict['mode'] = kmm_mode

        if kwdict['mode'] in [ PV_KMM_MODE_SELECT , PV_KMM_MODE_VISUAL ]:
            kwdict['range'] = [ vim.eval( 'getpos("%s")' % x )[1:3] for x in [ "'<" , "'>" ] ]

        resolver = self.call_function_map[kmm_mode][ kwdict['key'].vim_name ]
        if resolver.checkValidation( **kwdict ):
            return resolver.runAction()






