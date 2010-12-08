import _winreg
import os
import stat

def checkBinaryValidation( file_path ):
    try:
        mode = os.stat( file_path )[stat.ST_MODE]
        if stat.S_IMODE( mode ) == 511:
            return True
    except:
        return False


# search gvim.exe
vim_bin_path = None
dir_list = os.environ['PATH'].split(';')
dir_list.append( os.path.join( os.path.pardir , "bin"  ) )

for each_path in dir_list:
    test_path = os.path.abspath( os.path.join( each_path , "gvim.exe" ) )
    if checkBinaryValidation( test_path ):
        vim_bin_path = test_path
        break
else:
    print "Cannot find gvim.exe!"
    import sys
    sys.exit(0)

full_param_bin = "\"%s\"" % vim_bin_path 
full_param_bin += " --servername EXPLORER_VIM --remote-silent \"%L\"" 

# create: HKEY_CLASSES_ROOT\*\shell\open with gVim...
with _winreg.CreateKey( _winreg.HKEY_CLASSES_ROOT , "*\\shell\\Open with gVim...\\command" ) as handle:
    _winreg.SetValue( handle , "" , _winreg.REG_SZ , full_param_bin )
