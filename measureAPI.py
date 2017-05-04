from sys import argv
import json
import datetime
import matplotlib.pyplot as plt
import csv
import operator

'''
dataPersing function opens the json file obtained from greenspector containing measured data. then it retrives the
timestamp and platform discharge(AH_PL) values from the data and returns the following lists of values:
 1.measuredTime 2.batteryStat
'''
class energyConsumption:
    def dataPersing(self, filename):
        # in open filename must contain the gsptfile as input.
        global timedata
        with open(filename) as json_data:
            data_list = json.load(json_data)

            # list for storing timestamps
            timelist = []
            #list for storing platform discharge values (AH_PL)
            batteryStat = []

            #insert timestamps into the timelist
            for data in data_list:
                for msr_data in data["measures"]:
                    timelist.append(datetime.datetime.fromtimestamp(msr_data["time"] / 1e3))
                    #insert AH_PL values into batastatlist
                    if "AH_PL" in msr_data["values"]:
                        batteryStat.append(int(msr_data["values"]["AH_PL"]) / 1000)

        #declaring variable for storing time intervals
        measurementTimeIntervals = timelist[0] - timelist[0]
        #list for storing time intervals
        measuredTimes = []

        #insert values into measuredTimes list
        for index,item in enumerate(timelist):
            if index < len(timelist)-1:
                x = timelist[index+1]-timelist[index]
                measurementTimeIntervals = x + measurementTimeIntervals
                measuredTimes.append(measurementTimeIntervals)

        measuredTimes.insert(0, (measurementTimeIntervals - measurementTimeIntervals))
        timeDelta = str(measuredTimes[len(measuredTimes)-1]).split(':')

        timedata = int(timeDelta[1]) * 60 + float(timeDelta[2])
        meanConsumption=(sum(batteryStat)/timedata)/1e6
        return measuredTimes, batteryStat, meanConsumption

    def plotData(self, x):
        time=x[0]
        value=x[1]
        timeData = []
        for data in time:
            temp =str(data).split(':')
            timeData.append(float(temp[2]))

        # Common sizes: (10, 7.5) and (12, 9)
        plt.figure(figsize=(16, 7.5))

        # Remove the plot frame lines.
        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Ensure that the axis ticks only show up on the bottom and left of the plot.
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_axis_bgcolor('white')
        plt.title("Platform Discharge of a Device due to an App over Time", fontsize=16)

        plt.plot(timeData, value)


        plt.xticks(range(0, 61, 1), [str(x) for x in range(0, 61, 1)], fontsize=10)
        plt.yticks(range(5, max(value)+5, 5), [str(x) for x in range(5, max(value)+5, 5)], fontsize=10)
        plt.ylim(ymin=0)
        plt.gca()
        plt.grid(True)
        plt.ylabel("Platform discharge(microAh)", fontsize=12)
        plt.xlabel("Measured Time (s)", fontsize=12)
        plt.savefig('graph.png')
        #plt.show()


class APIcost:
    def measureCost(self, tracefile, measureConsumption):
        rawfile= []
        tstart=[]
        excl=[]
        APIname=[]
        APIcost=[]
        APIcost_file = open(tracefile, 'r')
        reader = csv.reader(APIcost_file)
        for row in reader:
            rawfile.append(row)
            tstart.append(int(row[1]))
            excl.append(int(row[5]))
            APIname.append(row[7])
        for data in excl:
            APIcost.append(int(data)*measureConsumption)
        # store the API method name with its consumption
        map_APInameAndCost = zip(APIname, APIcost)
        # reduce the mapAPInameandCost list by adding the values of same API method calls and make a dictionary
        reduce_APInameAndCost = dict()
        for each in map_APInameAndCost:
            key, val = each
            if key in reduce_APInameAndCost:
                reduce_APInameAndCost[key] += val
            else:
                reduce_APInameAndCost[key] = val
        # sort the reduced dictionary
        sorted_reducedList = sorted(reduce_APInameAndCost.items(), key=operator.itemgetter(1))
        with open('APIConssumptionMeasures.csv', 'wb') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['methodName', 'value'])
            for data in sorted_reducedList:
                csv_out.writerow(data)

script, gsptfile, tracefile = argv


gsptObj=energyConsumption()
costAPI=APIcost()
x=gsptObj.dataPersing(gsptfile)
gsptObj.plotData(x)
y=costAPI.measureCost(tracefile, x[2])


