# Here is how you can use your API!

# Import your API like this
from {name}.application import Application

# This statement isn't necessary, but it's good to have it when writing scripts
if __name__ == '__main__':

    # --- Starting Your Application --- #
    # To start your application, do
    myApp = Application().start()

    # You can also do this. Either way works:
    # myApp = Application()
    # myApp.start()
    # ---------------------- #

    # --- The Automation --- #
    # Below is where you use the functions you created, however you want. If you have an action pipeline called
    # "default", then all you have to do is:
    # myApp.default()
    #
    # If it has arguments, then:
    # myApp.default(arg1, arg2, arg3, etc)
    #
    # And if it returns values:
    # val1, val2, val3, etc = myApp.default(arg1, arg2, arg3, etc)
    #
    # You can take advantage of Python's built-in functions here to do some really cool things with your API,
    # or just loop your functions a couple times if you're doing some testing. It's up to you!

    # Just a small example

    # for task in todoList:
    #     if task.isBoring():
    #         myApp.automate(task)
    #
    # assert(life.isBetter())



    # ------------------------ #

    # --- Useful Functions --- #
    # We also offer some useful functions that make automating your application even more flexible
    #
    # If you want to wait a couple seconds for something to finish before running the next line, do:
    myApp.wait('2 s')

    # If you want a couple minutes instead, replace the s with an m.
    #
    # You can also pause your automation script's execution with
    myApp.pause(demo=True)

    # except, you know, without the demo=True part. I mean, unless you want the cool text
    # as if you were running this demo. It'll have the same functionality either way.

    # Finally, to stop your application, call the stop() function:
    myApp.stop()

    # You don't have to do this, but it's practical if you ever need it. Be careful though, because it is more
    # of a kill-switch: It will not ask you to save or give any warnings, the process will just be stopped.
