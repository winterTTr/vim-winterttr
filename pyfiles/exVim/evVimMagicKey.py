# standard module
import vim
import re
# pyVim module
from pyVim.pvKeyMapManager import PV_KMM_MODE_INSERT , PV_KMM_MODE_NORMAL , PV_KMM_MODE_SELECT
from pyVim.pvWrap import pvWindow
# exVim
import exVimMagicKeyConfig 

# add the key to expand
exVim_magic_key_list = [
        exVimKey_ExpandContent , 
        exVimKey_AutoAddPair , 
        exVimKey_AutoMoveRightPair
        ]


class MagicKeyBase:
    def __init__( self , kmm , wm ):
        self.kmm = kmm
        self.wm = wm

    def registerKey( self , kmm ):
        raise RuntimeError("No implement")

    def doAction( self , **kwdict ):
        raise RuntimeError("No implement")



class exVimKey_ExpandContent( MagicKeyBase ):
    def registerKey( self ):
        self.kmm.register( '<Tab>' , PV_KMM_MODE_INSERT , self.doAction )

    def DoExpandKeyword( self ):
        # get left context accordding to the cursor position
        cursorRow , cursorCol = vim.current.window.cursor
        lineLeftCursor =  vim.current.line[:cursorCol]
        lineRightCursor = vim.current.line[cursorCol:]

        # make avaliable key list
        expandKeyList = exVimMagicKeyConfig.MagicKeyExpandTemplate['_'].keys()
        if exVimMagicKeyConfig.MagicKeyExpandTemplate.has_key( vim.eval('&ft') ) :
             expandKeyList.extend( exVimMagicKeyConfig.MagicKeyExpandTemplate[ vim.eval('&ft') ].keys() )

        regStr = "(.*\s+|^)(?P<key>" + '|'.join(expandKeyList) + ")\s*$"
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

    def DoCompleteFunctionPrototype( self ):
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


    def DoFocusAutoFillRegion( self ):
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

    def doAction( self  , **kwdict ):
        if not pvWindow() == self.wm.getWindow('main') : return

        # 1. try to expand keyword
        # 2. try to complete the function prototype
        # 3. try replace the region
        # 4. default , just return the Tab Key
        return self.DoExpandKeyword() or self.DoCompleteFunctionPrototype() or self.DoFocusAutoFillRegion() or '\<Tab>'


exVim_pair_map = {
        '(' : ')' ,
        '[' : ']' ,
        '{' : '}' ,
        '"' : '"' ,
        '\'' : '\''
        }
exVim_pair_map_revert = dict ( [ ( exVim_pair_map[x] , x ) for x in exVim_pair_map.keys() if x != exVim_pair_map[x] ] ) 

class exVimKey_AutoAddPair( MagicKeyBase ):
    def registerKey( self ):
        for key in exVim_pair_map :
            self.kmm.register( key , PV_KMM_MODE_INSERT , self.doAction )

    def doAction( self , **kwdict ):
        if pvWindow() == self.wm.getWindow('main') :
            return '%s\<C-\>\<C-N>i' % ( str(key) + self.pair_map( str(key) ) , ) 

class exVimKey_AutoMoveRightPair( MagicKeyBase ):
    def registerKey( self ):
        for key in exVim_pair_map_revert :
            self.kmm.register( key , PV_KMM_MODE_INSERT , self.doAction )

    def CalcBracketNumber( self , line , key ):
        left = 0
        right = 0
        for x in line:
            if x == exVim_pair_map_revert[str(key)]
                left +=1
            elif x == str(key)
                right += 1
        return ( left , right )

    def doAction( self , **kwdict ):
        if not pvWindow() == exVim_window_manager.getWindow('main') : return
        # get left context accordding to the cursor position
        cursorRow , cursorCol = vim.current.window.cursor
        lineLeftCursor =  vim.current.line[:cursorCol]
        lineRightCursor = vim.current.line[cursorCol:]

        regRet =  re.match( '^\s*(%s).*' % ( str(key) if key != ')' else '\\' + str(key  , ) , lineRightCursor )
        if regRet:
            position = regRet.start(1)

            leftLB , leftRB = self.CalcBracketNumber( lineLeftCursor , key )
            rightLB , rightRB = self.CalcBracketNumber( lineRightCursor , key  )

            if leftLB - leftRB != 0 and leftLB - leftRB == rightRB - rightLB:
                vim.current.window.cursor = ( cursorRow , cursorCol + position + 1 )
                return ''

        return ')'

