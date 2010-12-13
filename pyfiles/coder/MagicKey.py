import vim
import re
import MagicKeyConfig 

globalMagicKeyMap = {}

def MagicKey( keyName ):
    if globalMagicKeyMap.has_key( keyName ) :
        globalMagicKeyMap[ keyName ].Action()


# register key to the globalMagicKeyMap
def RegisterKey( keymanager ) :
    globalMagicKeyMap[ keymanager.GetKeyName() ] = keymanager


# init the global function and register the key
def MagicKeyInit():
    vim.command("""
let g:Coder_MagicKey_ReturnValue=''
function! g:Coder_MagicKey(key)
    exec 'py coder.MagicKey("' . a:key .'")'
    return g:Coder_MagicKey_ReturnValue
endfunction
""")
    RegisterKey( Tab() )
    RegisterKey( LeftRoundBracket() )
    RegisterKey( RightRoundBracket() )


class KeyBase():
    def __init__( self ):
        vim.command(
                'inoremap %(vimkey)s <C-R>=g:Coder_MagicKey("%(key)s")<CR>' %  
                { 'vimkey' : self.GetVimKeyName() , 'key' : self.GetKeyName() } )

    def GetKeyName( self ):
        vimKey = self.GetVimKeyName()
        return vimKey.replace('<' , '').replace('>','')

    def SetReturn( self , keyReturned = None ):
        if keyReturned == None :
            vim.command( 'let g:Coder_MagicKey_ReturnValue=""' )
        else:
            vim.command( 'let g:Coder_MagicKey_ReturnValue="%s"' % keyReturned )

    def Action( self ):
        self.SetReturn()
        self.DoAction()

    # virtual function , need to be implement
    def DoAction( self ):
        raise RuntimeError("No implement")


    def GetVimKeyName( self ):
        raise RuntimeError("No implement")



class Tab( KeyBase ):
    def GetVimKeyName( self ):
        return "<Tab>"

    def DoExpandKeyword( self ):
        # get left context accordding to the cursor position
        cursorRow , cursorCol = vim.current.window.cursor
        lineLeftCursor =  vim.current.line[:cursorCol]
        lineRightCursor = vim.current.line[cursorCol:]

        # make avaliable key list
        expandKeyList = MagicKeyConfig.MagicKeyExpandTemplate['_'].keys()
        if MagicKeyConfig.MagicKeyExpandTemplate.has_key( vim.eval('&ft') ) :
             expandKeyList.extend( MagicKeyConfig.MagicKeyExpandTemplate[ vim.eval('&ft') ].keys() )

        regStr = "(.*\s+|^)(?P<key>" + '|'.join(expandKeyList) + ")\s*$"
        regRet =  re.match( regStr , lineLeftCursor )
        if not regRet :
            return False

        begin , end , key = regRet.start('key') , regRet.end('key') , regRet.group('key')
        expandObject = None
        if MagicKeyConfig.MagicKeyExpandTemplate['_'].has_key( key):
            expandObject = MagicKeyConfig.MagicKeyExpandTemplate['_'][key]
        else:
            expandObject = MagicKeyConfig.MagicKeyExpandTemplate[vim.eval('&ft')][key]

        if callable( expandObject ):
            retStr = expandObject()
        else:
            retStr = expandObject

        if retStr == None or retStr =="":
            self.SetReturn( '\<Tab>' )
            return True

        retStr = '\<C-\>\<C-N>%(moveOffset)dhd%(deleteOffset)dl%(insertMode)s' + retStr
        configDict = {}
        configDict['moveOffset'] = end - begin - 1
        configDict['deleteOffset'] = end - begin 
        configDict['insertMode'] = 'i' if len( lineRightCursor ) else 'a'
        self.SetReturn( retStr % configDict )
        return True

    def DoCompleteFunctionPrototype( self ):
        # get left context accordding to the cursor position
        cursorRow , cursorCol = vim.current.window.cursor
        lineLeftCursor =  vim.current.line[:cursorCol]
        lineRightCursor = vim.current.line[cursorCol:]

        # 1. get Function name
        reFunctionName = re.compile( "^.*?(?P<funcname>\w+)\s*\(\s*$" )
        regRet = reFunctionName.match( lineLeftCursor )
        if not regRet :
            return False

        funcname = regRet.group('funcname')

        # 2. get tag list
        functionInfoList = vim.eval('taglist("^%s$")' % funcname )
        if functionInfoList == [] :
            sys.stderr.write("No tag for function |%s|" % funcname)
            return False

        # 3. check whether  'signature' item exist , and retrieve them
        sigList = []
        for funcInfo in functionInfoList :
            if not funcInfo.has_key('signature'): continue
            sigList.append( funcInfo['signature'] )

        if sigList == []:
            sys.stderr.write("No signature found")
            return False
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
                        "begin" : MagicKeyConfig.MagicKeyConfig['AutoFillRegion']['begin'] ,
                        "end" : MagicKeyConfig.MagicKeyConfig['AutoFillRegion']['end'] ,
                        "eachone" : param } )
            paramStr = ','.join( paramListEx )
            insertSigList.append( paramStr )

        if len( insertSigList ) == 1 :
            self.SetReturn( insertSigList[0] ) 
            return True

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
            return True

        self.SetReturn("%s" % insertSigList[userSelection - 1] )
        return True


    def DoFocusAutoFillRegion( self ):
        offsetSearch = 20  # search 20 lines range up and down the current line
        totalLine = len( vim.current.buffer )
        cursorRow , cursorCol = vim.current.window.cursor  # get cursor position

        # get search range
        fromLine = cursorRow - offsetSearch if cursorRow - offsetSearch > 0  else 0
        toLine = cursorRow + 20  if cursorRow + 20 < totalLine else totalLine

        # find the AutoFillRegion
        regStr = "%(begin)s.*?%(end)s" % MagicKeyConfig.MagicKeyConfig['AutoFillRegion']
        regRet = None
        for x in xrange( fromLine , toLine ):
            regRet = re.search( regStr , vim.current.buffer[x] )
            if regRet :
                break

        if not regRet :
            return False

        begin = regRet.start()
        end = regRet.end()
        lineIndex = x
        vim.current.window.cursor = ( lineIndex + 1 , begin + 1 )
        self.SetReturn('\<C-\>\<C-N>v%dl\<C-G>' % ( end - begin - 1 , ) )
        return True




    def DoAction( self ):
        # 1. try to expand keyword
        if self.DoExpandKeyword():
            return

        # 2. try to complete the function prototype
        if self.DoCompleteFunctionPrototype():
            return

        # 3. try replace the region
        if self.DoFocusAutoFillRegion():
            return

        # 4 . default , just return the Tab Key
        self.SetReturn('\<Tab>')

class LeftRoundBracket( KeyBase ):
    def GetVimKeyName( self ):
        return '('

    def DoAction( self ):
        self.SetReturn('()\<C-\>\<C-N>i')

class RightRoundBracket( KeyBase ):
    def GetVimKeyName( self ):
        return ')'

    def CalcBracketNumber( self , line ):
        left = 0
        right = 0
        for x in line:
            if x == '(' :
                left +=1
            elif x == ')' :
                right += 1
        return ( left , right )

    def DoAction( self ):
        vim.command("set noshowmode")
        # get left context accordding to the cursor position
        cursorRow , cursorCol = vim.current.window.cursor
        lineLeftCursor =  vim.current.line[:cursorCol]
        lineRightCursor = vim.current.line[cursorCol:]

        regRet =  re.match( '^\s*(\)).*' , lineRightCursor )
        if regRet:
            position = regRet.start(1)

            leftLB , leftRB = self.CalcBracketNumber( lineLeftCursor )
            rightLB , rightRB = self.CalcBracketNumber( lineRightCursor )

            if leftLB - leftRB != 0 and leftLB - leftRB == rightRB - rightLB:
                vim.current.window.cursor = ( cursorRow , cursorCol + position + 1 )
                return

        self.SetReturn(')')

