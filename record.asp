<!--record http get arg -->
<font size="4" color="#FF0000"><b>record string in strings.txt</b> </font>

<%
dim XKey,strLogFile,strString,strDate
strDate=year(date)&month(date)&day(date)
strLogFile="strings"&strDate&".txt"
XKey=request("str")
if XKey=""  then
  response.write "String is empty!"
  response.end
End If
StrString=StrString&XKey
StrString=StrString&" "&strDate&" "&time

set f=Server.CreateObject("scripting.filesystemobject")
set ff=f.opentextfile(server.mappath(".")&"\"&strLogFile,8,true,0)
ff.writeline(chr(13)+chr(10)&StrString)
ff.close
set ff=nothing
set f=nothing

%>