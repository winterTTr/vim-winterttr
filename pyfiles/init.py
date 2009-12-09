import vim
import sys
import os

pyfiles_basepath = vim.eval('g:pyfiles_basepath')
sys.path.append( pyfiles_basepath )
load_list = os.listdir( pyfiles_basepath )

# load __base__ first
for eachdir in load_list :
    if not os.path.isdir( os.path.join( pyfiles_basepath , eachdir ) ):
        continue
    
    try:
        module = __import__( eachdir )
    except ImportError:
        continue
    globals()[eachdir] = module
    try :
        getattr( module , 'pyfilesInit' )()
    except:
        pass

del eachdir
del module
del pyfiles_basepath
del load_list
del sys
del os


