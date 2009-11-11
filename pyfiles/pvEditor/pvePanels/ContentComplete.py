import vim
import re

from _PanelBase_ import PanelBase

from pyVim.pvListBuffer import pvListBuffer
from pyVim.pvUtil import pvString

from pyVim.pvKeyMap import pvKeyMapEvent , pvKeyMapManager , pvKeyMapObserver
from pyVim.pvKeyMap import PV_KM_MODE_INSERT , PV_KM_MODE_SELECT

from pyVim.pvWrap import pvWindow

import pveMagicKeyConfig


class _class_( PanelBase , pvKeyMapObserver ):
    def __init__( self , win_mgr ):
        self.__win_mgr = win_mgr
        self.__buffer = pvListBuffer()

        self.__name = u"Content Complete"

        # init key event

        # <tab>
        _ob = CCExpandContent( self.__win_mgr.getWindow('main') )
        _event = pvKeyMapEvent( '<Tab>' ,  PV_KM_MODE_INSERT )
        pvKeyMapManager.registerObserver( _event , _ob )

        # <pairs>
        _ob = CCAutoAddPair( self.__win_mgr.getWindow('main') )
        for key in pve_pair_map :
            _event = pvKeyMapEvent( key ,  PV_KM_MODE_INSERT )
            pvKeyMapManager.registerObserver( _event , _ob )

        # <pair move>
        _ob = CCAutoMoveRightPair( self.__win_mgr.getWindow('main') )
        for key in pve_pair_map_revert :
            _event = pvKeyMapEvent( key ,  PV_KM_MODE_INSERT )
            pvKeyMapManager.registerObserver( _event , _ob )

        # < move item on panel >
        _ob = CCChangeSelecton( self.__win_mgr.getWindow('main') , self.__buffer )
        pvKeyMapManager.registerObserver( pvKeyMapEvent( '<C-J>' , PV_KM_MODE_INSERT ) , _ob )
        pvKeyMapManager.registerObserver( pvKeyMapEvent( '<C-K>' , PV_KM_MODE_INSERT ) , _ob )

        # < auto complete >
        _ob = CCAutoContextComplete( self.__win_mgr.getWindow('main') , self.__buffer )
        import string
        for letter in string.ascii_letters:
            pvKeyMapManager.registerObserver( pvKeyMapEvent( letter , PV_KM_MODE_INSERT ) , _ob )
        pvKeyMapManager.registerObserver( pvKeyMapEvent( '_' , PV_KM_MODE_INSERT ) , _ob )
        pvKeyMapManager.registerObserver( pvKeyMapEvent( '<backspace>' , PV_KM_MODE_INSERT ) , _ob )

        # < accept complete >
        _ob = CCAcceptSelection( self.__win_mgr.getWindow('main') , self.__buffer )
        pvKeyMapManager.registerObserver( pvKeyMapEvent( '<C-Space>' , PV_KM_MODE_INSERT ) , _ob )
        pvKeyMapManager.registerObserver( pvKeyMapEvent( '<C-Space>' , PV_KM_MODE_SELECT ) , _ob )


    # from |PanelBase|
    def OnName( self ):
        str = pvString()
        str.UnicodeString = self.__name
        return str

    def OnPanelSelected( self , item ):
        if item.UnicodeString != self.__name :
            return

        self.__buffer.showBuffer( self.__win_mgr.getWindow('panel') )
        self.__buffer.updateBuffer()

    # from |pvKeyMapObserver|
    def OnHandleKeyEvent( self , **kwdict ):
        if not self.__buffer.isShown() :
            return ""

        if len( self.__buffer.items ):
            offset = 1 if kwdict['key'] == '<C-J>' else -1
            self.__buffer.updateBuffer( selection = ( self.__buffer.selection + offset ) % len( self.__buffer.items ) )


class CCExpandContent( pvKeyMapObserver ):
    def __init__( self , main_window ):
        self.main_window = main_window

    def OnHandleKeyEvent( self  , **kwdict ):
        if not pvWindow() == self.main_window:
            return '\<Tab>'

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
        expandKeyList = pveMagicKeyConfig.MagicKeyExpandTemplate['_'].keys()
        if pveMagicKeyConfig.MagicKeyExpandTemplate.has_key( vim.eval('&ft') ) :
             expandKeyList.extend( pveMagicKeyConfig.MagicKeyExpandTemplate[ vim.eval('&ft') ].keys() )

        regStr = "(.*\s+|^)(?P<key>" + '|'.join(expandKeyList) + ")$"
        regRet =  re.match( regStr , lineLeftCursor )
        if not regRet :
            return ""

        begin , end , key = regRet.start('key') , regRet.end('key') , regRet.group('key')
        expandObject = None
        if pveMagicKeyConfig.MagicKeyExpandTemplate['_'].has_key( key):
            expandObject = pveMagicKeyConfig.MagicKeyExpandTemplate['_'][key]
        else:
            expandObject = pveMagicKeyConfig.MagicKeyExpandTemplate[vim.eval('&ft')][key]

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
                        "begin" : pveMagicKeyConfig.MagicKeyConfig['AutoFillRegion']['begin'] ,
                        "end" : pveMagicKeyConfig.MagicKeyConfig['AutoFillRegion']['end'] ,
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
        regStr = "%(begin)s.*?%(end)s" % pveMagicKeyConfig.MagicKeyConfig['AutoFillRegion']
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

pve_pair_map = {
        '(' : ')' ,
        '[' : ']' ,
        '{' : '}' ,
        '<' : '>' ,
        '"' : '"' ,
        '\'' : '\''
        }

class CCAutoAddPair( pvKeyMapObserver ):
    def __init__( self , main_window ):
        self.main_window = main_window 

    def OnHandleKeyEvent( self , **kwdict ):
        self.key = str( kwdict['key'] )

        if not pvWindow() == self.main_window :
            return self.key

        if self.key == '"' :
            return_value = '%s\<C-\>\<C-N>i' % ( '\\' + self.key + '\\' + pve_pair_map[ self.key ] , )
        else:
            return_value = '%s\<C-\>\<C-N>i' % ( self.key + pve_pair_map[ self.key ] , )
        return return_value


pve_pair_map_revert = dict ( [ ( pve_pair_map[x] , x ) for x in pve_pair_map if x != pve_pair_map[x] ] ) 

class CCAutoMoveRightPair( pvKeyMapObserver ):
    def __init__( self , main_window ):
        self.main_window = main_window 

    def OnHandleKeyEvent( self , **kwdict ):
        self.key = str( kwdict['key'] )

        if not pvWindow() == self.main_window:
            return self.key

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
            if x == pve_pair_map_revert[str(key)] :
                left +=1
            elif x == str(key) :
                right += 1
        return ( left , right )


class CCAutoContextComplete( pvKeyMapObserver ):
    re_match_last_word = re.compile( "(.*\W+|^)(?P<word>[\w_]+)$" )

    def __init__( self , main_window , complete_buffer ):
        self.main_window = main_window
        self.complete_buffer = complete_buffer

    def OnHandleKeyEvent( self , **kwdict ):
        print "here"

        self.key = kwdict['key']
        self.return_key = '\\<Backspace>'  if self.key == '<Backspace>' else str ( self.key )

        print "11"

        # check if the main window
        if not pvWindow() == self.main_window :
            return self.return_key

        print "1"

        # check if the [content complete] panels is open
        if not self.complete_buffer.isShown() : return self.return_key

        print "2"

        
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

        self.complete_buffer.items = []
        items = searchDict2List( search_dict__start_with )
        uni_items = [ pvString() for x in items ]
        for x in xrange( len(uni_items) ):
            uni_items[x].MultibyteString = items[x]
        self.complete_buffer.items.extend( uni_items )
        if ( not self.key == '<Backspace>' ) and len (  self.complete_buffer.items ) == 1 :
            final_word = items[0]
            append_part = final_word[len(word):]
            if len( append_part ) == 1 :
                self.return_key = '%s%s\<C-O>v\<C-G>' % ( self.key , append_part )
            else:
                self.return_key = '%s%s\<C-O>v%dh\<C-G>' % (  self.key , append_part ,  len( append_part ) - 1 )


        items = searchDict2List( search_dict__middle_with )
        uni_items = [ pvString() for x in items ]
        for x in xrange( len(uni_items) ):
            uni_items[x].MultibyteString = items[x]
        self.complete_buffer.items.extend( uni_items )
        self.complete_buffer.updateBuffer( selection = 0 )

        return self.return_key


class CCAcceptSelection( pvKeyMapObserver ):
    def __init__( self , main_window , complete_buffer ):
        self.main_window = main_window
        self.complete_buffer = complete_buffer

    def OnHandleKeyEvent( self , **kwdict ):
        self.mode = kwdict['mode']
        if not pvWindow() == self.main_window : return ""
        if not self.complete_buffer.isShown(): return ""

        if self.mode == PV_KM_MODE_INSERT :
            # no data to complete
            if len( self.complete_buffer.items ) == 0 : return ""

            # delete word on cursor
            return ('\<C-W>%s' % self.complete_buffer.items[ self.complete_buffer.selection ].MultibyteString )
        elif self.mode ==  PV_KM_MODE_SELECT:
            return ""


class CCChangeSelecton( pvKeyMapObserver ):
    def __init__( self , main_window , complete_buffer ):
        self.main_window = main_window
        self.complete_buffer = complete_buffer

    def OnHandleKeyEvent( self , **kwdict ):
        if not pvWindow() == self.main_window : return ""
        if not self.complete_buffer.isShown() : return ""

        if len( self.complete_buffer.items ):
            offset = 1 if kwdict['key'] == '<C-J>' else -1
            self.complete_buffer.updateBuffer( selection = ( self.complete_buffer.selection + offset ) % len( self.complete_buffer.items ) )

