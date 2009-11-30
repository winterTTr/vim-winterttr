import vim
import urllib
import types

import logging
_logger = logging.getLogger('pyVim.pvAutoCmd')

vim.command("""
augroup PYVIM_AUTOCOMMAND
augroup END""")

_command_format = 'autocmd PYVIM_AUTOCOMMAND %(event)s %(pat)s py pyVim.pvAutocmd.pvAUManager.notifyObserver("%(uid)s")'


class pvAUEvent(object):
    def __init__( self , event = None, pattern = None ):
        if event == None and pattern == None :
            self.__uid = None
            return

        self.__uid = "%(event)s:%(pat)s" % {
                'event' : event.lower() , 
                'pat'   : urllib.quote( pattern ) }

    @property
    def uid( self ):
        return self.__uid

    @uid.setter
    def uid( self , uid ):
        self.__uid = uid

    @property
    def event( self ):
        event , pat = self.__uid.split(':')
        return event

    @property
    def pattern( self ):
        event , pat = self.__uid.split(':')
        return urllib.unquote( pat )

class pvAUObserver(object):
    def OnHandleAUEvent( self , **kwdict ):
        raise NotImplementedError('pvAUObserver::OnHandleAUEvent')
        

class pvAUManager(object):
    __ob_register = {}

    @staticmethod
    def registerObserver( event , ob ):
        command = _command_format % {
                'event' : event.event,
                'pat'   : event.pattern,
                'uid'   : event.uid
                }
        vim.command( command )

        pvAUManager.__ob_register[ event.uid ] = pvAUManager.__ob_register.get( event.uid , [] )
        pvAUManager.__ob_register[ event.uid ].append( ob )


    @staticmethod
    def notifyObserver( uid ):
        if not uid in pvAUManager.__ob_register:
            _logger.debug('pvAUManager::notifyObserver() no key for event[%s], do nothing.' % uid )
            return

        event = pvAUEvent()
        event.uid = uid
        kwdict = {}
        kwdict['event'] = event.event
        kwdict['pattern'] = event.pattern
        _logger.debug('pvAUManager::notifyObserver() make param[%s]' % str( kwdict ) ) 

        vim.command( 'set eventignore=all' )
        try :
            for ob in pvAUManager.__ob_register[uid] :
                ob.OnHandleAUEvent( **kwdict )
        finally:
            vim.command( 'set eventignore=')


    @staticmethod
    def removeObserver( event , ob ):
        # no slot for the event , just return
        if not event.uid in pvAUManager.__ob_register:
            return 

        try :
            pvAUManager.__ob_register[ event.uid ].remove( ob )
        except:
            # not register
            return

        # clear the slot if no ob in it
        if pvAUManager.__ob_register[ event.uid ] is [] :
            del pvAUManager.__ob_register[ event.uid ]



