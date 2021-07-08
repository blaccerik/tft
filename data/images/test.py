import cv2
import numpy as np
import mss

net = cv2.dnn.readNet("network/yolov3_training_last.weights", "network/yolov3_testing.cfg")

classes = []

with open("network/classes.txt", "r") as f:
    classes = f.read().splitlines()

monitor = {"top": 100, "left": 100, "width": 1000, "height": 800}
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


acc = 0.5

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
indexes = cv2.dnn.NMSBoxes(boxes, confs, acc, 0.4)
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
        cv2.putText(img, label + " " + confidence, (x, y + 20), font, 2, (255,255,255), 2)


cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
