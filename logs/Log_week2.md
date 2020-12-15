# Project Report - Week 2

[TOC]

# SI100B Project Report - GPIO

Please submit this report as a PDF file along with your code to receive full score of the project. 

## Workload Division

- 颜毅恒（yanyh1@shanghaitech.edu.cn）& 彭琬迪（pengwd@shanghaitech.edu.cn)：

  Study the documentations and figure out how to realize the requirements. Write the project report.

- 苏慧哲（suhzh@shanghaitech.edu.cn or vhtmscyo@gmail.com):

  Write python program .

## Preliminary Comment

#### references

- [GPIO - Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)
- [gpiozero](https://gpiozero.readthedocs.io/en/stable/)
- [week2.pdf](https://piazza.com/class_profile/get_resource/keihltlrsa273/kifwk7y7i8b374)

#### difficulties

- One of the LEDs is broken.

## Control the LED

#### The connection of LEDs to Pi

| LEDs  | GPIO pins |
| ----- | --------- |
| LED 0 | GPIO 26   |
| LED 1 | GPIO 19   |
| LED 2 | GPIO 12   |
| LED 3 | GPIO 5    |

The picture of Pi is as follows:

![pi pic](C:\Users\lenovo\Desktop\pi pic.png)

#### Class for LED control & How to determine which LED to control

- Class `BaseController` is used to control the LEDs.

- We have a private member in the class called `__digit` that contains 4 PWMLED instances as a list to control different LEDs.

  ```python
  class BaseController:
      def __init__(self):
          kStich = [26, 19, 12, 5]
          self.__digit = [
              PWMLED(i, initial_value=0, frequency=120) for i in kStich
          ]
  
      def work_once(self, num):
          print("NUM:", num)
          if num == 0:
              for i in range(3):
                  self.__digit[0].value = self.__digit[1].value = 1
                  sleep(0.2)
                  self.__digit[0].value = self.__digit[1].value = 0
                  sleep(0.2)
          elif num > 15:
              for i in range(3):
                  self.__digit[2].value = self.__digit[3].value = 1
                  sleep(0.2)
                  self.__digit[2].value = self.__digit[3].value = 0
                  sleep(0.2)
          else:
              for i in range(4):
                  self.__digit[i].value = num % 2
                  num //= 2
  
  ```

  

## Integration with the Crawler

#### How to differ importing the module from running directly

The value of `__name__` is set to `__main__` when the module is run as a main program and to the module's name when the module is imported by another module. We only need to check `if __name__ == '__main__'` to differ importing situation from running directly.

```python
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        kLatitude = float(sys.argv[1])
        kLongitude = float(sys.argv[2])
    else:
        kLatitude = 31.17940
        kLongitude = 121.59043
    crl = FlightAwareCrawler((kLatitude, kLongitude),
                             (kLatitude + 0.35, kLongitude - 0.35))
    state = State()
    for i in range(5):
        crl.spin(max_loop=1)
        state.spin(max_loop=1)  
```

