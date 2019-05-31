import subprocess
import telnetlib
import time

def check_ip_ping(ip):
    """
    进行ping交换机IP的操作，并对网络是否畅通返回值
    :param ip:
    :return: 0：网络不通  1：网络畅通
    """
    cmd = "ping -n 1 " + ip
    response = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    lines = response.stdout.readlines()
    res = lines[2].decode("gbk")
    #print(res.split(":")[1].strip())
    if res.strip() == "请求超时。":
        return 0
    else:
        res = res.split(":")[1].strip()
        if res == "无法访问目标主机。":
            return 0
        else:
            return 1

def telnet_func(ip):

    tn = telnetlib.Telnet()
    tn.open(ip)
    tn.read_until(b"SWA3300-ZJZZ login:", timeout=10)
    tn.write(user.encode("ascii")+b"\n")
    tn.read_until(b"Password:", timeout=10)
    tn.write(passwd.encode("ascii") + b"\n")
    #tn.read_until(b"root@SWA3300-ZJZZ:~#", timeout=10)
    time.sleep(0.5)
    tn.write(cmd_reboot.encode("ascii") + b"\n")
    time.sleep(0.5)
    cmd_result = tn.read_very_eager().decode("ascii")
    #logging.warning("%s"%cmd_result)

def time_now():
    """
    :return:返回固定时间格式 如：<20:35:29>
    """
    return time.strftime('<%H:%M:%S>', time.localtime())


if __name__ == '__main__':

    count = 0
    user = "root"
    passwd = "root"
    cmd_reboot = "reboot"
    ip = input("请输入ip：")
    while True:
        for i in range(120):
            time.sleep(1)
            res = check_ip_ping(ip)
            if res:
                print("<%s>网络连通..."%time_now())
                break
        for i in range(1,71):
            time.sleep(1)
            if i%5 == 0:
                print("<%s>%d"%(time_now(), i))
        telnet_func(ip)
        for i in range(20):
            time.sleep(1)
            res = check_ip_ping(ip)
            if not res:
                print("<%s>采集器重启中...."%time_now())
                break
        count +=1
        print("<%s>第%d次重启...."%(time_now(), count))