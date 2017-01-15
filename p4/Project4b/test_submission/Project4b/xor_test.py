import random
from NeuralNet import buildNeuralNet

xor_data = [[[0, 0], [1, 0]], [[0, 1], [0, 1]], [[1, 0], [0, 1]], [[1, 1], [1, 0]]]

xor_data = xor_data * 125

# shuffle the data
# random.seed(13)
random.shuffle(xor_data)

# split into 70:30 train:test
train_num = 0.7 * len(xor_data)

xor_train = xor_data[:int(train_num)]
xor_test = xor_data[int(train_num):]
xor_data = [xor_train, xor_test]

count_perceptron = 3
hiddenLayers = [count_perceptron]
clf = buildNeuralNet(xor_data, maxItr=200, hiddenLayerList=hiddenLayers)
