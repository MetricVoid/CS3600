from NeuralNet import NeuralNet, buildNeuralNet
import Testing
import sys

if __name__ == '__main__':
    accuracy_pen = [[] for i in range(0, 41, 5)]
    hidden_layer_pen = [[i] for i in range(0, 41, 5)]

    accuracy_car = [[] for i in range(0, 41, 5)]
    hidden_layer_car = [[i] for i in range(0, 41, 5)]

    with open('q6_result.txt', 'a') as f:
        f.write('RESULT FOR PEN: \n')

    # for each of hidden layer
    for i in range(len(hidden_layer_pen)):
        # run 5 trials
        print 'now testing with hidden layer: ', hidden_layer_pen[i]
        for j in range(5):
            testPen = Testing.testPenData(hiddenLayers=hidden_layer_pen[i])
            accuracy_pen[i].append(testPen[1])
        with open('q6_result.txt', 'a') as f:
            f.write('Hidden Layer: ' + str(hidden_layer_pen[i]) + '\t' + 'Max: ' + str(max(accuracy_pen[i])) + 'Average: ' + str(Testing.average(accuracy_pen[i])) + 'STD: ' + str(Testing.stDeviation(accuracy_pen[i])) + '\n')

    print 'NOW START TO TEST WITH CAR'
    with open('q6_result.txt', 'a') as f:
        f.write('\n')
        f.write('RESULT FOR CAR:\n')
    # for each of hidden layer
    for i in range(len(hidden_layer_car)):
        # run 5 trials
        print 'now testing with hidden layer: ', hidden_layer_car[i]
        for j in range(5):
            testCar = Testing.testCarData(hiddenLayers=hidden_layer_car[i])
            accuracy_car[i].append(testCar[1])
        with open('q6_result.txt', 'a') as f:
            f.write('hl: ' + str(hidden_layer_car[i]) + '\t' + 'Max: ' + str(max(accuracy_car[i])) + 'Average: ' + str(Testing.average(accuracy_car[i])) + 'STD: ' + str(Testing.stDeviation(accuracy_car[i])) + '\n')
