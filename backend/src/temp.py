import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
import pandas as pd
import numpy as np
from datetime import *
from src.utils import *
from src.utils import *
import os


def mean_absolute_percentage_error(y_true, y_pred):
    ads = []
    for i in range(0, len(y_true)):
        ad = 1. * (y_true[i, 0] - y_pred[i, 0]) / (y_true[i, 0] + 1) + \
             1. * (y_true[i, 1] - y_pred[i, 1]) / (y_true[i, 1] + 1)
        ads.append(ad)
    return ads


class seq2seq(nn.Module):
    def __init__(self, input_dim1, input_dim2, hid_dim, output_dim):
        super(seq2seq, self).__init__()
        self.embedding_hour = nn.Embedding(24, 1)
        self.embedding_week = nn.Embedding(7, 1)

        self.encode = nn.LSTM(input_dim1, hid_dim, num_layers=1)
        self.decode = nn.LSTM(input_dim2, hid_dim, num_layers=1)
        self.out = nn.Linear(hid_dim, output_dim)

    def forward(self, x, trg, isTrain):
        x1 = self.embedding_hour(x[:, :, -1].long())
        x2 = self.embedding_week(x[:, :, -2].long())
        encode_len = x.shape[0]
        batch_size = x.shape[1]

        x_input = torch.cat([x1, x2, x[:, :, :-2]], 2)

        outputs, encode_state = self.encode(x_input)

        decode_len = trg.shape[0]
        batch_size = trg.shape[1]
        outputs = torch.zeros(decode_len, batch_size, 2)

        for t in range(decode_len):
            if t == 0:
                decode_input = torch.zeros_like(trg[0, :, :])
                h_next = encode_state
            else:
                decode_input = trg[t, :, :] if isTrain else prediction
            h_now = h_next
            decode_output, h_next = self.decode(decode_input.reshape(1, batch_size, 2), h_now)
            prediction = self.out(decode_output.squeeze(0))
            outputs[t] = prediction
        return outputs


class Temp():
    def __init__(self):

        data = get_data("data/UnicomBJ_flows.h5")
        cur_flow = [data[:, 0, :, :].reshape((len(data), -1)), data[:, 1, :, :].reshape((len(data), -1))]
        self.flows = np.concatenate(cur_flow, axis=1)
        zero_index = self.flows == 0
        self.flows[zero_index] = 1
        self.flows = np.log(self.flows)

    def predict(self, now_time):
        td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds() // 3600)

        if td < 24:
            return None

        x = np.array([])
        for k in range(0, 1024):
            inputs = []
            for i in range(td - 24, td):
                cur_time = now_time + timedelta(hours=i - 24)
                cur_input = [self.flows[i, k], self.flows[i, k + 1024], cur_time.weekday(),
                             1 if cur_time.weekday() > 5 else 0,
                             1 if datetime(2017, 9, 30) < cur_time < datetime(2017, 10, 9) else 0,
                             cur_time.hour]
                inputs.append(cur_input)
            if x.shape[0] == 0:
                x = np.array([inputs])
            else:
                x = np.concatenate([x, [inputs]], axis=0)

        y = np.zeros(shape=(1024, 2, 2))
        model = torch.load("model/ad.01_b128_lambda_10.pkl", map_location=torch.device('cpu'))
        model.eval()

        x = torch.from_numpy(x).float()
        y = torch.from_numpy(y).float()

        x1 = x.permute(1, 0, 2)
        y1 = y.permute(1, 0, 2)

        pred = model(x1, y1, False).detach().numpy()
        pred = pred[0, :, :].reshape(1024, -1)
        return np.exp(pred)

    def get_temp_ad(self, inflow, outflow, now_time):
        td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds()//3600)

        if td < 24:
            return None

        for i in range(0, 1024):
            if inflow[i] == 0:
                inflow[i] = 1
            if outflow[i] == 0:
                outflow[i] = 1

        inflow = np.log(inflow)
        outflow = np.log(outflow)

        y_real = np.concatenate([inflow, outflow], axis=1)
        x = np.array([])

        for k in range(0, 1024):
            inputs = []
            for i in range(td - 24, td):
                cur_time = now_time + timedelta(hours=i - 24)
                cur_input = [self.flows[i, k], self.flows[i, k + 1024], cur_time.weekday(),
                             1 if cur_time.weekday() > 5 else 0,
                             1 if datetime(2017, 9, 30) < cur_time < datetime(2017, 10, 9) else 0,
                             cur_time.hour]
                inputs.append(cur_input)
            if x.shape[0] == 0:
                x = np.array([inputs])
            else:
                x = np.concatenate([x, [inputs]], axis=0)

        y = np.zeros(shape=(1024, 2, 2))

        model = torch.load("model/ad.01_b128_lambda_10.pkl", map_location=torch.device('cpu'))
        model.eval()

        x = torch.from_numpy(x).float()
        y = torch.from_numpy(y).float()

        x1 = x.permute(1, 0, 2)
        y1 = y.permute(1, 0, 2)

        pred = model(x1, y1, False).detach().numpy()
        pred = pred[0, :, :].reshape(1024, -1)

        res = abs(pred - y_real)
        maxs = np.max(res, axis=0)
        mins = np.min(res, axis=0)
        for i in range(0, res.shape[1]):
            res[:, i] = (res[:, i]-mins[i])/maxs[i]

        return res
