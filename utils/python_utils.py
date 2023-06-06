import pyedflib
import numpy as np
from scipy import signal

def readEDF(filepath, filldisrupt = False):
    file = pyedflib.EdfReader(filepath)
    signal_labels = file.getSignalLabels()
    print('signal_labels: ', signal_labels)

    channel1 = file.readSignal(0)
    print('channel1: ', channel1)
    channel2 = file.readSignal(1)

    srate = file.getSampleFrequency(0)
    print('srate ch1: ', srate)
    print('srate ch2: ', file.getSampleFrequency(1))

    total_seconds = file.getFileDuration()
    num_hrs = total_seconds/3600
    num_ten_min_intervals = num_hrs * 6
    samples_per_ten_mins = int(len(channel1) / num_ten_min_intervals)

    ten_min_ratios_ch1 = np.array([])
    ten_min_ratios_ch2 = np.array([])

    # Iterate over EEG data and get the BSEEG score for every 10 minute window
    for i in range(0, int(num_ten_min_intervals)):
        ten_min_signals_ch1 = channel1[i*samples_per_ten_mins:(i*samples_per_ten_mins + samples_per_ten_mins)]
        ten_min_signals_ch2 = channel2[i*samples_per_ten_mins:(i*samples_per_ten_mins + samples_per_ten_mins)]
        # srate*8
        print(f'len of ten_min_signals_ch1: {len(ten_min_signals_ch1)}')
        ten_min_psd_ch1_freqs, ten_min_psd_ch1_power  = signal.welch(ten_min_signals_ch1, srate, nperseg=min(2048, len(ten_min_signals_ch1)))
        print(f'ten_min_psd_ch1_power: {ten_min_psd_ch1_power}')
        ten_min_psd_ch2_freqs, ten_min_psd_ch2_power = signal.welch(ten_min_signals_ch2, srate, nperseg=min(2048, len(ten_min_signals_ch2)))

        print(f'ch1 freqs: {ten_min_psd_ch1_freqs}')
        print(f'ch1 power: {ten_min_psd_ch1_power}')

        sum_ch1_power_3hz = 0
        total_3hz_ch1 = 0
        sum_ch1_power_10hz = 0
        total_10hz_ch1 = 0

        sum_ch2_power_3hz = 0
        total_3hz_ch2 = 0
        sum_ch2_power_10hz = 0
        total_10hz_ch2 = 0

        # Filter for power numbers corresponding to frequencies between (3-3.5 Hz) or (9.5-10 Hz) for channel 1 and 2
        for j in range(len(ten_min_psd_ch1_freqs)):
            if 3 <= ten_min_psd_ch1_freqs[j] <= 3.5:
                sum_ch1_power_3hz += ten_min_psd_ch1_power[j]
                print(f'for {i}, curr 3hz filter: {ten_min_psd_ch1_power[j]}')
                total_3hz_ch1 += 1
            elif 9.5 <= ten_min_psd_ch1_freqs[j] <= 10:
                sum_ch1_power_10hz += ten_min_psd_ch1_power[j]
                total_10hz_ch1 += 1
            if 3 <= ten_min_psd_ch2_freqs[j] <= 3.5:
                sum_ch2_power_3hz += ten_min_psd_ch2_power[j]
                total_3hz_ch2 += 1
            elif 9.5 <= ten_min_psd_ch2_freqs[j] <= 10:
                sum_ch2_power_10hz += ten_min_psd_ch2_power[j]
                total_10hz_ch2 += 1

        avg_ch1_power_3hz = 0 if total_3hz_ch1 == 0 else sum_ch1_power_3hz / total_3hz_ch1
        print(f'avg_ch1_power_3: {avg_ch1_power_3hz}')
        avg_ch1_power_10hz = 0 if total_10hz_ch1 == 0 else sum_ch1_power_10hz / total_10hz_ch1
        print(f'avg_ch1_power_10: {avg_ch1_power_10hz}')
        ch1_power_ratio = 0 if avg_ch1_power_10hz == 0 else avg_ch1_power_3hz / avg_ch1_power_10hz

        avg_ch2_power_3hz = 0 if total_3hz_ch2 == 0 else sum_ch2_power_3hz / total_3hz_ch2
        avg_ch2_power_10hz = 0 if total_10hz_ch2 == 0 else sum_ch2_power_10hz / total_10hz_ch2
        ch2_power_ratio = 0 if avg_ch2_power_10hz == 0 else avg_ch2_power_3hz / avg_ch2_power_10hz

        print('FinalAvg_ch1: ', ch1_power_ratio)
        print('curr i: ', i)
        ten_min_ratios_ch1 = np.append(ten_min_ratios_ch1, ch1_power_ratio)
        ten_min_ratios_ch2 = np.append(ten_min_ratios_ch2, ch2_power_ratio)


    print(f'Ten_min_ratios_ch1: {ten_min_ratios_ch1}')

    final_hour_ratio_avgs_ch1 = np.array([])
    final_hour_ratio_avgs_ch2 = np.array([])    

    # Calculate the average BSEEG Score (power ratio) over every hour
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

    print('\n\n\n\nFinal Values Calculated:\n\n')
    print(f'final hour by hour ratios ch1: \n{final_hour_ratio_avgs_ch1}\n\n')
    print(f'final hour by hour ratios ch2: \n{final_hour_ratio_avgs_ch2}\n\n')

    return final_hour_ratio_avgs_ch1, final_hour_ratio_avgs_ch2