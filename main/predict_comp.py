import torch.nn as nn
import torch.nn.functional as F
import torch
import torch.optim as optim
import numpy as np

training_data = np.load("training_comp.npy", allow_pickle=True)

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        line21 = 128
        self.linear21 = nn.Linear(in_features=7, out_features=line21)
        self.linear22 = nn.Linear(in_features=line21, out_features=22)

        line31 = 400
        line32 = 200
        self.linear31 = nn.Linear(in_features=7, out_features=line31)
        self.linear32 = nn.Linear(in_features=line31, out_features=line32)
        self.linear33 = nn.Linear(in_features=line32, out_features=22)

        line41 = 200
        line42 = 200
        line43 = 200
        self.linear41 = nn.Linear(in_features=7, out_features=line41)
        self.linear42 = nn.Linear(in_features=line41, out_features=line42)
        self.linear43 = nn.Linear(in_features=line42, out_features=line43)
        self.linear44 = nn.Linear(in_features=line43, out_features=22)

    def forward(self, x):
        # x = F.relu(self.linear21(x))
        # x = self.linear22(x)

        x = F.relu(self.linear31(x))
        x = F.relu(self.linear32(x))
        x = self.linear33(x)
        #
        # x = F.relu(self.linear41(x))
        # x = F.relu(self.linear42(x))
        # x = F.relu(self.linear43(x))
        # x = self.linear44(x)

        # # apply sigmoid activation to get all the outputs between 0 and 1
        # x = torch.sigmoid(x)
        x = F.softmax(x, dim=1)
        return x

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net = Net().to(device)

# criterion_multioutput = nn.CrossEntropyLoss()
# criterion = nn.BCEWithLogitsLoss()
criterion = nn.MSELoss()
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
batch_size = 64
epochs = 3
net.train()
for epoch in range(epochs):
    for i in range(0, len(train_X), batch_size):
        batch_X = train_X[i:i + batch_size]
        batch_y = train_y[i:i + batch_size]
        # test if it actually learn from inputs
        # a = torch.randn(len(batch_X), 7)
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
net.eval()
correct = 0
total = 0
dicta = {}
with torch.no_grad():
    for i in range(len(test_X)):
        real_class = torch.argmax(test_y[i])
        a = int(real_class)
        if a in dicta:
            dicta[a] += 1
        else:
            dicta[a] = 1
        net_out = net(test_X[i].view(-1, 7))
        predicted_class = torch.argmax(net_out)
        # print(predicted_class, real_class, test_X[i])
        # print(predicted_class)
        if predicted_class == real_class:
            correct += 1
        total += 1

    a = [4,4,4,4,4,4,4]
    b = torch.FloatTensor(a)
    net_out = net(b.view(-1, 7))
    print(net_out)
    predicted_class = torch.argmax(net_out)
    print(predicted_class)

    a = [2,2,2,2,2,2,2]
    b = torch.FloatTensor(a)
    net_out = net(b.view(-1, 7))
    print(net_out)
    predicted_class = torch.argmax(net_out)
    print(predicted_class)

    # a = [1,1,1,7,7,7,0]
    # b = torch.FloatTensor(a)
    # net_out = net(b.view(-1, 7))
    # print(net_out)
    # predicted_class = torch.argmax(net_out)
    # print(predicted_class)

print("Acc: ", round(correct / total, 3) * 100)
a = list(dicta.items())
a.sort(key=lambda x: x[1], reverse=True)
for i in range(10):
    b = a[i]
    nr = b[0]
    times = b[1]
    print(f"comp {nr} {round(times * 100 / total, 3)} %")
torch.save(net.state_dict(), "neuralnetwork.pth")
