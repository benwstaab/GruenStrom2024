import datetime
import time


def getTimeFrame(data_list, split, dur, take_off):
    # Calculate epoch time for tomorrow and the takeoff time
    take_off += 2
    epoch_time_tomorrow = int(time.time()) + (24 * 3600)
    epoch_time_takeoff = datetime.datetime.utcfromtimestamp(epoch_time_tomorrow).replace(hour=take_off, minute=0,
                                                                                         second=0)

    # Filter future data_list from data_list
    current_epoch_time = int(time.time())
    data_list = [entry for entry in data_list if entry['epochtime'] > current_epoch_time + 3600]

    if split == 1:
        # Find and mark the highest 'dur' entries regardless of the timeframe
        limited_data = [entry for entry in data_list if entry['epochtime'] < epoch_time_takeoff.timestamp()]
        sorted_data = sorted(limited_data, key=lambda x: x['value'], reverse=True)
        highest_entries = sorted_data[:dur]
        highest_set = set(entry['epochtime'] for entry in highest_entries)

        for entry in data_list:
            entry['highest'] = 1 if entry['epochtime'] in highest_set else 0
    else:
        max_sum = -float('inf')
        start_index = -1

        # Iterate through the array with a window of size n
        for i in range(len(data_list) - dur):
            if data_list[i+dur-1]['epochtime'] >= epoch_time_takeoff.timestamp():
                break

            current_series = data_list[i:i + dur]
            current_sum = sum(entry['value'] for entry in current_series)

            if current_sum > max_sum:
                max_sum = current_sum
                start_index = i

        # Mark the series with the highest sum
        if start_index != -1:
            for i in range(len(data_list)):
                if start_index <= i < start_index + dur:
                    data_list[i]['highest'] = 1
                else:
                    data_list[i]['highest'] = 0

    for entry in data_list:
        entry['time_str'] = time_str(entry['epochtime'])

    # Sort time_frame by 'epochtime' before returning
    return sorted(data_list, key=lambda x: x['epochtime'])


def time_str(epoch):
    '''
    Converts epoch time to formatted string.

    Parameters:
    - epoch (int): Epoch time to convert.

    Returns:
    - str: Formatted datetime string.
    '''
    return datetime.datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
