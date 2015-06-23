#get system hardware info.
import socket
import platform
import datetime
import psutil

data = {}

#get system info.
data['hostname'] = socket.gethostname()
data['kernel_version'] = platform.release()
data['python_version'] = platform.python_version()
#get cpu info.
data['arch'] = platform.machine()
data['logical_cpu_num'] = psutil.cpu_count()  
data['physical_cpu_num' = psutil.cpu_count(logical=False) 
#get mem info.
data['memory'] = str(psutil.virtual_memory().total/1024/1024)+'M' 
#get disk info.
data['disk_total'] = psutil.disk_usage('/').total





#查看系统的用户信息
users_count = len(psutil.users())  
users_list = ",".join([ u.name for u in psutil.users()])  
print u"当前有%s个用户，分别是%s"%(users_count, users_list)  

#系统启动时间  
print u"系统启动时间 %s"%datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")  

#网卡，可以得到网卡属性，连接数，当前流量等信息  
net = psutil.net_io_counters()  
bytes_sent = '{0:.2f} kb'.format(net.bytes_recv / 1024)  
bytes_rcvd = '{0:.2f} kb'.format(net.bytes_sent / 1024)  
print u"网卡接收流量 %s 网卡发送流量 %s"%(bytes_rcvd, bytes_sent)  


