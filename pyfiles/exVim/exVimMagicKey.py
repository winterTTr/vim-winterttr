# standard module
import vim
import re
# pyVim module
from pyVim.pvKeyMap import pvKeyMapResolver , pvKeyMapManager
from pyVim.pvKeyMap import PV_KMM_MODE_INSERT , PV_KMM_MODE_NORMAL , PV_KMM_MODE_SELECT
from pyVim.pvWrap import pvWindow
from pyVim.pvListBuffer import pvListBuffer
# exVim
import exVimMagicKeyConfig 


class exVimMagicKeyBase( pvKeyMapResolver ):
    def register( self ):
        raise NotImplementedError( "exVimMagicKeyBase::register" )


class exVimKey_ExpandContent( exVimMagicKeyBase ):
    def __init__( self , main_window ):
        self.main_window = main_window

    def register( self ):
        from exVimConfig import appid
        kmm = pvKeyMapManager( appid )
        kmm.register( '<Tab>' , PV_KMM_MODE_INSERT , self )

    def checkValidation( self , **kdwcit ):
        return pvWindow() == self.main_window

    def runAction( self  ):
        # 1. try to expand keyword
        # 2. try to complete the function prototype
        # 3. try replace the region
        # 4. default , just return the Tab Key
        return self.__DoExpandKeyword() or self.__DoCompleteFunctionPrototype() or self.__DoFocusAutoFillRegion() or '\<Tab>'

    def __DoExpandKeyword( self ):
        # get left context accordding to the cursor position
        cursorRow , cursorCol = vim.current.window.cursor
        lineLeftCursor =  vim.current.line[:cursorCol]
        lineRightCursor = vim.current.line[cursorCol:]

        # make avaliable key list
        expandKeyList = exVimMagicKeyConfig.MagicKeyExpandTemplate['_'].keys()
        if exVimMagicKeyConfig.MagicKeyExpandTemplate.has_key( vim.eval('&ft') ) :
             expandKeyList.extend( exVimMagicKeyConfig.MagicKeyExpandTemplate[ vim.eval('&ft') ].keys() )

        regStr = "(.*\s+|^)(?P<key>" + '|'.join(expandKeyList) + ")$"
        regRet =  re.match( regStr , lineLeftCursor )
        if not regRet :
            return ""

        begin , end , key = regRet.start('key') , regRet.end('key') , regRet.group('key')
        expandObject = None
        if exVimMagicKeyConfig.MagicKeyExpandTemplate['_'].has_key( key):
            expandObject = exVimMagicKeyConfig.MagicKeyExpandTemplate['_'][key]
        else:
            expandObject = exVimMagicKeyConfig.MagicKeyExpandTemplate[vim.eval('&ft')][key]

        if callable( expandObject ):
            retStr = expandObject()
        else:
            retStr = expandObject

        if retStr == None or retStr =="":
            return '\<Tab>' 

        retStr = '\<C-\>\<C-N>%(moveOffset)dhd%(deleteOffset)dl%(insertMode)s' + retStr
        configDict = {}
        configDict['moveOffset'] = end - begin - 1
        configDict['deleteOffset'] = end - begin 
        configDict['insertMode'] = 'i' if len( lineRightCursor ) else 'a'
        return retStr % configDict 

    def __DoCompleteFunctionPrototype( self ):
        # get left context accordding to the cursor position
        cursorRow , cursorCol = vim.current.window.cursor
        lineLeftCursor =  vim.current.line[:cursorCol]
        lineRightCursor = vim.current.line[cursorCol:]

        # 1. get Function name
        reFunctionName = re.compile( "^.*?(?P<funcname>\w+)\s*\(\s*$" )
        regRet = reFunctionName.match( lineLeftCursor )
        if not regRet :
            return ""

        funcname = regRet.group('funcname')

        # 2. get tag list
        functionInfoList = vim.eval('taglist("^%s$")' % funcname )
        if functionInfoList == [] :
            sys.stderr.write("No tag for function |%s|" % funcname)
            return ""

        # 3. check whether  'signature' item exist , and retrieve them
        sigList = []
        for funcInfo in functionInfoList :
            if not funcInfo.has_key('signature'): continue
            sigList.append( funcInfo['signature'] )

        if sigList == []:
            sys.stderr.write("No signature found")
            return ""
        sigList = list( set(sigList) )


        # 4 . analyze the signature
        reSig = re.compile( "^\s*\((?P<param>.*)\)\s*(?P<const>const)?\s*$" )
        insertSigList = []
        for sig in sigList :
            regRet = reSig.match( sig )
            if not regRet: 
                insertSigList.append( "" )
                continue

            paramStr = ""
            paramList = regRet.group('param').split(',')
            for x in xrange( len( paramList) ): paramList[x] = paramList[x].strip() # strip the space
            
            # check if it is the "void"
            if len( paramList ) == 1 :
                paramIfVoid = paramList[0]
                if  paramIfVoid == "VOID" or paramIfVoid == "void" or paramIfVoid == "":
                    insertSigList.append("")
                    continue
            
            # give the AutoFillRegion tag around the each param
            paramListEx = []
            for param in paramList :
                paramListEx.append( "%(begin)s %(eachone)s %(end)s " % {
                        "begin" : exVimMagicKeyConfig.MagicKeyConfig['AutoFillRegion']['begin'] ,
                        "end" : exVimMagicKeyConfig.MagicKeyConfig['AutoFillRegion']['end'] ,
                        "eachone" : param } )
            paramStr = ','.join( paramListEx )
            insertSigList.append( paramStr )

        if len( insertSigList ) == 1 :
            return insertSigList[0] 

        # 5. show the choice to user
        prompt = ""
        for index in xrange( len( sigList ) ) :
            prompt += "%d> %s\\n" % ( index  + 1  ,  sigList[index] )
        prompt += "Select the Signature ( ESC to CANCEL ):"
        userSelection = vim.eval( 'input("%s")' % prompt )

        try :
            userSelection = int( userSelection )
            if userSelection < 1 or userSelection > len( sigList ):
                raise
        except:
            return ""

        return insertSigList[userSelection - 1] 


    def __DoFocusAutoFillRegion( self ):
        offsetSearch = 20  # search 20 lines range up and down the current line
        totalLine = len( vim.current.buffer )
        cursorRow , cursorCol = vim.current.window.cursor  # get cursor position

        # get search range
        fromLine = cursorRow - offsetSearch if cursorRow - offsetSearch > 0  else 0
        toLine = cursorRow + 20  if cursorRow + 20 < totalLine else totalLine

        # find the AutoFillRegion
        regStr = "%(begin)s.*?%(end)s" % exVimMagicKeyConfig.MagicKeyConfig['AutoFillRegion']
        regRet = None
        for x in xrange( fromLine , toLine ):
            regRet = re.search( regStr , vim.current.buffer[x] )
            if regRet :
                break

        if not regRet :
            return ""

        begin = regRet.start()
        end = regRet.end()
        lineIndex = x
        vim.current.window.cursor = ( lineIndex + 1 , begin + 1 )
        return '\<C-\>\<C-N>v%dl\<C-G>' % ( end - begin - 1 , )


exVim_pair_map = {
        '(' : ')' ,
        '[' : ']' ,
        '{' : '}' ,
        '<' : '>' ,
        '"' : '"' ,
        '\'' : '\''
        }

class exVimKey_AutoAddPair( exVimMagicKeyBase ):
    def __init__( self , main_window ):
        self.main_window = main_window 

    def register( self ):
        from exVimConfig import appid
        kmm = pvKeyMapManager( appid )
        for key in exVim_pair_map :
            kmm.register( key , PV_KMM_MODE_INSERT , self )

    def checkValidation( self , **kwdict ):
        self.key = str( kwdict['key'] )
        return pvWindow() == self.main_window

    def runAction( self ):
        if self.key == '"' :
            return_value = '%s\<C-\>\<C-N>i' % ( '\\' + self.key + '\\' + exVim_pair_map[ self.key ] , )
        else:
            return_value = '%s\<C-\>\<C-N>i' % ( self.key + exVim_pair_map[ self.key ] , )
        return return_value


exVim_pair_map_revert = dict ( [ ( exVim_pair_map[x] , x ) for x in exVim_pair_map.keys() if x != exVim_pair_map[x] ] ) 

class exVimKey_AutoMoveRightPair( exVimMagicKeyBase ):
    def __init__( self , main_window ):
        self.main_window = main_window 

    def register( self ):
        from exVimConfig import appid
        kmm = pvKeyMapManager( appid )
        for key in exVim_pair_map_revert :
            kmm.register( key , PV_KMM_MODE_INSERT , self )

    def checkValidation( self ,  **kwdict ):
        self.key = str( kwdict['key'] )
        return pvWindow() == self.main_window


    def runAction( self ):
        # get left context accordding to the cursor position
        cursorRow , cursorCol = vim.current.window.cursor
        lineLeftCursor =  vim.current.line[:cursorCol]
        lineRightCursor = vim.current.line[cursorCol:]

        regRet =  re.match( '^\s*(%s).*' % ( self.key if self.key != ')' else '\\)' , ) , lineRightCursor )
        if regRet:
            position = regRet.start(1)

            leftLB , leftRB = self.__CalcBracketNumber( lineLeftCursor , self.key )
            rightLB , rightRB = self.__CalcBracketNumber( lineRightCursor , self.key )

            if leftLB - leftRB != 0 and leftLB - leftRB == rightRB - rightLB:
                vim.current.window.cursor = ( cursorRow , cursorCol + position + 1 )
                return ''

        return self.key

    def __CalcBracketNumber( self , line , key ):
        left = 0
        right = 0
        for x in line:
            if x == exVim_pair_map_revert[str(key)] :
                left +=1
            elif x == str(key) :
                right += 1
        return ( left , right )
    

class exVimKey_ChangeSelectionOnPanel( exVimMagicKeyBase ):
    def __init__( self , tab_panel ):
        self.tab_panel = tab_panel

    def register( self ):
        from exVimConfig import appid
        kmm = pvKeyMapManager( appid )
        kmm.register( '<C-J>' , PV_KMM_MODE_INSERT , self )
        kmm.register( '<C-J>' , PV_KMM_MODE_NORMAL , self )
        kmm.register( '<C-K>' , PV_KMM_MODE_INSERT , self )
        kmm.register( '<C-K>' , PV_KMM_MODE_NORMAL , self )

    def checkValidation( self , **kwdict ):
        self.key = kwdict['key']
        return True

    def runAction( self ):
        panel_item = self.tab_panel.getCurrentPanel()
        buffer = panel_item.getBuffer()

        # check if the buffer is list buffer
        if not isinstance( buffer , pvListBuffer ): return

        offset = 1 if self.key == '<C-J>' else -1
        buffer.updateBuffer( selection = ( buffer.getSelection() + offset ) % len( buffer.getItemList() ) )


class exVimKey_ChangeSelectonOnPanelList( exVimMagicKeyBase ):
    def __init__ ( self , tab_panel ):
        self.tab_panel = tab_panel

    def register( self ):
        from exVimConfig import appid
        kmm = pvKeyMapManager( appid )
        kmm.register( '<2-LeftMouse>' , PV_KMM_MODE_NORMAL , self , self.tab_panel.getTabBuffer() )

    def checkValidation( self , **kwdict ):
        return True

    def runAction( self ):

        item_list = self.tab_panel.buffer.getItemList()
        # get selection position and update list
        cursor_line = vim.current.window.cursor[0]
        try :
            self.tab_panel.switchPanel( item_list[ cursor_line - 1 ] )
        except:
            return



class exVimKey_AutoContextComplete( exVimMagicKeyBase ):
    re_match_last_word = re.compile( "(.*\W+|^)(?P<word>[\w_]+)$" )

    def __init__( self , main_window , tab_panel ):
        self.main_window = main_window
        self.tab_panel = tab_panel

    def register( self ):
        from exVimConfig import appid
        kmm = pvKeyMapManager( appid )

        import string
        for letter in string.ascii_letters:
            kmm.register( letter , PV_KMM_MODE_INSERT , self )

        kmm.register( '_' , PV_KMM_MODE_INSERT , self )
        kmm.register( '<backspace>' , PV_KMM_MODE_INSERT , self )

    def checkValidation( self , **kwdict ):
        self.key = kwdict['key']
        self.return_key = '\\<Backspace>'  if self.key == '<Backspace>' else str ( self.key )
        return True

    def runAction( self ):
        # check if the main window
        if not pvWindow() == self.main_window :
            return self.return_key


        # check if the [content complete] panels is open
        current_panel = self.tab_panel.getCurrentPanel()
        if not current_panel == 'Context Complete' : return self.return_key

        
        # get line left cursor 
        cursor_line , cursor_column = vim.current.window.cursor
        line_left_cursor = vim.current.buffer[ cursor_line - 1 ][: cursor_column ] 
        # if input a valid letter , append it 
        if not self.key == '<Backspace>' :
            line_left_cursor += str( self.key )

        try :
            base_word = self.re_match_last_word.match( line_left_cursor ).group('word')
        except:
            return self.return_key

        if self.key == '<Backspace>' :
            # if just one letter left , it will be remove , so just
            # remove it , without complete anything
            if len( base_word ) == 1 :
                return self.return_key

            word = base_word[:-1]
            remove_list = [ base_word ]
        else:
            word = base_word
            remove_list = []

        if len( word ) < 3 : return self.return_key

        # find the possible words
        def searchWord( re_search_str , decrease_list = [] ):
            search_dict = {}
            re_search = re.compile( re_search_str )
            for eachline in vim.current.buffer :
                for search_ret in re_search.finditer( eachline ):
                    find_word = search_ret.group('word')
                    search_dict.__setitem__( find_word , search_dict.get( find_word , 0 ) + 1 )

            for x in decrease_list :
                if search_dict.has_key( x ):
                    if search_dict[x] == 1 :
                        del search_dict[x]
                    else:
                        search_dict[x] -= 1
                        
            revert_dict = {}
            for key in search_dict.keys() :
                if revert_dict.has_key( search_dict[key] ):
                    revert_dict[ search_dict[key] ].append( key )
                else:
                    revert_dict[ search_dict[key] ] = [ key ]

            for key in revert_dict.keys():
                revert_dict[key].sort()

            return revert_dict

        ## search  start with the 'word'  and middle with
        search_dict__start_with = searchWord( '(^|\s+)(?P<word>%s[\w_]+)' % word , remove_list )
        search_dict__middle_with = searchWord( '(?P<word>[\w_]+%s[\w_]*)' % word )

        # to list
        def searchDict2List( data_dict ):
            return_list = []
            key_list = data_dict.keys()
            key_list.sort( lambda x , y : x < y )
            for x in key_list :
                return_list.extend( data_dict[x] )
            return return_list

        buffer = current_panel.getBuffer()
        buffer.item = []
        buffer.item.extend( searchDict2List( search_dict__start_with ) )
        if ( not self.key == '<Backspace>' ) and len (  buffer.item ) == 1 :
            final_word = buffer.item[0]
            append_part = final_word[len(word):]
            if len( append_part ) == 1 :
                self.return_key = '%s%s\<C-O>v\<C-G>' % ( self.key , append_part )
            else:
                self.return_key = '%s%s\<C-O>v%dh\<C-G>' % (  self.key , append_part ,  len( append_part ) - 1 )

        buffer.item.extend( searchDict2List( search_dict__middle_with ) )
        buffer.updateBuffer( selection = 0 )

        return self.return_key

class exVimKey_AcceptSelectionOnPanel( exVimMagicKeyBase ):
    def __init__( self , main_window , tab_panel ):
        self.main_window = main_window
        self.tab_panel = tab_panel


    def register( self ):
        from exVimConfig import appid
        kmm = pvKeyMapManager( appid )

        kmm.register( '<C-Space>' , PV_KMM_MODE_INSERT , self )
        kmm.register( '<C-Space>' , PV_KMM_MODE_SELECT , self )

    def checkValidation( self , **kwdict ):
        self.mode = kwdict['mode']
        # check if it occured on the main window
        if not pvWindow() == self.main_window : return False
        # check if the 'Context Complete' Panel
        return self.tab_panel.getCurrentPanel() == 'Context Complete'

    def runAction( self ):
        if self.mode == PV_KMM_MODE_INSERT :
            complete_buffer = self.tab_panel.getCurrentPanel().getBuffer()

            # no data to complete
            if len( complete_buffer.item ) == 0 : return ""

            # delete word on cursor
            return ('\<C-W>%s' % complete_buffer.getItemList()[ complete_buffer.getSelection() ] )
        elif self.mode ==  PV_KMM_MODE_SELECT:
            return ""


class exVimKey_OpenTreeItem( exVimMagicKeyBase ):
    def __init__( self , tab_panel ):
        self.buffer = tab_panel.searchPanel(u'File Explorer').getBuffer()

    def register( self ):
        from exVimConfig import appid
        kmm = pvKeyMapManager( appid )
        kmm.register( '<2-LeftMouse>' , PV_KMM_MODE_NORMAL , self , self.buffer )

    def checkValidation( self , **kwdict ):
        return True

    def runAction( self ):
        from pyVim.pvTreeBuffer import PV_TREE_ACTION_TYPE_SWITCH
        self.buffer.updateBuffer( type = PV_TREE_ACTION_TYPE_SWITCH )

