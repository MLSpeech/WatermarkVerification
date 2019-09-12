import numpy as np
import matplotlib.pyplot as plt
from csv import DictReader, DictWriter

model_name = 'mnist.w.wm'
vals = {}

datafile = open('./data/results/{}.WatermarkVerification1SecondBestPrediction.csv'.format(model_name))
file_reader = DictReader(datafile)
vals[1] = np.array([float(line['sat-epsilon']) for line in file_reader])
datafile.close()
for i in range(2,8):
    datafile = open('./data/results/problem3/WatermarkVerification3.{}.wm.csv'.format(i))
    file_reader = DictReader(datafile)
    vals[i] = np.array([float(line['sat-epsilon']) for line in file_reader])
    datafile.close()

# x = range(1,8)
# average = np.array([np.average(vals[i]) for i in x])
# maximum = np.array([np.max(vals[i]) for i in x])
# minimum = np.array([np.min(vals[i]) for i in x])
# plt.bar(x, average)
# plt.xlabel('Number of Watermark Images')
# plt.ylabel('epsilon')
# plt.savefig('./data/results/problem3/{}.WatermarkVerification3.average.png'.format(model_name))
# plt.bar(x, maximum)
# plt.xlabel('Number of Watermark Images')
# plt.ylabel('epsilon')
# plt.savefig('./data/results/problem3/{}.WatermarkVerification3.maximum.png'.format(model_name))
# plt.bar(x, minimum)
# plt.xlabel('Number of Watermark Images')
# plt.ylabel('epsilon')
# plt.savefig('./data/results/problem3/{}.WatermarkVerification3.minimum.png'.format(model_name))
# # plt.xticks(np.arange(min(sat_vals), max(sat_vals), 0.1))

# datafile = open('./data/results/problem2/{}.WatermarkVerification2.csv'.format(model_name))
# file_reader = DictReader(datafile)

# sat_vals = np.array([float(line['sat-epsilon']) for line in file_reader])
# sat_vals = np.sort(sat_vals)
# numbers = np.array(range(1, len(sat_vals)+1))
# plt.step(numbers, sat_vals)
# plt.xlabel('Number of Watermark Images')
# plt.ylabel('epsilon')
# plt.savefig('./data/results/problem2/{}.WatermarkVerification2.png'.format(model_name))
# # plt.xticks(np.arange(min(sat_vals), max(sat_vals), 0.1))
# # plt.show()


