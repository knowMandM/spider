# 
#
#
#
import settings

f=open(settings.LOG_PATH, "w+")

def log(*args):
    for i in range(len(args)):
        if (i + 1 == len(args)):
            print(args[i])
            print(args[i], file = f)
        else:
            print(args[i], ' ', end = "")
            print(args[i], ' ', end = "", file = f)
    f.flush()