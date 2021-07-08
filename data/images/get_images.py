import mss
import time

def main():
    time.sleep(5)
    print("------")
    for i in range(8):
        nr = int(time.time() * 100)
        name = f"{nr}.png"
        mss.mss().shot(output=name)
        print("done")
        time.sleep(2)
    pass

if __name__ == '__main__':
    main()