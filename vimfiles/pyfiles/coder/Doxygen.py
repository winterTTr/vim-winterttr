import vim
import re
import sys

def DoxygenInit():
    vim.command('silent! nnoremenu <silent> p&yfiles.&doxygen.&file :py coder.Doxygen.DgFile()<CR>')
    vim.command('silent! nnoremenu <silent> p&yfiles.&doxygen.fun&ction :py coder.Doxygen.DgFunction()<CR>')
    vim.command('silent! nnoremenu <silent> p&yfiles.&doxygen.&class&&struct :py coder.Doxygen.DgClass()<CR>')


def GetIndent():
    ret = re.match('^(?P<indent>\s*).*$' , vim.current.line )
    if ret :
        return ret.group('indent')
    else:
        return ""

def DgFile():
    insertContent = [
            "/*!",
            " * @file     %s" % vim.eval('expand("%:t")') , 
            " * @brief    -->add brief <--" ,
            " * @author   winterTTr" ,
            " * @version  $Revision$" , 
            " * @date     $Date$",
            " * @bug      --> the bug <--",
            " *",
            " * ---> add detail <----",
            " */" ]
    vim.current.buffer[0:0] = insertContent

def DgFunction():
    reFunction = re.compile( """
        ^
        (?P<indent>\s*)
        (?P<status>(static|virtual)\s+)?
        (?P<return>(const\s+)?\w+(\s*[*&])*\s+)?
        (?P<name>[~\w]+)
        \s*
        \(
        (?P<sig>.*)
        \)
        \s*
        (const)?
        \s*
        (=\s*0)?
        \s*
        ;?
        \s*
        $
        """ , re.VERBOSE )
    ret = reFunction.match( vim.current.line )
    if not ret :
        sys.stderr.write( 'The current line does not seem a valid function decleration!')
        return

    # strip the spaces in items
    reFunctionDict = ret.groupdict()
    for key in reFunctionDict.keys():
        if key == 'indent':
            continue
        if reFunctionDict[key] != None :
            reFunctionDict[key] = reFunctionDict[key].strip()
        else:
            reFunctionDict[key] = ""

    # anylize the signature
    reParam = re.compile( """
        ^
        \s*
        (?P<type>(const\s+)?\w+(\s*[*&])*)
        \s+
        (?P<name>\w+)
        \s*
        (\[\s*\])?
        \s*
        $
        """ , re.VERBOSE )

    sigNameList = []
    if len( reFunctionDict['sig'] ) != 0 :
        for x in reFunctionDict['sig'].split(','):
            ret =  reParam.match( x )
            if ret :
                sigNameList.append( ret.group('name') )

    print sigNameList

    insertContent =     [ "/*!" ]
    insertContent.append( " * @brief    --> add brief <--" )

    for name in sigNameList :
        insertContent.append( " * @param[in,out]  %s   --> about param <--" % name )

    if reFunctionDict['return'] != "" and reFunctionDict['return'] != 'void':
        insertContent.append( " * @return   --> about return <--" )

    insertContent.append( " * @sa       --> about see also <--" )
    insertContent.append( " *")
    insertContent.append( " * --> about Detail <--")
    insertContent.append( " */")

    for index in xrange( len( insertContent ) ) :
        insertContent[index] = reFunctionDict['indent'] + insertContent[index]

    curLine = vim.current.window.cursor[0] - 1
    vim.current.buffer[curLine:curLine] = insertContent

def DgClass():
    reClass = re.compile( """
        ^
        (?P<indent>\s*)
        (?P<type>class|struct)
        \s+
        (?P<name>\w+)
        \s*
        (?P<inherit>:[^{]*)?
        ({.*)?
        (}.*)?
        ;?
        $
        """ , re.VERBOSE )
    ret = reClass.match( vim.current.line )
    if not ret :
        sys.stderr.write( 'The current line does not seem a valid function decleration!')
        return

    reClassDict = ret.groupdict()
    print reClassDict

    insertContent =     [ "/*!" ]
    insertContent.append( " * @%(type)-6s   %(classname)s  %(filename)s" % { 
            'type'      : reClassDict['type'] ,
            'classname' : reClassDict['name'] , 
            'filename'  : vim.eval( 'expand("%:t")' ) } )
    insertContent.append( " * @brief    --> add brief <--" )
    insertContent.append( " * @sa       --> add brief <--" )
    insertContent.append( " *")
    insertContent.append( " * --> about Detail <--")
    insertContent.append( " */")

    curLine = vim.current.window.cursor[0] - 1
    vim.current.buffer[curLine:curLine] = insertContent










