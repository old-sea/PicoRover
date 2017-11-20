#!/usr/bin/env python3

import iperf3
import sys
import paho.mqtt.client as mqtt
from time import sleep





def TesT(port):

    iclient = iperf3.Client()
    iclient.duration = 1 # Measurement time [sec]
    iclient.server_hostname = '192.168.95.151' # Server's IP address
    iclient.port = port
    result = iclient.run()


    print("start")
    if result.error:
        print(result.error)
    else:
        print('')
        #print('Test completed:')
        #print('  started at         {0}'.format(result.time))
        #print('  bytes transmitted  {0}'.format(result.sent_bytes))
        #print('  retransmits        {0}'.format(result.retransmits))
        #print('  avg cpu load       {0}%\n'.format(result.local_cpu_total))

        #print('Average transmitted data in all sorts of networky formats:')
        #print('  bits per second      (bps)   {0}'.format(result.sent_bps))
        #print('  Kilobits per second  (kbps)  {0}'.format(result.sent_kbps))
        print('  Megabits per second  (Mbps)  {0}'.format(result.sent_Mbps))
        #print('  KiloBytes per second (kB/s)  {0}'.format(result.sent_kB_s))
        #print('  MegaBytes per second (MB/s)  {0}'.format(result.sent_MB_s))
        print(result.sent_Mbps)
        client.publish(topic,result.sent_Mbps)
        TesT(port);
if __name__ == '__main__':
    args = sys.argv
    #while True:
    host = args[1]
    port = 1883
    topic = 'PicoRover/throughput/' + args[3]
    iport = args[2]


    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(host, port=port, keepalive=60)
    print ("on_connect")

    TesT(iport)
        #sleep(5)