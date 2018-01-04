<!--record http get arg -->
<font size="4" color="#FF0000"><b>record string in strings.txt</b> </font>

<%
dim strKey,strLogFile,strString,strDate,strMonth,strDay

if len(Month(date))=1 then
  strMonth="0"&Month(date)
else
  strMonth=Month(date)
end if
if len(day(date))=1 then
  strDay="0"&day(date)
else
  strDay=day(date)
end if

strDate=year(date)&strMonth&strDay
strLogFile="strings"&strDate&".txt"
strKey=request("str")
if str
Key=""  then
  response.write "String is empty!"
  response.end
End If
strString=strKey&" "&strDate&" "&time

set f=Server.CreateObject("scripting.filesystemobject")
set ff=f.opentextfile(server.mappath(".")&"\"&strLogFile,8,true,0)
ff.writeline(chr(13)+chr(10)&StrString)
ff.close
set ff=nothing
set f=nothing

%>