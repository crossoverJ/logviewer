import sys
import os
import threading

def logCollecter():
    def __init__(self,logFilter):
        self.logFilter = logFilter
    def getWordBetween(self,line,wa,wb):
        pos =line[line.find(wa)+len(wa):]
        pos = pos[:pos.find(wb)]
        return pos
    def logProcesser(self):
        print "log_processer"
        os.system('adb wait-for-device\n')
        os.system('adb shell logcat -c\n')
        time.sleep(0.5)
        result=open('templog','w')
        log=subprocess.Popen('adb shell logcat -v time',stdout=subprocess.PIPE,shell=True)
        time1=datetime.datetime(1900, 1, 1, 0, 0, 0, 0)
        time2=datetime.datetime(1900, 1, 1, 0, 0, 0, 0)
        while not quit_flag:
            line=log.stdout.readline()
            for filt in log_filter:
                if line.find(filt['keyword'])>1:
                    result.write(line)
                    try:
                        log_time=datetime.datetime.strptime(line[:18],'%m-%d %H:%M:%S.%f')
                        value = get_word_between(line,filt['leftword'],filt['rightword'])
                        value = filt['convert'](value.strip())
                        value = value / filt['div']
                        add_data(filt,int(value),log_time)
                    except:
                        print "process_log,error"
                    if filt['pass2next']:
                        continue
                    else:
                        break
        print 'out!'
        if quit_flag:
            print "kill -9 "+str(log.pid)+'\n'
            os.system("kill -9 "+str(log.pid)+'\n')
            os.system("kill -9 "+str(log.pid+2)+'\n')
            result.close()
        quit_flag=False
        result.close()
        print 'log_process quit'
        sys.exit()
    def fileProcesser(self):
        print "file_processer"
    def startProcess(self,mode):
        if self.logThread.alive():
            print "a"
