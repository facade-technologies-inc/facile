from myFirstAPI.application import Application

myApp = Application()
myApp.start()
print(myApp.default3('My name is Andrew ', 'KIRIMA!'))
myApp.stop()