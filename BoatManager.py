import time
import ThermometerService


print('hello')

Tempy = ThermometerService.ThermometerService()
print('starting')
#Tempy.runService()

while True:
    print('loop')   
    print(Tempy.CurrentFarenheight 'F' )
    time.sleep(15)
    pass