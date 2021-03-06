import os
import csv
import datetime
from statistics import mean
from collections import deque

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

# Some of the project's constants
AIR_POLLUTANT = 'no2'
STARTING_YEAR = 2013
ENDING_YEAR = 2017
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AIR_QUALITY_DATA_PATH = [BASE_DIR, 'data', 'air_quality', AIR_POLLUTANT]
AIR_QUALITY_PROCESSED_PATH = [BASE_DIR, 'data', 'air_quality', AIR_POLLUTANT, 'processed']
AIR_QUALITY_PROCESSED_FILE = [BASE_DIR, 'data', 'air_quality', AIR_POLLUTANT, 'processed', 'air_processed.csv']


####################################################
##                                                ##
##              AUXILIARY FUNCTIONS               ##
##                                                ##
####################################################

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
'''
def line_is_valid(time_unit, concentration, unit, validity, verification):

    res = False

    if(time_unit == 'hour' and concentration >= 0 and
            unit == 'µg/m3' and validity > 0 and verification < 3):
        res = True

    return res


'''
    Returns a numeric representation of the month using
    two numeric places:
    
                    01, 02, ..., 12
'''
def prettify_month(int_month):

    res = str(int_month)

    if len(res) == 1:
        res = '0' + res

    return res

'''
    Modifies the input date representation so that python
    parses it correctly
'''
def correct_strdate(input_strdate):
    res = input_strdate

    if ":" == input_strdate[-3:-2]:
        res = input_strdate[:-3] + input_strdate[-2:]

    return res

if __name__ == '__main__':

    # Obtain a representation of both the path where
    # the data is stored and the path to the file that
    # will hold the processed result
    air_quality_data_path = get_file_path(AIR_QUALITY_DATA_PATH)
    air_quality_processed_path = get_file_path(AIR_QUALITY_PROCESSED_PATH)
    air_quality_processed = get_file_path(AIR_QUALITY_PROCESSED_FILE)

    # List containing last three months pollution data
    pollution_acc = deque()

    # Dictionary containing the columns of interest the
    # CSV
    data_of_interest = {
        'AveragingTime': 10,
        'Concentration': 11,
        'UnitOfMeasurement': 12,
        'DateTimeBegin': 13,
        'DateTimeEnd': 14,
        'Validity': 15,
        'Verification': 16,
    }

    # Create a directory where to save the processed files
    if not os.path.exists(air_quality_processed_path):
        os.makedirs(air_quality_processed_path)

    # If a previous file existed, delete from disk to
    # create a brand new
    if os.path.exists(air_quality_processed):
        os.remove(air_quality_processed)

    first_year_dump = True
    for year in range(STARTING_YEAR, ENDING_YEAR + 1):

        average_per_month = {k: list() for k in range(1, 13)}

        # We are interested in all of the files containing
        # data from different stations within the same year

        for f in os.listdir(air_quality_data_path):

            # Files containing data will follow the pattern:
            #   ES_YYYY_X_timeseries.csv

            if f.startswith('ES_{}'.format(year)) and f.endswith('_timeseries.csv'):

                air_quality_data_file = get_file_path([air_quality_data_path, f])
                print('Accessing file {} '.format(air_quality_data_file))

                with open(air_quality_data_file, mode='r', encoding='utf-8') as datafile:

                    # Both reader & writer of the input .csv file to the output
                    csv_reader = csv.reader(datafile, delimiter=',')

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
                        line_date_begin = datetime.datetime.strptime(correct_strdate(line[13]), '%Y-%m-%d %H:%M:%S %z')
                        line_date_end = datetime.datetime.strptime(correct_strdate(line[14]), '%Y-%m-%d %H:%M:%S %z')

                        line_validity = int(line[15])
                        line_verification = int(line[16])

                        line_valid = line_is_valid(line_time_unit, line_concentration, line_unit, line_validity,
                                            line_verification)

                        if not line_valid:
                            print('Line {} is invalid... Skipping to next line'.format(line_counter))
                            continue

                        last_date_buffer = line_date_begin

                        line_month = line_date_begin.date().month
                        average_per_month[line_month].append(line_concentration)

        with open(air_quality_processed, mode='a+', encoding='utf-8') as processed:

            csv_writer_users = csv.writer(processed, delimiter=',')

            for k, v in sorted(average_per_month.items()):

                if first_year_dump:
                    first_year_dump = False
                    csv_writer_users.writerow(['Month', 'Year', '{} Concentration'.format(AIR_POLLUTANT), '{} TrimestralConcentration'.format(AIR_POLLUTANT), 'UnitOfMeasurement'])

                if average_per_month[k]:
                    average_per_month[k] = mean(v)
                else:
                    average_per_month[k] = -1

                trimestral_pollution = None

                if len(pollution_acc) == 3:
                    pollution_acc.popleft()

                pollution_acc.append(average_per_month[k])

                if len(pollution_acc) == 3:
                    trimestral_pollution = mean(pollution_acc)

                csv_writer_users.writerow([prettify_month(k), year, average_per_month[k], trimestral_pollution, 'µg/m3'])

                # Write and Persist the line to the file
                processed.flush()
