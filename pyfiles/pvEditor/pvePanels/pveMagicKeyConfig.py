MagicKeyConfig = {}
MagicKeyConfig['AutoFillRegion'] = {}
MagicKeyConfig['AutoFillRegion']['begin'] = '`<'
MagicKeyConfig['AutoFillRegion']['end'] = '>`'
MagicKeyConfig['AutoFillRegion']['region'] = "%(begin)s  %(end)s" % MagicKeyConfig['AutoFillRegion']


# Expand Template
MagicKeyExpandTemplate = {}

# all type file
MagicKeyExpandTemplate['_'] = {}
## _: get time      :time {{{2
def GetCurrentTime(): 
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
MagicKeyExpandTemplate['_']['time'] = GetCurrentTime  #}}}2


# cpp & c
MagicKeyExpandTemplate['cpp'] = {}
## cpp: main        :main {{{2
MagicKeyExpandTemplate['cpp']['main'] = """\
int main( int argc , char * argv[] )
{
%(region)s;
return 0;
}\
""" % MagicKeyConfig['AutoFillRegion'] #}}}2
## cpp: for         :for {{{2
MagicKeyExpandTemplate['cpp']['for'] = """\
for ( %(region)s ; %(region)s ; %(region)s )
{
%(region)s;
}\
""" % MagicKeyConfig['AutoFillRegion'] # }}}2
## cpp: switch      :switch {{{2
MagicKeyExpandTemplate['cpp']['switch'] = """\
switch( %(region)s )
{
case %(region)s :
%(region)s;
break;
case %(region)s :
%(region)s;
break;
case %(region)s :
%(region)s;
break;
default :
%(region)s;
break;
}\
""" % MagicKeyConfig['AutoFillRegion'] # }}}2
## cpp: while       :while {{{2
MagicKeyExpandTemplate['cpp']['while'] = """\
while( %(region)s )
{
%(region)s;
}\
""" % MagicKeyConfig['AutoFillRegion'] #}}}2
## cpp: if          :if {{{2
MagicKeyExpandTemplate['cpp']['if'] = """\
if ( %(region)s )
{
%(region)s;
}
else
{
%(region)s;
}\
""" % MagicKeyConfig['AutoFillRegion'] #}}}2
## cpp: define      :#d {{{2
MagicKeyExpandTemplate['cpp']['#d'] = """\
#define \
""" #}}}2
## cpp: include     :#i {{{2
MagicKeyExpandTemplate['cpp']['#i'] = """\
#include \
""" #}}}2
## cpp: define file :#df  {{{2
def MakeDefineForHeaderFile():
    import vim 
    filename = vim.eval('expand("%:t")')
    if filename == "" or filename == None:
        return ""
    define = filename.upper().replace('.','_')
    defineContext = """\
#ifndef %(define)s
#define %(define)s

%(region)s

#endif //%(define)s\
""" % { 'define' : define , 'region' : MagicKeyConfig['AutoFillRegion']['region'] }
    return defineContext
MagicKeyExpandTemplate['cpp']['#df'] = MakeDefineForHeaderFile # }}}2

