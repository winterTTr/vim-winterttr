import vim


def VimConfirm( prompt , choices = [] , default = 1 , type = "Generic" ):
    choicesStr = map( lambda x : str(x) , choices )
    command = 'confirm("' + prompt + '","' + '\\n'.join( choicesStr ) + '",' + str( default ) + ',"' + type + '")' 
    selection = int( vim.eval( command ) )
    if selection == 0 :
        return None
    return choices[ selection -1 ]
