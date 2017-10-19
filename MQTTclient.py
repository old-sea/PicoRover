#! /home/pi/.pyenv/shims/python2.7
# coding: utf-8

import paho.mqtt.client as mqtt
import time
import datetime
import time 
import sys
import pigpio
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
servo = 18
DIR1 = 25
DIR2 = 24
PWM1 = 13
PWM2 = 19


def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(topic,0)

def on_message(client, userdata, msg):
    print("on_message")
    m = str(msg.payload)
    M = m.replace("b'","")
    M = M.replace("'","")
    M = M.split(':')
    print(M)
    try:
        RCcontroll(M)
    except:
        print("Controll Out")
    global n
    n = 1
    global ptime
    ptime = datetime.datetime.now()

def RCcontroll(recv):
    print("control")
    if recv.count('S') >= 1:
        print ('S')
    elif recv.count('E') >= 1:
        print ('E')
        global end
        end = 1
    elif recv[0].startswith('A'):  # å—ã‘å–ã£ãŸæ–‡å­—åEãŒAã§å§‹ã¾ã‚‹å ´åE
        value1 = int(recv[0].lstrip('A'))  # æ–E­—åEã®é ­ã‚’å‰Šé™¤ã—ã¦æ•´æ•°ã«å¤‰æ›
        if value1 < -boundary:
            print (str(value1))
            value1 = abs(value1)*0.3
            pi.set_mode(PWM1, pigpio.ALT2)  # 13ç•ªãƒ”ãƒ³ã‚’ALT2ã«è¨­å®E
            pi.set_mode(PWM2, pigpio.ALT2)  # 19ç•ªãƒ”ãƒ³ã‚’ALT2ã«è¨­å®E
            pi.set_PWM_dutycycle(PWM1, value1)  # pwmåˆ¶å¾¡
            pi.set_PWM_dutycycle(PWM2, value1)
            pi.write(DIR1, 1)  # 25,24ç•ªãƒ”ãƒ³ã«LOWã‚’åEåŠE
            pi.write(DIR2, 0)
            time.sleep(interval)

        elif -boundary <= value1 <= boundary:
            print (str(value1))
            pi.set_mode(PWM1, pigpio.INPUT)  # pwmãƒ¢ãƒ¼ãƒ‰ã§ãƒEƒ¥ãƒ¼ãƒE‚£æ¯”ã‚’0ã«ã™ã‚‹ã ã‘ã§ã¯ãƒ¢ãƒ¼ã‚¿ã®å›žè»¢ãŒæ­¢ã¾ã‚‰ãªãE
            pi.set_mode(PWM2, pigpio.INPUT)  # ãƒ”ãƒ³ã‚’åEåŠ›ã«è¨­å®šã™ã‚‹ã“ã¨ã§ãƒ¢ãƒ¼ã‚¿ãŒã¨ã¾ã‚‹ã¿ãŸã„
            time.sleep(interval)

        elif boundary < value1:
            print (str(value1))
            value1 = value1 * 0.2
            pi.set_mode(PWM1, pigpio.ALT2)  # 13ç•ªãƒ”ãƒ³ã‚’ALT2ã«è¨­å®E
            pi.set_mode(PWM2, pigpio.ALT2)  # 19ç•ªãƒ”ãƒ³ã‚’ALT2ã«è¨­å®E
            pi.set_PWM_dutycycle(PWM1, value1)  # pwmåˆ¶å¾¡
            pi.set_PWM_dutycycle(PWM2, value1)
            pi.write(DIR1, 0)  # 25,24ç•ªãƒ”ãƒ³ã«HIGHã‚’åEåŠE
            pi.write(DIR2, 1)
            time.sleep(interval)

    elif recv[0].startswith('B'):
        value2 = int(recv[0].lstrip('B'))
        recv[0] = ''
        print (str(value2))
        pi.set_servo_pulsewidth(servo, value2)
        time.sleep(interval)

    else:
        print("not defined signal")
        pass


if __name__ == '__main__':
    args = sys.argv
    host = args[1]
    counter = 0
     #Publisherã¨åŒæ§˜ã« v3.1.1ã‚’åˆ©ç”¨
    client = mqtt.Client(protocol=mqtt.MQTTv311)

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
            if n == 1 and timer > limit[n]:
                pi.set_mode(PWM1, pigpio.INPUT)  # pwmãƒ¢ãƒ¼ãƒ‰ã§ãƒEƒ¥ãƒ¼ãƒE‚£æ¯”ã‚’0ã«ã™ã‚‹ã ã‘ã§ã¯ãƒ¢ãƒ¼ã‚¿ã®å›žè»¢ãŒæ­¢ã¾ã‚‰ãªãE
                pi.set_mode(PWM2, pigpio.INPUT) 
                print("Controll TimeOut")
                n = 2
            elif timer > limit[n]:
                print("Connection TimeOut")
                break
            if end == 1:
                print('end')
                break
            time.sleep(0.1)

    except KeyboardInterrupt:
        print (u'')
        print (u'KeryboardInterrupt')

    finally:
        client.loop_stop()
        pi.set_mode(servo, pigpio.INPUT)
        pi.set_mode(PWM1, pigpio.INPUT)
        pi.set_mode(PWM2, pigpio.INPUT)
        pi.set_mode(DIR1, pigpio.INPUT)
        pi.set_mode(DIR2, pigpio.INPUT)
        pi.stop()
        print('-------EXIT-------')
        sys.exit()
