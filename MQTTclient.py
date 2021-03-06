#! /home/pi/.pyenv/shims/python2.7
# coding: utf-8

import paho.mqtt.client as mqtt
import time
import datetime
import time 
import sys
import pigpio
import iperf3
#test
n = 0 #待機モードの切り替え
port = 1883
topic = 'PicoRover/'+ sys.argv[2] +'/#'
deltaT = 0
ntime = datetime.datetime.now()
ptime = datetime.datetime.now()
timer = 0
limit = [30,1,15] #[初期接続待機時間、動作停止のタイムアウト時間、プログラム停止のタイムアウト時間]
end = 0
pi = pigpio.pi()
boundary = 205
interval = 0.001
Duty_center = 1500
counter = 0
#GPIOピン
servo = 18
DIR1 = 25
DIR2 = 24
PWM1 = 13
PWM2 = 19


def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(topic,0)

def on_message(client, userdata, msg):
    global signal
    #print("on_message")
    m = str(msg.payload)
    M = m.replace("b'","")
    M = M.replace("'","")
    M = M.split(':')
    #print(M)
    Message_switch(M)
    global n
    n = 1
    global ptime
    ptime = datetime.datetime.now()

def Message_switch(recv):

    if recv.count('S') >= 1:
        print ('')
    elif recv.count('E') >= 1:
        print ('E')
        global end
        end = 1
    elif recv[0].startswith('A'):
        RCcontroll_A(recv);
       # global com_speed
        #com_speed = recv
        #RC_timer1 = datetime.datetime.now()
    elif recv[0].startswith('B'):
        RCcontroll_B(recv);
    else:
        print("Not Defined Signal");
        pass;

def RCcontroll_A(recv):
        #global now_speed
        print(recv)
        value1 = int(recv[0].lstrip('A'))
        if value1 < -boundary:
            value1 = abs(value1)*0.3
            pi.set_mode(PWM1, pigpio.ALT2)
            pi.set_mode(PWM2, pigpio.ALT2)
            #now_speed = now_speed +(value1 - now_speed)/100
            #print(now_speed)
            pi.set_PWM_dutycycle(PWM1, value1)
            pi.set_PWM_dutycycle(PWM2, value1)
            #pi.set_PWM_dutycycle(PWM1, now_speed)
            #pi.set_PWM_dutycycle(PWM2, now_speed)
            pi.write(DIR1, 1)
            pi.write(DIR2, 0)
            time.sleep(interval)

        elif -boundary <= value1 <= boundary:
            print (str(value1))
            pi.set_mode(PWM1, pigpio.INPUT)
            pi.set_mode(PWM2, pigpio.INPUT)
            time.sleep(interval)

        elif boundary < value1:
            print (str(value1))
            value1 = value1*0.3
            pi.set_mode(PWM1, pigpio.ALT2)
            pi.set_mode(PWM2, pigpio.ALT2)
            #now_speed = now_speed +(value1 - now_speed)/100
            #print(now_speed)
            pi.set_PWM_dutycycle(PWM1, value1)
            pi.set_PWM_dutycycle(PWM2, value1)
            #pi.set_PWM_dutycycle(PMW1, now_speed)
            #pi.set_PWM_dutycycle(PWM2, now_speed)
            pi.write(DIR1, 0)
            pi.write(DIR2, 1)
            time.sleep(interval)



def RCcontroll_B(recv):
        value2 = int(recv[0].lstrip('B'))
        recv[0] = ''
        print (str(value2))
        pi.set_servo_pulsewidth(servo, value2)
        time.sleep(interval)


if __name__ == '__main__':
    args = sys.argv
    host = args[1]
    counter = 0
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    iclient = iperf3.Client()
    iclient.duration = 1 # Measurement time [sec]
    iclient.server_hostname = host # Server's IP address

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port=port, keepalive=60)

    pi.set_mode(PWM1, pigpio.INPUT) 
    pi.set_mode(PWM2, pigpio.INPUT)  
    pi.set_mode(DIR1, pigpio.OUTPUT)  
    pi.set_mode(DIR2, pigpio.OUTPUT)


    pi.set_PWM_range(PWM1, 1024) 
    pi.set_PWM_range(PWM2, 1024)
    ptime = datetime.datetime.now()

    pi.set_servo_pulsewidth(servo, Duty_center) #steering set center

    try:
        client.loop_start()

        while 1:
            ntime = datetime.datetime.now()
            deltaT = ntime - ptime
            timer = deltaT.total_seconds()
            if n == 1 and timer > limit[n]:#動作状態におけるタイムアウト時間をオーバーすると動作を止める
                pi.set_mode(PWM1, pigpio.INPUT)
                pi.set_mode(PWM2, pigpio.INPUT) 
                print("Controll TimeOut")
                n = 2 # 停止モード
            elif timer > limit[n]:#接続待機状態or停止状態におけるタイムアウト時間をオーバーすると動作を止める
                print("Connection TimeOut")
                break
            if end == 1:
                print('end')
                break
            time.sleep(0.1)#処理落ち防止のためにループ速度を落とす

    except KeyboardInterrupt:
        print (u'')
        print (u'KeryboardInterrupt')

    finally:
        client.loop_stop()
        #GPIOを入力に設定し、出力を止める
        pi.set_mode(servo, pigpio.INPUT)
        pi.set_mode(PWM1, pigpio.INPUT)
        pi.set_mode(PWM2, pigpio.INPUT)
        pi.set_mode(DIR1, pigpio.INPUT)
        pi.set_mode(DIR2, pigpio.INPUT)
        pi.stop()
        print('-------EXIT-------')
        sys.exit()
