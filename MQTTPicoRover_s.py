# coding: utf-8
import paho.mqtt.client as mqtt
import sys, pygame, time, datetime
from pygame.locals import *  # pygame中で使用できる定数群をimport


def JoystickDetection(args):
    host = args  # サーバの固定IPを設定
    port = 1883  # 通信に使用するポート番号を指定
    topic = ['PicoRover/1st','PicoRover/2nd','PicoRover/3rd','PicoRover/stop']
    range = 1024 # server側で使用するpwmのrange
    sleeptime = 0.05 # socketで送信した後のスリープ時間
    target = 0


    try:
        client = mqtt.Client(protocol=mqtt.MQTTv311)
        client.connect(host, port=port, keepalive=60)

    except KeyboardInterrupt:
        print ('')
        print ('KeyboardInterrupt')
        sys.exit()

    except:
        print(u'接続できませんでした')
        sys.exit()


    try:
        pygame.init()  # pygameの初期化
        j = pygame.joystick.Joystick(0)  # ジョイスティックオブジェクトの作成
        j.init()  # オブジェクトの初期化
        print (u'Joystickの名称: ' + j.get_name())
        print (u'WebカメラのIP:' + ' '  + host)
        print (u'Webカメラのポート:' + u' ' + u'8080')
        print (u'-------START-------')
        print ('')
        print (u'前進 : 右スティックUP')
        print (u'後退 : 右スティックDOWN')
        print (u'ステアリング左 : 左スティックLEFT')
        print (u'ステアリング右 : 左スティックRIGHT')
        print (u'終了 : PSボタン')

    except pygame.error:  # tryがうまくいかない場合pygame.errorからエラーがraiseされる
        print (u'Joystickが見つかりませんでした。')
        sys.exit()  # コントローラがつながれていないのでプログラムを終了

    # ボタンダウンとハットモーション入力をブロック
    pygame.event.set_blocked([JOYBUTTONUP, JOYHATMOTION])
    # value1,value2を初期化
    value1 = 0
    value2 = 1500 # 1500はサーボモータがセンター位置になるパルス幅
    timer_old = datetime.datetime.now()

    try:
        while 1:
            for e in pygame.event.get():  # イベントを取得
                # 取得したイベントをチェックし、サーバ側にボタンに対応するstringを送信
                if e.type == pygame.locals.JOYAXISMOTION:
                    value1_new = round(j.get_axis(3) * range) # 右スティックの値からデューティ比を計算
                    value2_new = round((j.get_axis(0) * 500) + 1500) # 左スティックの値からパルス幅を計算

                    value1_new = int(value1_new) # value1,value2の値をfloatからintに変換
                    value2_new = int(value2_new)

                    if (abs(value1_new - value1) <= 20) and (abs(value2_new - value2) <= 20): # value1,value2の値の微小な変化は無視する
                        pass

                    elif abs(value1_new - value1) > 20: # value1の値の微小な変化は送信しない
                        value1 = value1_new # value1の値を更新する

                        value1_str = 'A' + str(value1) + ':'  # value2をserver側で識別するため頭にAをつける。:は終端文字。文字列が連結した時にサーバ側でsplitするため。
                        print (value1_str) # デバッグ用に送信する値を表示
                        client.publish(topic[target],value1_str)
                        #client_sock.send(value1_str.encode('utf-8'))
                        time.sleep(sleeptime) # 値を送ったら時間を空ける。この時間がない、もしくはサーバ側でGPIOを操作した後の休止時間よりある程度短い場合文字列が連結してサーバ側でエラーが出る

                    elif abs(value2_new - value2) > 20: # value2の値の微小な変化は送信しない
                        value2 = value2_new # value2の値を更新する

                        value2_str = 'B' + str(value2) + ':' # value2をserver側で識別するため頭にBをつける
                        print (value2_str) # デバッグ用に送信する値を表示
                        client.publish(topic[target],value2_str)
                        #client_sock.send(value2_str.encode('utf-8'))
                        time.sleep(sleeptime) # 値を送ったら時間を空ける。この時間がない、もしくはサーバ側でGPIOを操作した後の休止時間よりある程度短い場合文字列が連結してサーバ側でエラーが出る
                elif e.type == pygame.locals.JOYBUTTONDOWN:
                    print(e.button)
                    if e.button == 2:
                        target = 0;
                        print(topic[target]);
                        client.publish("PicoRover/change","1st");
                    elif e.button == 3:
                        target = 1;
                        print(topic[target]);
                        client.publish("PicoRover/change","2nd");
                    elif e.button == 1:
                        target = 2;
                        print(topic[target]);
                        client.publish("PicoRover/change","3rd");
                    elif e.button == 0:
                        target = 3;
                        print(topic[target]);
                        client.publish("PicoRover/change","stop");
                    if e.button == 7:
                        print ('E:')
                        client.publish(topic[0],'E:')
                        client.publish(topic[1],'E:')
                        client.publish(topic[2],'E:')
                        pygame.quit()
                        sys.exit()

                    else:
                        pass
            timer_latest = datetime.datetime.now()
            delta = timer_latest - timer_old
            timer = delta.total_seconds()
            if timer >= 0.2:
                timer_old = datetime.datetime.now()
                client.publish(topic[0],'S:')
                client.publish(topic[1],'S:')
                client.publish(topic[2],'S:')                    
                print ('S:')

    except KeyboardInterrupt:
        print ('')
        print (u'Keyboardinterrupt')

    finally:
        client.publish(topic[0],'E:')
        client.publish(topic[1],'E:')
        client.publish(topic[2],'E:')
        print (u'-------EXIT-------')
        pygame.quit()
        sys.exit()



if __name__ == '__main__':
    args = sys.argv  # コマンドラインから引数を格納
    JoystickDetection(args[1])

# end
