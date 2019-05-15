import os
import csv
import datetime
from statistics import mean

'''
    CSV Structure

    Countrycode, Namespace, AirQualityNetwork, AirQualityStation,
    AirQualityStationEoICode, SamplingPoint,SamplingProcess,Sample,
    AirPollutant,AirPollutantCode,AveragingTime,Concentration,
    UnitOfMeasurement,DatetimeBegin,DatetimeEnd,Validity,
    Verification
    
    Each file contains data of an entire year

'''

'''
    Validity Values: http://dd.eionet.europa.eu/vocabulary/aq/observationvalidity/view

    *   -99 --> Not Valid due to station maintenance or...
    *   -1  --> Not Valid
    *   1   --> Valid
    *   2   --> Valid, but below detection limit ...
    *   3   --> Valid, but below detection limit and ...

'''

'''
    Verification Values: http://dd.eionet.europa.eu/vocabulary/aq/observationverification/view

    *   1 --> Verified
    *   2 --> Preliminary Verified
    *   3 --> Not Verified

'''

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AIR_QUALITY_DATA = [BASE_DIR, 'data', 'air_quality', 'ES_{}_timeseries.csv']
AIR_QUALITY_PROCESSED = [BASE_DIR, 'data', 'air_quality', 'processed', 'air_processed.csv']

'''
    Obtains a path using current SO path separator
    using a the specified path represented as a list.
'''
def get_file_path(path_list):
    res = ''

    for p in path_list:
        res = os.path.join(res, p)

    return res


'''
    Whether the provided date is valid or not, bearing in mind the previous
    processed one. A line is valid if and only if:
        
        - Its time unit is 'hour'
        - The registered concentration of the gas is 0 or positive
        - Its concentration unit is 'µg/m3'
        - It is valid, even if it has some defects
        - It is verified or at least, preliminary
        - It was recorded after the last processed line
        
'''
def line_is_valid(time_unit, concentration, unit, date_begin, validity, verification, last_date_in_buffer):

    res = False

    if(time_unit == 'hour' and concentration >= 0 and
            unit == 'µg/m3' and validity > 0 and verification < 3):
        if last_date_in_buffer is None or date_begin > last_date_in_buffer:
            pass
        res = True

    return res


def prettify_month(int_month):

    res = str(int_month)

    if len(res) == 1:
        res = '0' + res

    return res


if __name__ == '__main__':

    air_quality_data_path = get_file_path(AIR_QUALITY_DATA)
    air_quality_processed = get_file_path(AIR_QUALITY_PROCESSED)

    d = {
        'AveragingTime': 10,
        'Concentration': 11,
        'UnitOfMeasurement': 12,
        'DateTimeBegin': 13,
        'DateTimeEnd': 14,
        'Validity': 15,
        'Verification': 16,
    }

    if os.path.exists(air_quality_processed):
        os.remove(air_quality_processed)

    for year in range(2013, 2018):

        air_quality_data_file = air_quality_data_path.format(year)
        average_per_month = {k: list() for k in range(1, 13)}

        with open(air_quality_data_file, mode='r', encoding='utf-8') as datafile, \
                open(air_quality_processed, mode='a+', encoding='utf-8') as processed:

            # Both reader & writer
            csv_reader = csv.reader(datafile, delimiter=',')
            csv_writer_users = csv.writer(processed, delimiter=',')

            # DELETE
            csv_writer_users.writerow(d.keys())

            line_counter = 0
            last_date_buffer = None
            for line in csv_reader:

                line_counter += 1

                # First line only contains header descriptor
                if line_counter == 1:
                    continue

                # Extract fields' values
                line_time_unit = line[10]
                line_concentration = float(line[11])
                line_unit = line[12]
                line_date_begin = datetime.datetime.strptime(line[13], '%Y-%m-%d %H:%M:%S %z')
                line_date_end = datetime.datetime.strptime(line[14], '%Y-%m-%d %H:%M:%S %z')
                line_validity = int(line[15])
                line_verification = int(line[16])

                line_valid = line_is_valid(line_time_unit, line_concentration, line_unit, line_date_begin, line_validity,
                                    line_verification, last_date_buffer)

                if not line_valid:
                    print('Line {} is invalid... Skipping to next line'.format(line_counter))
                    continue

                last_date_buffer = line_date_begin

                line_month = line_date_begin.date().month
                average_per_month[line_month].append(line_concentration)

            for k, v in average_per_month.items():

                if average_per_month[k]:
                    average_per_month[k] = mean(v)
                else:
                    average_per_month[k] = -1

                csv_writer_users.writerow(['{}/{}'.format(k, year), average_per_month[k], 'µg/m3'])

            print(average_per_month)
            # Write and Persist the line to the file
            processed.flush()
