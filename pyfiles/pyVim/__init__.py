import logging
import logging.config
import os
import vim

# make the log path
if 'PYVIM_LOG_PATH' in os.environ:
    logging.PYVIM_LOG_PATH=os.environ['PYVIM_LOG_PATH']
else:
    logging.PYVIM_LOG_PATH=os.path.join( os.path.expanduser("~") , 'pyvim.log' )

logging.config.fileConfig( os.path.join( os.path.split( __file__ )[0] , 'pvLogging.ini') )

