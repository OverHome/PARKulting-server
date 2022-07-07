import os
import random
import shutil


def new_pic():
    fol = os.listdir("pic")
    mx = 0
    for i in fol:
        t = os.listdir("pic\\" + i)
        mx = max(mx, len(t))

    for i in fol:
        t = os.listdir("pic\\" + i)
        dell_folder("learn\\tren\\" + i)
        dell_folder("learn\\val\\" + i)
        dell_folder("learn\\test\\" + i)
        if not os.path.exists("learn\\tren\\" + i):
            os.mkdir("learn\\tren\\" + i)
        k = 0
        while k != mx:
            for l in t:
                shutil.copyfile("pic\\" + i + "\\" + l, "learn\\tren\\" + i + "\\" + i + "." + str(k) + ".jpg")
                k += 1
                if k == mx:
                    break
        if not os.path.exists("learn\\val\\" + i):
            os.mkdir("learn\\val\\" + i)
        if not os.path.exists("learn\\test\\" + i):
            os.mkdir("learn\\test\\" + i)
        for j in range(mx // 10):
            shutil.copyfile("pic\\" + i + "\\" + t[random.randint(0, len(t) - 1)],
                            "learn\\val\\" + i + "\\" + i + "." + str(k) + ".jpg")
            shutil.copyfile("pic\\" + i + "\\" + t[random.randint(0, len(t) - 1)],
                            "learn\\test\\" + i + "\\" + i + "." + str(k + 1) + ".jpg")
            k += 2


def dell_folder(st):
    if os.path.exists(st):
        shutil.rmtree(st, ignore_errors=True)
