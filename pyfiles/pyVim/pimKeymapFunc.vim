let g:Pim_KeymapFunc_Dict = {}

python <<<EOF
from pimBase.pimKeymapManager import PimGlobalKeymapManager
EOF

function! Pim_KeymapFunc_Dict.InsertMode(internal_key,complete_mode) dict
    execute 'py PimGlobalKeymapManager.Dispatch("'. a:internal_key .'", KMM_KEY_MODE_INSERT )'
    if 0 ==  a:complete_mode
        return ""
    else
        return "\<C-P>"
    endif
endfunction
