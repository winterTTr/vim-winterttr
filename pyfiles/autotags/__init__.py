import vim
from ATExport import LoadConfig , ResetConfig , UpdateTags , RegisterLoader , DoCommand

# pyfiles auto loaded
def pyfilesInit():
    vim.command('command! -nargs=0 Autotags py autotags.DoCommand()')
    #from ATTypeCPP import ATTypeCPP
    import ATTypeCPP
    RegisterLoader( ATTypeCPP.ATTypeCPP() )


