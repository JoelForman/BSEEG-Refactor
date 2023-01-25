from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pyedflib
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)
Bootstrap(app)

@app.route('/index.html', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

def power_spectral_density(data, srate):
    data = np.array(data)
    f, Pxx_den = signal.welch(data, srate, nperseg=1024)
    return f, Pxx_den


def readEDF(filepath, filldisrupt = False):
    #open the file using pyedflib
    file = pyedflib.EdfReader(filepath)
    signal_labels = file.getSignalLabels()
    print('signal_labels: ', signal_labels)
    #get the number of hours
    srate = file.getSampleFrequency(0)
    total_seconds = file.getNSamples()[0]
    num_hrs = total_seconds/(srate*3600)
    #parse the data into 24 hours and 10 minutes intervals
    num_hrs = int(num_hrs)
    thresh = int(total_seconds/(num_hrs*6))
    #initialize columns to hold the average for the first EEG electrode
    my_avg_3_eeg1 = np.empty(thresh)
    my_avg_10_eeg1 = np.empty(thresh)
    #initialize columns to hold the average for the second EEG electrode
    my_avg_3_eeg2 = np.empty(thresh)
    my_avg_10_eeg2 = np.empty(thresh)
    #initialize two variables for holding mean values
    final_avg_1 = np.empty(1)
    final_avg_2 = np.empty(1)
    #go through all the data for every 10 minute window
    for i in range(0, num_hrs*6):
        #read data from the file
        data = file.readSignal(i)
        if filldisrupt:
            idx = np.where(data[0] == 0.00045)[0]
            data = np.delete(data, idx, axis=1)
        if len(data) != 0:
            #compute power spectral density
            psd = power_spectral_density(data, srate)
            #find range
            hold_3_hz = [x for x in psd if 3 <= x[0] <= 3.5]
            hold_10_hz = [x for x in psd if 9.5 <= x[0] <= 10]
            #find the mean of hold3Hz and hold10Hz for the first electrode
            my_avg_3_eeg1[i] = np.mean([x[1] for x in hold_3_hz])
            my_avg_10_eeg1[i] = np.mean([x[1] for x in hold_10_hz])
            #find the mean of hold3Hz and hold10Hz for the second electrode
            my_avg_3_eeg2[i] = np.mean([x[1] for x in hold_3_hz])
            my_avg_10_eeg2[i] = np.mean([x[1] for x in hold_10_hz])
    #compute final averages
    final_avg_1 = np.mean(np.concatenate((my_avg_3_eeg1, my_avg_10_eeg1)))
    final_avg_2 = np.mean(np.concatenate((my_avg_3_eeg2, my_avg_10_eeg2)))
    file._close()
    return final_avg_1, final_avg_2

def post_process_data(final_avg_1, final_avg_2, filldis=False):
    #Initialize variables for holding results of computation
    avgavg1 = []
    avgavg2 = []
    normavg1 = []
    normavg2 = []
    #find the average of ratios for every hour
    numhm = len(final_avg_1)//6 - 1
    for k in range(0, numhm+1):
        #find the average for every hour
        valVal1 = final_avg_1[(6*(k)):(6*(k+1))]
        valVal2 = final_avg_2[(6*(k)):(6*(k+1))]
        avgavg1.append(sum(valVal1)/len(valVal1))
        avgavg2.append(sum(valVal2)/len(valVal2))
    #create a dataframe with time and EEG1 and EEG2 columns
    coolEDFTable = pd.DataFrame(columns=["time", "EEG1", "EEG2"])
    coolEDFTable["time"] = range(1, 25)
    coolEDFTable["EEG1"] = avgavg1 + [float('nan')]*(24-len(avgavg1))
    coolEDFTable["EEG2"] = avgavg2 + [float('nan')]*(24-len(avgavg2))
    coolEDFTable = coolEDFTable.dropna()
    coolEDFTableF = coolEDFTable.iloc[:12]
    coolEDFTableS = coolEDFTable.iloc[12:]
    if filldis:
        if len(coolEDFTableF.dropna()) >= 3:
            coolEDFTableF = coolEDFTableF.interpolate()
        if len(coolEDFTableS.dropna()) >= 3:
            coolEDFTableS = coolEDFTableS.interpolate()
    return coolEDFTableF, coolEDFTableS

@app.route('/analysis.html', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']
        # Get the file name and extension
        filename = file.filename

        # Check if the file is an EDF file
        if file and filename.rsplit('.', 1)[1].lower() == 'edf':
            # Save the file to the server
            file.save('uploaded_file.edf')
            print(file)

            final_avg1, final_avg2 = readEDF('uploaded_file.edf')
            print('final_avg1: ', final_avg1)
            print('final_avg2: ', final_avg2)
            #coolEDFTableF, coolEDFTableS = post_process_data(final_avg1, final_avg2)
            #print("First table: ", coolEDFTableF)
            #print("Second table: ", coolEDFTableS)
        else:
            # Return an error message
            return 'Invalid file format. Only .edf files are allowed.'
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)