import vim
import urllib
import types
from pvWrap import GenerateRandomName

# register the dispatch funciton for vim
vim.command( """
if !exists("*PV_KEY_MAP_DISPATCH")
    function PV_KEY_MAP_DISPATCH(appid,uid)
      exec 'python pyVim.pvKeyMap.pvKeyMapDispatch("' .a:appid . '" , "'. a:uid . '")'
      return @v
    endfunction
endif
""" )

# possible mode for the key map
PV_KMM_MODE_INSERT  = 0x01
PV_KMM_MODE_NORMAL  = 0x02
PV_KMM_MODE_SELECT  = 0x04
PV_KMM_MODE_VISUAL  = 0x08


pv_kmm_vim_keymap_command_map = {
        PV_KMM_MODE_NORMAL : 'nnoremap <silent> %(vim_key)s :call PV_KEY_MAP_DISPATCH("%(appid)s" , "%(uid)s" )<CR>' ,
        PV_KMM_MODE_INSERT : 'inoremap <silent> %(vim_key)s <C-R>=PV_KEY_MAP_DISPATCH("%(appid)s" ,"%(uid)s" )<CR>' , 
        PV_KMM_MODE_SELECT : 'snoremap <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(appid)s" ,"%(uid)s")<CR>' ,
        PV_KMM_MODE_VISUAL : 'xnoremap <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(appid)s" ,"%(uid)s")<CR>'
        }

pv_kmm_vim_buffered_keymap_command_map = {
        PV_KMM_MODE_NORMAL : 'nnoremap <buffer> <silent> %(vim_key)s :call PV_KEY_MAP_DISPATCH("%(appid)s" , "%(uid)s" )<CR>' ,
        PV_KMM_MODE_INSERT : 'inoremap <buffer> <silent> %(vim_key)s <C-R>=PV_KEY_MAP_DISPATCH("%(appid)s" ,"%(uid)s" )<CR>' , 
        PV_KMM_MODE_SELECT : 'snoremap <buffer> <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(appid)s" ,"%(uid)s")<CR>' ,
        PV_KMM_MODE_VISUAL : 'xnoremap <buffer> <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(appid)s" ,"%(uid)s")<CR>'
        }
# function used to dispatch all the key to call this registered py functions
def pvKeyMapDispatch( appid , uid ):
    vim.command('let @v=""')

    # call function
    ret = pvKeyMapManager( appid , False ).doKey( uid )
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

    def register( self , vim_key , kmm_mode , resolver , buffer = None ):
        key = pvKeyName()
        key.vim_name = vim_key

        # register the python method to internal map
        uid = "%(keyname)s:%(mode)d:%(bufferid)d" % {
                'keyname' : key.internal_name , 
                'mode'    : kmm_mode , 
                'bufferid': buffer.id if buffer else 0 }
        self.call_function_map[uid] = resolver

        vim_cmd_format = pv_kmm_vim_keymap_command_map if buffer == None else pv_kmm_vim_buffered_keymap_command_map
        vim_cmd = vim_cmd_format[ kmm_mode ] % {
                'vim_key' : key.vim_name , 
                'appid' : self.appid , 
                'uid' : uid
            }

        if buffer : # <buffer> map
            buffer.registerCommand( vim_cmd )
        else: # global map
            vim.command( vim_cmd )



    def doKey( self , uid ):
        # analyze the uid
        internal_key , mode , bufferid = uid.split(':')
        mode , bufferid = map( int , [ mode , bufferid ] ) # convert to int

        # make key
        kwdict = {}
        kwdict['key'] = pvKeyName()
        kwdict['key'].internal_name = internal_key
        kwdict['mode'] = mode
        if bufferid != 0 :
            kwdict['bufferid'] = bufferid

        if kwdict['mode'] in [ PV_KMM_MODE_SELECT , PV_KMM_MODE_VISUAL ]:
            kwdict['range'] = [ vim.eval( 'getpos("%s")' % x )[1:3] for x in [ "'<" , "'>" ] ]

        resolver = self.call_function_map[ uid ]
        if resolver.checkValidation( **kwdict ):
            return resolver.runAction()






