from api.application import Application

myApp = Application()
myApp.start()
print(myApp.default3('hello ', 'world!'))
myApp.stop()