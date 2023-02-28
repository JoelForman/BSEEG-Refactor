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


def readEDF(filepath, filldisrupt = False):
    #open the file using pyedflib
    file = pyedflib.EdfReader(filepath)
    signal_labels = file.getSignalLabels()
    print('signal_labels: ', signal_labels)

    channel1 = file.readSignal(0)
    channel2 = file.readSignal(1)

    #get the number of hours
    srate = file.getSampleFrequency(0)
    total_seconds = file.getFileDuration()
    # print('total_seconds: ', total_seconds)
    # print('length of first signal: ', len(channel1))
    # print('length of second signal: ', len(channel2))
    # print('srate: ', srate)
    # print('srate * total seconds: ', srate * total_seconds)
    num_hrs = total_seconds/3600
    num_ten_min_intervals = num_hrs * 6
    samples_per_ten_mins = int(len(channel1) / num_ten_min_intervals)
    print('length of samples_per_ten_mins: ', samples_per_ten_mins)

    ten_min_ratios_ch1 = np.array([])
    ten_min_ratios_ch2 = np.array([])

    for i in range(0, int(num_ten_min_intervals)):
        ten_min_signals_ch1 = channel1[i*samples_per_ten_mins:(i*samples_per_ten_mins + samples_per_ten_mins)]
        ten_min_signals_ch2 = channel2[i*samples_per_ten_mins:(i*samples_per_ten_mins + samples_per_ten_mins)]
        # print(f'channel 1 interval {i} length: {len(ten_min_signals_ch1)}')
        # print(f'channel 2 interval {i} length: {len(ten_min_signals_ch2)}')

        ten_min_psd_ch1 = signal.welch(ten_min_signals_ch1, len(ten_min_signals_ch1) / 600)[1]
        ten_min_psd_ch2 = signal.welch(ten_min_signals_ch2, len(ten_min_signals_ch2) / 600)[1]

        # print(f'len of psd of 10 min interval of channel 1: {len(ten_min_psd_ch1)}')
        # print(f'len of psd of 10 min interval of channel 2: {len(ten_min_psd_ch2)}')


        # filter by frequencies

        filtered_psd_3hz_ch1 = np.array([x for x in ten_min_psd_ch1 if 3 <= x <= 3.5])
        filtered_psd_3hz_ch2 = np.array([x for x in ten_min_psd_ch2 if 3 <= x <= 3.5])
        # print(f'filtered_psd_3hz_ch1: {filtered_psd_3hz_ch1}')
        # print(f'filtered_psd_3hz_ch2: {filtered_psd_3hz_ch2}')

        filtered_psd_10hz_ch1 = np.array([x for x in ten_min_psd_ch1 if 9.5 <= x <= 10])
        filtered_psd_10hz_ch2 = np.array([x for x in ten_min_psd_ch2 if 9.5 <= x <= 10])
        # print(f'filtered_psd_10hz_ch1: {filtered_psd_10hz_ch1}')
        # print(f'filtered_psd_10hz_ch2: {filtered_psd_10hz_ch2}')

        # take averages

        avg_3hz_psd_ch1 = np.mean(filtered_psd_3hz_ch1)
        avg_3hz_psd_ch2 = np.mean(filtered_psd_3hz_ch2)
        # print(f'mean 3hz psd ch1: {avg_3hz_psd_ch1}')
        # print(f'mean 3hz psd ch2: {avg_3hz_psd_ch2}')

        avg_10hz_psd_ch1 = np.mean(filtered_psd_10hz_ch1)
        avg_10hz_psd_ch2 = np.mean(filtered_psd_10hz_ch2)
        # print(f'mean 10hz psd ch1: {avg_10hz_psd_ch1}')
        # print(f'mean 10hz psd ch2: {avg_10hz_psd_ch2}')

        ten_min_ratios_ch1 = np.append(ten_min_ratios_ch1, avg_3hz_psd_ch1/avg_10hz_psd_ch1)
        ten_min_ratios_ch2 = np.append(ten_min_ratios_ch2, avg_3hz_psd_ch2/avg_10hz_psd_ch2)

    print(f'all ten min rations channel1: {ten_min_ratios_ch1}')
    print(f'all ten min rations channel2: {ten_min_ratios_ch2}')

    final_hour_ratio_avgs_ch1 = np.array([])
    final_hour_ratio_avgs_ch2 = np.array([])    

    for i in range(len(ten_min_ratios_ch1) // 6):
        sum = 0
        num_total = 0
        for j in range(i*6, (i*6 + 6)):
            if not np.isnan(ten_min_ratios_ch1[j]):
                sum += ten_min_ratios_ch1[j]
                num_total += 1
        if num_total == 0:
            avg = 0
        else:
            avg = sum / num_total
        final_hour_ratio_avgs_ch1 = np.append(final_hour_ratio_avgs_ch1, avg)

    for i in range(len(ten_min_ratios_ch2) // 6):
        sum = 0
        num_total = 0
        for j in range(i*6, (i*6 + 6)):
            if not np.isnan(ten_min_ratios_ch2[j]):
                sum += ten_min_ratios_ch2[j]
                num_total += 1
        if num_total == 0:
            avg = 0
        else:
            avg = sum / num_total
        final_hour_ratio_avgs_ch2 = np.append(final_hour_ratio_avgs_ch2, avg)

    print(f'final hour by hour ratios ch1: {final_hour_ratio_avgs_ch1}')
    print(f'final hour by hour ratios ch2: {final_hour_ratio_avgs_ch2}')

    # standardize
    final_hour_ratio_avgs_ch1[final_hour_ratio_avgs_ch1 == 0] = np.nan
    final_hour_ratio_avgs_ch2[final_hour_ratio_avgs_ch2 == 0] = np.nan

    standardized_ratio_avgs_ch1 = (final_hour_ratio_avgs_ch1 - np.nanmean(final_hour_ratio_avgs_ch1)) / np.nanstd(final_hour_ratio_avgs_ch1)
    standardized_ratio_avgs_ch2 = (final_hour_ratio_avgs_ch2 - np.nanmean(final_hour_ratio_avgs_ch2)) / np.nanstd(final_hour_ratio_avgs_ch2)

    print(f'standardized final hour by hour ratios ch1: {standardized_ratio_avgs_ch1}')
    print(f'standardized final hour by hour ratios ch2: {standardized_ratio_avgs_ch2}')

    #return (final_hour_ratio_avgs_ch1 - np.mean(final_hour_ratio_avgs_ch1)) / np.std(final_hour_ratio_avgs_ch1), (final_hour_ratio_avgs_ch2 - np.mean(final_hour_ratio_avgs_ch2)) / np.std(final_hour_ratio_avgs_ch2)
    return standardized_ratio_avgs_ch1, standardized_ratio_avgs_ch2

@app.route('/analysis.html', methods=['GET', 'POST'])
def analysis():
    final_avg1 = final_avg2 = []
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
            # print('final_avg1: ', final_avg1)
            # print('final_avg2: ', final_avg2)
            #coolEDFTableF, coolEDFTableS = post_process_data(final_avg1, final_avg2)
            #print("First table: ", coolEDFTableF)
            #print("Second table: ", coolEDFTableS)
        else:
            # Return an error message
            return 'Invalid file format. Only .edf files are allowed.'
    return render_template('analysis.html', final_avg1=final_avg1.tolist(), final_avg2=final_avg2.tolist())

if __name__ == '__main__':
    app.run(debug=True)