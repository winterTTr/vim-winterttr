import vim
import urllib
import types

# register the dispatch funciton for vim
vim.command( """
if !exists("*PV_KEY_MAP_DISPATCH")
    function PV_KEY_MAP_DISPATCH(uid)
      exec 'python pyvim.pvKeyMap.pvKeyMapManager.notifyObserver("'. a:uid . '")'
      return @v
    endfunction
endif
""" )

# possible mode for the key map
PV_KM_MODE_INSERT  = 0x01
PV_KM_MODE_NORMAL  = 0x02
PV_KM_MODE_SELECT  = 0x04
PV_KM_MODE_VISUAL  = 0x08


pv_km_vim_keymap_command_map = {
        PV_KM_MODE_NORMAL : 'nnoremap <silent> %(vim_key)s :call PV_KEY_MAP_DISPATCH("%(uid)s" )<CR>' ,
        PV_KM_MODE_INSERT : 'inoremap <silent> %(vim_key)s <C-R>=PV_KEY_MAP_DISPATCH("%(uid)s" )<CR>' , 
        PV_KM_MODE_SELECT : 'snoremap <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(uid)s")<CR>' ,
        PV_KM_MODE_VISUAL : 'xnoremap <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(uid)s")<CR>'
        }

pv_km_vim_buffered_keymap_command_map = {
        PV_KM_MODE_NORMAL : 'nnoremap <buffer> <silent> %(vim_key)s :call PV_KEY_MAP_DISPATCH("%(uid)s" )<CR>' ,
        PV_KM_MODE_INSERT : 'inoremap <buffer> <silent> %(vim_key)s <C-R>=PV_KEY_MAP_DISPATCH("%(uid)s" )<CR>' , 
        PV_KM_MODE_SELECT : 'snoremap <buffer> <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(uid)s")<CR>' ,
        PV_KM_MODE_VISUAL : 'xnoremap <buffer> <silent> %(vim_key)s <ESC>`>a<C-R>=PV_KEY_MAP_DISPATCH("%(uid)s")<CR>'
        }

class pvKeyName(object):
    def __init__( self ):
        self.vim_key = None

    @property
    def vim_name( self ):
        return self.vim_key

    @vim_name.setter
    def vim_name( self , key ):
        if key.find('<') != -1 and key.find('>') != -1 :
            self.vim_key = key.lower()
        else:
            self.vim_key = key

    @property
    def internal_name( self ):
        return urllib.quote( self.vim_key )

    @internal_name.setter
    def internal_name( self , key ):
        self.vim_name =  urllib.unquote( key )

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


class pvKeyMapEvent(object):
    def __init__( self , key = None , mode = None , buffer = None ):
        if key == None and mode == None:
            self.__uid = None
            return

        _key = pvKeyName()
        _key.vim_name = key

        self.__buffer = buffer
        # register the python method to internal map
        self.__uid = "%(keyname)s:%(mode)d:%(bufferid)d" % {
                'keyname' : _key.internal_name , 
                'mode'    : mode , 
                'bufferid': buffer.id if buffer else 0 }

    @property
    def uid( self ):
        return self.__uid

    @uid.setter
    def uid( self , uid ):
        self.__uid = uid 

    @property
    def key( self ):
        internal_key , mode , bufferid = self.__uid.split(':')

        _key = pvKeyName()
        _key.internal_name = internal_key
        return _key

    @property
    def mode( self ):
        internal_key , mode , bufferid = self.__uid.split(':')
        return int(mode)

    @property
    def bufferid( self ):
        internal_key , mode , bufferid = self.__uid.split(':')
        return int(bufferid)

    @property
    def buffer( self ):
        return self.__buffer





class pvKeyMapObserver(object):
    def OnHandleKeyEvent( self , **kwdict ):
        raise NotImplementedError('pvKeyMapObserver::OnHandleKeyEvent')




class pvKeyMapManager(object):
    __ob_register = {}

    @staticmethod
    def registerObserver( event , ob ):
        # if not exist, create the item, register the command
        pvKeyMapManager.__ob_register[ event.uid ] = pvKeyMapManager.__ob_register.get( event.uid , [] )
        vim_cmd_format = pv_km_vim_keymap_command_map if event.buffer == None else pv_km_vim_buffered_keymap_command_map
        vim_cmd = vim_cmd_format[ event.mode ] % {
                'vim_key' : event.key.vim_name , 
                'uid' : event.uid
                }

        if event.buffer : # <buffer> map
            event.buffer.registerCommand( vim_cmd , True )
        else: # global map
            vim.command( vim_cmd )

        pvKeyMapManager.__ob_register[event.uid].append( ob )

    @staticmethod
    def notifyObserver( uid ):
        event = pvKeyMapEvent()
        event.uid = uid

        # make key
        kwdict = {}
        kwdict['key'] = event.key
        kwdict['mode'] = event.mode

        bufferid = event.bufferid
        if bufferid != 0 :
            kwdict['bufferid'] = bufferid

        if kwdict['mode'] in [ PV_KM_MODE_SELECT , PV_KM_MODE_VISUAL ]:
            kwdict['range'] = [ vim.eval( 'getpos("%s")' % x )[1:3] for x in [ "'<" , "'>" ] ]


        # clear the return register
        vim.command('let @v=""')
        for ob in pvKeyMapManager.__ob_register[uid]:
            ret = ob.OnHandleKeyEvent( **kwdict )
            if ret != None :
                # set return value
                vim.command('let @v="%s"' % str(ret) )

    @staticmethod
    def removeObserver( event , ob ):
        # no slot for the event , just return
        if not event.uid in pvKeyMapManager.__ob_register:
            return 

        try :
            pvKeyMapManager.__ob_register[ event.uid ].remove( ob )
        except:
            # not register
            return

        # clear the slot if no ob in it
        if pvKeyMapManager.__ob_register[ event.uid ] is [] :
            del pvKeyMapManager.__ob_register[ event.uid ]





