# i2c通信，1 secごとに地磁気データを出力する関数
import time
import board
import adafruit_lsm303dlh_mag
import csv
import sys

def percentpick(listdata):
    n = int(len(listdata) *p/100)
    listdata = sorted(listdata) # 昇順
    min = listdata[n-1]
    max = listdata[len(listdata)-n]
    return max, min

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

t = 0
duration = 0.5
maglist = []

while t <= 5:
    t += duration
    time.sleep(duration)
i = 1
try:
    with open('mag.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['magX_max', 'magX_min', 'magY_max', 'magY_min', 'magZ_max', 'magZ_min'])
        f.close()
    while True:
  
        t = 0
        while t <= 60:
            mag_x, mag_y, mag_z = sensor.magnetic
            maglist.append([mag_x,mag_y,mag_z])
            print('Magnetometer (gauss): ({0:10.3f}, {1:10.3f}, {2:10.3f})'.format(mag_x, mag_y, mag_z))
            print('')
        
            t += duration
            time.sleep(duration)
    

        # 最大値，最小値の算出
        p = 5 # 上位何%をpickするか
        Xmax, Xmin = percentpick(mag_x)
        Ymax, Ymin = percentpick(mag_y)
        Zmax, Zmin = percentpick(mag_z)
       
        with open('mag.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([Xmax, Xmin, Ymax, Ymin, Zmax, Zmin])
            f.close()
        with open(f'lsm303_No{i}.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(maglist)
        i += 1
        time.sleep(300)

except KeyboardInterrupt:
    
    sys.exit()
