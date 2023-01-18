
import argparse
import functions
import sys


def set_long_lat():
    DF = functions.open_file(functions.FILE)
    # Adding coordinates columns for storing latitude and longitude values
    # -- updating rows with coordinates
    # -- writing result in file
    DF['latitude'] = -1
    DF['longitude'] = -1

    DF = DF.apply(lambda row: functions.add_coordinates(row), axis='columns')

    DF.to_csv(functions.COORDINATES_FILE, sep=';', index=False)

def set_adresses():
    DF = functions.open_file(functions.COORDINATES_FILE)
    # Adding coordinates columns for storing postcodes
    # -- removing duplicates lines (same operator + latitude + longitude)
    # -- updating rows with postcode value
    # -- dropping unused columns
    # -- writing result in file
    DF['postcode'] = -1

    DF.drop_duplicates(['Operateur', 'latitude', 'longitude'], inplace=True)
    DF = DF.apply(lambda row: functions.update_row(row), axis='columns')
    DF.drop(columns=['x', 'y', 'latitude', 'longitude'], inplace=True)

    DF.to_csv(functions.PROCESSED_FILE, sep=';', index=False)


if __name__ == '__main__':
    return_code = 1

    # Setting commands usage for processing main file
    cmd_usage = 'process.py [options]'
    cmd_parser = argparse.ArgumentParser(cmd_usage)
    cmd_parser.add_argument('-f', '--function', action='store', dest='function_name', help='Function to call: coordinates|addresses', default=1)
    cmd_options = cmd_parser.parse_args()
    # Processing according to given command
    match cmd_options.function_name:
        case 'coordinates':
            set_long_lat()
        case 'addresses':
            set_adresses()
        case _:
            print('Usage: process.py [options]\n\nPlease type process.py --help for help.')
            return_code = 0

    sys.exit(return_code)