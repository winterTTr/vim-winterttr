if exists("loaded_pimBase")
    finish
else
    let loaded_pimBase = 1
endif


let g:pimBase = "D:\\work_spaces\\Project_Coding\\__TEST\\py__\\google_svn\\PIM"


let s:gtl=&guitablabel
function PimDynamicTabLabel()
    let l:gtl=s:gtl
    let l:title=""
    if exists('t:pimTitle')
        let l:title=t:pimTitle
    else
        let l:title=l:gtl
    endif
    return l:title
endfunction
set guitablabel=%{PimDynamicTabLabel()}
