import time

import torch.nn as nn
import torch.nn.functional as F
import torch
import torch.optim as optim
import datetime
import numpy as np

"""
train
2 [champs] -> 1 champs
3 [champs]
...

test
2 [champs] -> 1 champs
3 [champs]
...
"""

#from keras.preprocessing.image import load_img
#import cv2
#from tqdm import tqdm
from predict.edit_data import EditData

def module2():
    rebuild_data = True
    if rebuild_data:
        e = EditData()
        e.read_champions("C:/Users/theerik/PycharmProjects/tft/data/champions.json")
        # at which point would like to start "accepting" data to training data
        # its better if date is recent or last patch as metas change and so does the best comp
        date = "23/06/2021"
        date_number = int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())) * 1000

        e.make_training_data(earl_game=False,
                             add_remove=False,
                             shuffle_placements=10,
                             game_time=date_number)

    training_data = np.load("training_data.npy", allow_pickle=True)
    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.linear = nn.Linear(63, 59)

            line21 = 128
            self.linear21 = nn.Linear(in_features=63, out_features=line21)
            self.linear22 = nn.Linear(in_features=line21, out_features=59)

            line31 = 64
            line32 = 64
            self.linear31 = nn.Linear(in_features=63, out_features=line31)
            self.linear32 = nn.Linear(in_features=line31, out_features=line32)
            self.linear33 = nn.Linear(in_features=line32, out_features=59)

            line41 = 64
            line42 = 128
            line43 = 64
            self.linear41 = nn.Linear(in_features=63, out_features=line41)
            self.linear42 = nn.Linear(in_features=line41, out_features=line42)
            self.linear43 = nn.Linear(in_features=line42, out_features=line43)
            self.linear44 = nn.Linear(in_features=line43, out_features=59)

        def forward(self, x):
            # x = F.relu(self.linear21(x))
            # x = self.linear22(x)

            x = F.relu(self.linear31(x))
            x = F.relu(self.linear32(x))
            x = self.linear33(x)

            # x = F.relu(self.linear41(x))
            # x = F.relu(self.linear42(x))
            # x = F.relu(self.linear43(x))
            # x = self.linear44(x)

            # # apply sigmoid activation to get all the outputs between 0 and 1
            # x = torch.sigmoid(x)
            # x = self.linear(x)
            return x

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    net = Net().to(device)

    # criterion_multioutput = nn.CrossEntropyLoss()
    criterion = nn.BCEWithLogitsLoss()
    # criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)

    val_pct = 0.1
    val_size = int(len(training_data) * val_pct)

    X = torch.Tensor([i[0] for i in training_data])  #.view(-1, 7, 10)
    y = torch.Tensor([i[1] for i in training_data])

    print(len(X), "len")
    print(val_size, "val_size")

    train_X = X[:-val_size]
    train_y = y[:-val_size]

    test_X = X[-val_size:]
    test_y = y[-val_size:]

    # main loop
    batch_size = 32
    epochs = 50
    net.train()
    for epoch in range(epochs):
        for i in range(0, len(train_X), batch_size):
            batch_X = train_X[i:i + batch_size]
            batch_y = train_y[i:i + batch_size]

            # test if it actually learn from inputs
            # a = torch.randn(len(batch_X), 63)
            # output = net(a)
            output = net(batch_X)
            loss = criterion(output, batch_y)

            # backward
            # net.zero_grad()
            optimizer.zero_grad()
            loss.backward()

            optimizer.step()
        print(epoch, loss)

    # check accuracy
    correct = 0
    total = 0
    streak8 = 0
    streak7 = 0
    streak6 = 0
    streak5 = 0
    streak4 = 0
    streak3 = 0
    streak2 = 0
    streaktotal = 0
    wrong = 0
    confident_ratio = 0.5
    net.eval()

    # def comp_tracker(best):
    #     comp1 = [56, 46, 23, 29, 34, 6, 28, 20]  # night yasuo
    #     comp2 = [14, 4, 33, 12, 38, 58, 20, 54]  # abo revenants
    #     comp3 = [9, 41, 31, 37, 12, 15, 8, 54]  # karma
    #     comp4 = [10, 30, 45, 16, 7, 36, 38, 51]  # forgotten
    #     c1 = 0
    #     c2 = 0
    #     c3 = 0
    #     c4 = 0
    #     for i in best:
    #         nr = int(i)
    #         if nr in comp1:
    #             c1 += 1
    #         if nr in comp2:
    #             c2 += 1
    #         if nr in comp3:
    #             c3 += 1
    #         if nr in comp4:
    #             c4 += 1
    #     c = max([c1,c2,c3,c4])
    #     if c >= 10:
    #         if c == c1:
    #             return comp1
    #         if c == c2:
    #             return comp2
    #         if c == c3:
    #             return comp3
    #         if c == c4:
    #             return comp4
    #     return best

    with torch.no_grad():
        for i in range(len(test_X)):

            real_classes = test_y[i]
            real_champs = []
            for j in range(len(real_classes)):
                if real_classes[j] == 1:
                    real_champs.append(j)

            net_out = net(test_X[i])
            outputs = torch.sigmoid(net_out)
            outputs = outputs.detach().cpu()

            # confident_outputs = []
            # for i in range(len(outputs)):
            #     if outputs[i] > confident_ratio:
            #         confident_outputs.append((i, outputs[i]))
            #     # print(i, outputs[i])
            # confident_outputs.sort(key=lambda x: x[1], reverse=True)
            # size = len(confident_outputs)
            # if size > len(real_champs):
            #     size = len(real_champs)

            size = len(real_champs)
            # size = 9
            sorted_indices = np.argsort(outputs)
            best = sorted_indices[-size:]
            # best = comp_tracker(best)
            streak = 0
            for j in best:
                a = int(j)
                if a == 0:
                    break
                elif a in real_champs:
                    streak += 1
                    correct += 1
                else:
                    wrong += 1
                total += 1
            if streak >= 8:
                streak8 += 1
            if streak >= 7:
                streak7 += 1
            if streak >= 6:
                streak6 += 1
            if streak >= 5:
                streak5 += 1
            if streak >= 4:
                streak4 += 1
            if streak >= 3:
                streak3 += 1
            if streak >= 2:
                streak2 += 1
            streaktotal += 1

    print(correct, wrong)
    print("Acc: ", round(correct / (correct + wrong), 3) * 100)
    print("Acc8: ", round(streak8 / streaktotal, 3) * 100)
    print("Acc7: ", round(streak7 / streaktotal, 3) * 100)
    print("Acc6: ", round(streak6 / streaktotal, 3) * 100)
    print("Acc5: ", round(streak5 / streaktotal, 3) * 100)
    print("Acc4: ", round(streak4 / streaktotal, 3) * 100)
    print("Acc3: ", round(streak3 / streaktotal, 3) * 100)
    print("Acc2: ", round(streak2 / streaktotal, 3) * 100)
    torch.save(net.state_dict(), "neuralnetwork2.pth")
    # Full random (9):
    # Acc: 29.4
    # Acc8: 0.3
    # Acc7: 1.9
    # Acc6: 7.5
    # Acc5: 17.0
    # Acc4: 28.499999999999996
    # Acc3: 43.1
    # Acc2: 64.8

    # Acc:  33.4
    # Acc5:  19.1
    # Acc4:  33.300000000000004
    # Acc3:  50.9
    # Acc2:  72.39999999999999
    # neuralnetwork.pth

if __name__ == '__main__':
    # a = datetime.datetime.fromtimestamp(1623107793.155)
    # print(a)
    module2()
