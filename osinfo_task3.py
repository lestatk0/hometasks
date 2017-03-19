import psutil
import datetime
import json
import configparser
import time
import schedule

config = configparser.ConfigParser()
config.read('config.ini')
output = config.get('common', 'output')
interval = config.get('common', 'interval')

snapshot_num=0

def cpu_info():
    cpu=""
    for i in range(len(psutil.cpu_percent(interval=1,percpu=True))):
        cpu+="Core{0} : {1} %\n".format(i+1,psutil.cpu_percent(interval=1,percpu=True)[i])
        i+=1
    return cpu

def memory_info():
    memory=""
    memory_data=psutil.virtual_memory()
    memory_str=["total","avaliable","Usage percent %","Used","Free"]
    for i in range(len(memory_str)):
        if i != 2:
            memory+="{0} : {1} MB \n".format(memory_str[i], round(memory_data[i]/1048576,2))
        else:
            memory += "{0} : {1} \n".format(memory_str[i],memory_data[i])
        i+=1
    return memory

def swap_info():
    swap=""
    swap_data=psutil.swap_memory()
    swap_str=["total","Used","Free","Percent %","sin","sout"]
    for i in range(len(swap_str)):
        if i != 3:
            swap+="{0} : {1} MB \n".format(swap_str[i], round(swap_data[i]/1048576,3))
        else:
            swap += "{0} : {1}\n".format(swap_str[i],swap_data[i])
        i+=1
    return swap

def disk_info():
    disk_in='Disk read: {0} MB\n'.format(round(psutil.disk_io_counters()[2] / 1048576,2))
    disk_out='Disk write: {0} MB'.format(round(psutil.disk_io_counters()[3] / 1048576,2))
    disk=disk_in + disk_out + "\n"
    return disk


def net_info():
    net_output='Send {}Mb\n'.format(round(psutil.net_io_counters()[0] / 1048576,2))
    net_input='Recieve {}Mb\n'.format(round(psutil.net_io_counters()[1] / 1048576,2))
    net=net_output + net_input
    return net


def txt():
    global snapshot_num
    datatime=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d - %H:%M:%S')
    file = open('log.txt', "a")
    file.write("\nSNAPSHOT {0}:{1}\n".format(snapshot_num, datatime))
    file.write("{}\n".format("="*10))
    file.write("CPU load:\n{0}".format(cpu_info()))
    file.write("."*10 + "\n")
    file.write("Memory :\n{0}".format(memory_info()))
    file.write("." * 10 + "\n")
    file.write("Swap :\n{0}".format(swap_info()))
    file.write("." * 10 + "\n")
    file.write("Disk I/O:\n{0}".format(disk_info()))
    file.write("." * 10 + "\n")
    file.write("Net I/O :\n{0}".format(net_info()))
    file.write("="*10)
    file.close()
    snapshot_num += 1

def jsonfile():
    global snapshot_num
    datatime=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d - %H:%M:%S')
    info = {
     "CPU load:": cpu_info(),
     "Memory:" : memory_info(),
     "Swap:": swap_info(),
     "Disk I/O:":disk_info(),
     'Net:':net_info(),
      }
    data = ('SNAPSHOT' + str(snapshot_num) + ": " + str(datatime) + ": ",info)
    with open("log.json", "a") as file:
     json.dump(data, file, indent=3, sort_keys=True)
    snapshot_num += 1

if output == "json":
    schedule.every(int(interval)).minutes.do(jsonfile)
elif output == "txt":
    schedule.every(int(interval)).minutes.do(txt)
else:
    print("Format error")

while True:
    schedule.run_pending()
    time.sleep(1)