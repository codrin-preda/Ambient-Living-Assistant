import speech_recognition as sr
import pyttsx3
import random
import csv
import datetime
import glob
import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
import os
from time import process_time_ns


diseasesNames = []
temperaturesLower = []
temperaturesUpper = []

bloodPressuresUpper = []
bloodPressuresLower = []

restingHeartRatesUpper = []
restingHeartRatesLower = []

healthyTemp = 36.5
healthyBloodPressure = 80
healthyRestingHR = 65

idealRoomTemp = 23
idealO2 = 25
idealC02 = 300


class User1:
    startDate = datetime.datetime(2020, 1, 1)

    def __init__(self, name, temperature, bloodPressure, restingHR):
        self.diseases = []
        self.name = name
        self.temperature = temperature
        self.bloodPressure = bloodPressure
        self.restingHR = restingHR

    def checkDiseases(self):
        self.diseases = []
        if self.temperature < 32 or self.temperature > 43:
            self.diseases.append("Critical Temperature!")
        if self.restingHR < 30 or self.restingHR > 120:
            self.diseases.append("Critical Heart Rate!")
        if self.bloodPressure < 50 or self.bloodPressure > 200:
            self.diseases.append("Critical Blood Pressure")

        for x in range(10):
            if (int(temperaturesLower[x]) < self.temperature < int(temperaturesUpper[x])) and (
                    int(bloodPressuresLower[x]) < self.bloodPressure < int(bloodPressuresUpper[x])) and (
                    int(restingHeartRatesLower[x]) < self.restingHR < int(restingHeartRatesUpper[x])):
                self.diseases.append(diseasesNames[x])

    def nextDay(self, roomTemp, o2Level, c02Level):                                                                                        #check diseases
        self.temperature = self.temperature + (idealRoomTemp/roomTemp * healthyTemp - self.temperature) / 2
        self.bloodPressure = self.bloodPressure + (idealO2/o2Level * healthyBloodPressure - self.bloodPressure) / 2
        self.restingHR = self.restingHR + (c02Level/idealC02 * healthyRestingHR - self.restingHR) / 2

        print(f"Temperature: {round(self.temperature,2)}, Blood Pressure: {self.bloodPressure}, Heart Rate: {self.restingHR}")
        print(f"Room Temperature: {roomTemp}, Oxygen: {o2Level}, C02: {c02Level}")
        print("----------------------------------")

        self.startDate = self.startDate + datetime.timedelta(days=1)

        data = [self.startDate.date(), round(self.temperature,2), round(self.bloodPressure,2), round(self.restingHR,2),round(roomTemp,2),round(o2Level,2),round(c02Level,2)]
        with open('output.csv', 'a', newline="" ) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(data)
        self.checkDiseases()
        if not self.diseases == []:
            print("DISEASE!!!!!!")
            print(self.diseases)

    def showCurrentDiseases(self):
        print("Current diseases:")
        for disease in self.diseases:
            print(disease)


class Environment:
    startDate = datetime.datetime(2020, 1, 1)

    def __init__(self, user, roomTemp, o2level, c02level):
        self.user = user
        self.roomTemp = roomTemp
        self.o2level = o2level
        self.c02level = c02level

    def checkUser(self):
        self.user.checkDiseases()

    def nextDay(self):                                                         #nex day+generating data.

        if not self.user.diseases == []:
            self.roomTemp = self.roomTemp + (idealRoomTemp - self.roomTemp)/2
            self.o2level = self.o2level + (idealO2 - self.o2level)/2
            self.c02level = self.c02level + (idealC02 - self.c02level)/2

        else:
            self.roomTemp += random.randint(-10, 10) / 10

            if self.o2level > 1:
                self.o2level += random.randint(-10, 10) / 10

            self.c02level += random.randint(-5, 12)

        self.user.nextDay(self.roomTemp, self.o2level, self.c02level)


def speak():
    print("Here you speak now, go!")                                 #speech recognition
    # Initialize the recognizer
    r = sr.Recognizer()

    # Loop infinitely for user to speak
    while (1):
        # Exception handling to handle exceptions at the runtime
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                # wait for a second to let the recognizer adjust the energy threshold based on the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                # listens for the user's input
                audio2 = r.listen(source2)
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                print("Did you say " + MyText)
                if int(MyText)== 1:
                    T.delete('1.0', END)
                    T.insert(tk.END, "You have selected Temperature ")
                    variable.set("1.Temperature")
                    break
                elif int(MyText)== 2:
                    T.delete('1.0', END)
                    T.insert(tk.END, "You have selected Blood Pressure ")
                    variable.set("2.Blood Pressure")
                    break
                elif int(MyText)== 3:
                    T.delete('1.0', END)
                    T.insert(tk.END, "You have selected Resting Heart Rate ")
                    variable.set("3.Resting Heart Rate")
                    break


                # SpeakText(MyText)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")

        continue

def goaction():                                         #submit action + process time
    t1_start = process_time_ns()


    startDate = datetime.datetime(2020, 1, 1)
    vitalValues = []
    vitalsDay = []
    day = 1
    plt.cla()

    print(variable.get())
    if variable.get() == "1.Temperature":
        col = 1
    elif variable.get() == "2.Blood Pressure":
        col = 2
    elif variable.get() == "3.Resting Heart Rate":
        col = 3

    d1 = entryText.get()
    d2 = entryText2.get()

    firstDate = datetime.datetime.strptime(d1, '%d/%m/%Y')
    secondDate = datetime.datetime.strptime(d2, '%d/%m/%Y')

    begin = firstDate-startDate
    end = (secondDate-firstDate)
    sum = 0.00
    average = 0.00
    ok = True


    if secondDate < firstDate:
        T.delete('1.0', END)
        T.insert(tk.END, "Please insert valid dates")
        ok = False

    if ok:
        nr = 0.00
        with open('output.csv', 'r') as file:
            reader = csv.reader(file)
            row = []
            i = 0
            for row in reader:
                if i>=begin.days and i <=(end.days+begin.days):
                    sum = sum+float(row[col])
                    vitalValues.append(float(row[col]))
                    vitalsDay.append(day)
                    day += 1
                    nr = nr+1.00
                i = i+1

    print("Sum = "+str(sum))
    print("Nr = " + str(nr))
    print(end.days)
    average = round(sum / nr, 2)

    T.delete('1.0', END)
    T2.delete('1.0', END)

    if variable.get() == "1.Temperature":
        res = "The average temperature of the user in the given period was:"+str(average)
    elif variable.get() == "2.Blood Pressure":
        res = "The average Blood Pressure of the user in the given period was:"+str(average)
    elif variable.get() == "3.Resting Heart Rate":
        res = "The average Resting Heart Rate of the user in the given period was:"+str(average)
    else:
        res = "Error"

    t1_stop = process_time_ns()
   # res=res+"\n the operation lasted "+str((t1_stop - t1_start)/100000)+"ms"
    process="the operation lasted "+str((t1_stop - t1_start)/100000)+"ms"

    T.insert(tk.END, res)
    T2.insert(tk.END, process)



    print("Elapsed time:", t1_stop, t1_start)

    print("Elapsed time during the whole program in nanoseconds:", t1_stop - t1_start)

    if ok:
        plt.plot(vitalsDay, vitalValues)
        plt.xlabel("Day")
        if col == 1:
            plt.ylabel("Temperature")
            plt.title("Temperature Data")
        elif col == 2:
            plt.ylabel("Blood Pressure")
            plt.title("Blood Pressure Data")
        else:
            plt.ylabel("Resting Heart Rate")
            plt.title("Resting Heart Rate Data")

        plt.show()



if __name__ == '__main__':

    with open('output.csv', 'w+') as output_file:
        output_file.truncate()

    listOfParameters = ["1.Temperature",  "2.Blood Pressure", "3.Resting Heart Rate"]

    i = 0
    with open('input.csv', 'r') as file:
        reader = csv.reader(file)
        row = []
        for row in reader:
            if i == 0:
                diseasesNames = row
            elif i == 1:
                temperaturesLower = row
            elif i == 2:
                temperaturesUpper = row
            elif i == 3:
                bloodPressuresLower = row
            elif i == 4:
                bloodPressuresUpper = row
            elif i == 5:
                restingHeartRatesLower = row
            elif i == 6:
                restingHeartRatesUpper = row
            i = i + 1

    userBob = User1("James", 37, 100, 80)
    environment = Environment(userBob, 25, 20, 330)
    environment.checkUser()

    while os.stat('output.csv').st_size< 300000:                           #generating data with a limit of file size
        environment.nextDay()
        print(os.stat('output.csv').st_size)
    userBob.showCurrentDiseases()
    with open('output.csv') as in_file:
        with open('outfinal.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)


#--------------------- GUI --------------------

    mw = tk.Tk()
    mw.title('GUI')
    mw.geometry("700x900")
    mw.resizable(0, 0)
    mw.configure(bg='#845EC2')


    info = tk.Label(text='Vitals average calculator', bg='#D65DB1', fg='black')
    info.place(x=260, y=10, width=140, height=25)

    info = tk.Label(text='Please input the dates:', bg='#FF6F91', fg='black')
    info.place(x=30, y=60, width=180, height=25)

    entryText = tk.Entry(bg='white', fg='black')
    entryText.place(x=270, y=60, width=100, height=25)

    entryText2 = tk.Entry(bg='white', fg='black')
    entryText2.place(x=430, y=60, width=100, height=25)

    btn1 = tk.Button(text='Speak to select vital', command=speak, bg='#FF6F91', fg='black')
    btn1.place(x=30, y=140, width=200, height=25)

    btn2 = tk.Button(text='Submit', command=goaction, bg='#FF6F91', fg='black')
    btn2.place(x=430, y=140, width=100, height=25)

    info = tk.Label(text='Result box', bg='#FF6F91', fg='black')
    info.place(x=240, y=240, width=180, height=30)

    T = tk.Text(mw, bg='#D65DB1', fg='black')
    T.place(x=180, y=300, width=300, height=100)
    T.insert(tk.END, "Results")

    T2 = tk.Text(mw, bg='#D65DB1', fg='black')
    T2.place(x=180, y=540, width=300, height=100)
    T2.insert(tk.END, "process time")

    info = tk.Label(text='*The starting date of the simulation is 01/01/2020 ', bg='#D65DB1', fg='black')
    info.place(x=180, y=450, width=300, height=25)

    variable = tk.StringVar(mw)
    variable.set(listOfParameters[0])
    w = OptionMenu(mw, variable, *listOfParameters)
    w.pack()
    #T.pack()
    w.place(x=270, y=140, width=120, height=25)

    mw.mainloop()
