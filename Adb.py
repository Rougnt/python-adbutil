import os 
import subprocess
from sys import stderr

adb_path=os.path.join('adb','adb.exe')

class Adb():
    '''
        用来创建一个设备连接
    '''
    def __init__(self,device=None,ipAddress=None,port=None) -> None:
        '''
            初始化使用IP地址和端口
            ipAddress: 设备IP，本地为127.0.0.1
            port: 开放端口 默认为5555
            初始化使用设备id
            device: 设备id

            例：
            使用设备IP Adb(ipAddress = '192.168.123.186',port = 43137)
            使用设备id Adb(device = 'd5c42b2a')

        '''
        if ipAddress is not None:
            self.connect = ipAddress+':'+str(port)   # 连接设备字符串
            output = subprocess.Popen(adb_path+' connect '+self.connect,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read().decode('utf-8')
            self.connect = ' -s '+self.connect
            if output.split(' ')[0] == 'connected' or output.split(' ')[0] == 'already' :
                print('连接成功')
                self.resolution = self.getScreenResolution()
            else:
                raise Exception('无法连接设备\n'+str(output))
        elif device is not None:
            self.connect = device
            output = subprocess.Popen(adb_path+' devices',stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read().decode('utf-8')
            self.connect = ' -s '+self.connect
            b = [i.split('\t') for i in output.splitlines()[1:-1]]
            for a in b:
                if a[0]==device and a[1]=='device':
                    print('连接成功')
                    self.resolution = self.getScreenResolution()
                    break
            else:
                raise Exception('无法连接设备\n'+str(output))
        else:
            raise ValueError("参数不能为空")

        

    def tap(self,x,y):
        '''
            点击屏幕
            x,y为点击的屏幕坐标
            Return 命令执行状态
        '''
        return os.system(adb_path+self.connect+' shell input tap '+str(x)+' '+str(y))
    
    def screenCap(self):
        '''
            屏幕截图存储至/sdcard/01.png
            Return 窗口分辨率
        '''
        output = subprocess.Popen(adb_path+self.connect+' shell screencap -p /sdcard/01.png',stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read().decode('utf-8')
        
        return output.split(' ')[-1].split('x')
    
    def pullBackScreenCap(self,savePath=None,delete=True):
        '''
            将截图的屏幕传回到savePath，如e://savepath//01.png
            默认传回./adb/screen.png
        '''
        if savePath is None:
            # 默认
            os.system(adb_path+self.connect+' pull /sdcard/01.png '+os.path.join('adb','screen.png'))
            
        else:
            os.system(adb_path+self.connect+' pull /sdcard/01.png '+savePath)
        
        if delete is True:
            self.rmFile(filePath='/sdcard/01.png')
    
    def getScreenResolution(self):
        '''
            获得屏幕分辨率
            Return (tuple) 屏幕分辨率
        '''
        result = os.popen(adb_path+self.connect+' shell wm size').read().strip()
        result = str(result).split(' ')[2].split('x')
        result = (int(result[0]),int(result[1]))
        assert result[0] is not int and result[1] is not int 
        return result
    
    def rmFile(self,filePath):
        '''
            删除手机中文件
            Return 是否成功删除
        '''
        result = os.popen(adb_path+self.connect+' shell rm '+filePath).read()
        return result
    


if __name__ == '__main__':
    adb = Adb(ipAddress='192.168.123.186',port=43137)
    adb.screenCap()
    adb.pullBackScreenCap()