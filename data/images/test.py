import cv2
import numpy as np
import mss
import time

def main():

    net = cv2.dnn.readNet("network/yolov3_training_last.weights", "network/yolov3_testing.cfg")

    classes = []

    with open("network/classes.txt", "r") as f:
        classes = f.read().splitlines()

    monitor = {"top": 50, "left": 300, "width": 900, "height": 300}

    while True:
        last_time = time.time()
        img = cv2.cvtColor(np.array(mss.mss().grab(monitor)), cv2.COLOR_RGBA2RGB)

        height, width, _ = img.shape

        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)

        # for b in blob:
        #     for n, imgblob in enumerate(b):
        #         cv2.imshow(str(n), imgblob)

        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)

        boxes = []
        confs = []
        class_ids = []


        acc = 0.01

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                conf = scores[class_id]
                if conf > acc:
                    cenx = int(detection[0] * width)
                    ceny = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(cenx - w / 2)
                    y = int(ceny - h / 2)

                    boxes.append([x,y,w,h])
                    confs.append((float(conf)))
                    class_ids.append(class_id)

        # print(len(boxes))

        # 0.4 default
        # print(boxes)
        indexes = cv2.dnn.NMSBoxes(boxes, confs, acc, 0.4)
        # try:
        #     indexes = cv2.dnn.NMSBoxes(boxes, confs, acc, 0.4)
        # except TypeError as exc:
        #     print(str(exc).find("index"))
        #     return
        # print(indexes.flatten())

        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(len(boxes), 3))

        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confs[i], 2))
                color = colors[i]
                cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
                print(label)
                cv2.putText(img, label + " " + confidence, (x, y + 20), font, 2, (255,255,255), 2)

        cv2.imshow("b", img)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
        print("time:", time.time() - last_time)
        time.sleep(0.01)

if __name__ == '__main__':
    main()
