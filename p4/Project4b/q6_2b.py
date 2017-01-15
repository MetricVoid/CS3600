from NeuralNet import NeuralNet, buildNeuralNet
import Testing
import sys

if __name__ == '__main__':

    accuracy_car = [[] for i in range(0, 41, 5)]
    hidden_layer_car = [[i] for i in range(0, 41, 5)]

    with open('q6_result_car.txt', 'a') as f:
        f.write('Hidden Layer, Max, Mean, STD\n')
    # for each of hidden layer
    for i in range(len(hidden_layer_car)):
        # run 5 trials
        print 'now testing with hidden layer: ', hidden_layer_car[i]
        for j in range(5):
            testCar = Testing.testCarData(hiddenLayers=hidden_layer_car[i])
            accuracy_car[i].append(testCar[1])
        with open('q6_result_car.txt', 'a') as f:
            f.write(str(hidden_layer_car[i]) + ',' + str(max(accuracy_car[i])) + ',' + str(Testing.average(accuracy_car[i])) + ',' + str(Testing.stDeviation(accuracy_car[i])) + '\n')
