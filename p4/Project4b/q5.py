from NeuralNet import NeuralNet, buildNeuralNet
import Testing
import sys

if __name__ == '__main__':
    accuracy_pen = []
    accuracy_car = []

    for i in range(5):
        testPen = Testing.testPenData()
        accuracy_pen.append(testPen[1])

    for i in range(5):
        testCar = Testing.testCarData()
        accuracy_car.append(testCar[1])

    print '\n'
    print '-----------STATS FOR PEN-----------'
    print 'max is: ', max(accuracy_pen)
    print 'avg is: ', Testing.average(accuracy_pen)
    print 'std is: ', Testing.stDeviation(accuracy_pen)


    print '-----------STATS FOR CAR-----------'
    print 'max is: ', max(accuracy_car)
    print 'avg is: ', Testing.average(accuracy_car)
    print 'std is: ', Testing.stDeviation(accuracy_car)

    with open('q5_result.txt', 'w') as f:
        f.write('------STATS FOR PEN------\n')
        f.write('max is: ' + str(max(accuracy_pen)) + '\n')
        f.write('avg is: ' + str(Testing.average(accuracy_pen)) + '\n')
        f.write('std is: ' + str(Testing.stDeviation(accuracy_pen)) + '\n')
        f.write('\n')

        f.write('------STATS FOR CAR------\n')
        f.write('max is: ' + str(max(accuracy_car)) + '\n')
        f.write('avg is: ' + str(Testing.average(accuracy_car)) + '\n')
        f.write('std is: ' + str(Testing.stDeviation(accuracy_car)) + '\n')
        f.write('\n')
