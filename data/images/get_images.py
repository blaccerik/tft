import mss
import time
import cv2
import numpy as np
from PIL import Image


def main():
    time.sleep(1.5)
    print("-------")
    for i in range(2):
        nr = int(time.time() * 100)
        name = f"{nr}.png"
        mss.mss().shot(output=name)
        print(i, "done")
        time.sleep(1)
    pass

def main2():
    # used to get images of the champions in store
    time.sleep(0)
    monitor = {"top": 772, "left": 319, "width": 833, "height": 122}
    array = cv2.cvtColor(np.array(mss.mss().grab(monitor)), cv2.COLOR_RGBA2RGB)
    # 167 , 168, 168, 168, 168
    aa = [0, 167, 335, 503, 671]
    for i in range(5):
        nr = int(time.time() * 1000)
        name = f"{nr}.png"
        x = aa[i]
        a = array[:, x:x + 162]
        cv2.imshow("a", a)
        print(a.shape)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
        time.sleep(0.5)
        cv2.imwrite(name, a)

if __name__ == '__main__':
    main()
    # main2()