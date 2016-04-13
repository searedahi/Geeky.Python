import time
import ThermometerService


print('hello')

Tempy = ThermometerService.ThermometerService()
print('starting')
#Tempy.runService()

while True:
    print('loop')   
    print('{0} Degrees F').format(Tempy.CurrentFarenheight())
    time.sleep(15)
    pass