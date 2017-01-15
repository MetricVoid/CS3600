from NeuralNet import NeuralNet, buildNeuralNet
import Testing
import sys

if __name__ == '__main__':

    accuracy_pen = [[] for i in range(0, 41, 5)]
    hidden_layer_pen = [[i] for i in range(0, 41, 5)]

    with open('q6_result_pen.txt', 'a') as f:
        f.write('Hidden Layer, Max, Mean, STD\n')
    # for each of hidden layer
    for i in range(len(hidden_layer_pen)):
        # run 5 trials
        print 'now testing with hidden layer: ', hidden_layer_pen[i]
        for j in range(5):
            testPen = Testing.testPenData(hiddenLayers=hidden_layer_pen[i])
            accuracy_pen[i].append(testPen[1])
        with open('q6_result_pen.txt', 'a') as f:
            f.write(str(hidden_layer_pen[i]) + ',' + str(max(accuracy_pen[i])) + ',' + str(Testing.average(accuracy_pen[i])) + ',' + str(Testing.stDeviation(accuracy_pen[i])) + '\n')
