# Get bandwidth data for home LTE connection
# saw the project here https://healeycodes.com/webdev/javascript/python/opensource/2019/08/22/bot-vs-isp.html

import os
import speedtest
import pandas as pd
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.absolute()
DATA_DIR = Path('./data')
DATA_FILE = 'broadband_data.pkl'
FILE_PATH = SCRIPT_PATH / DATA_DIR / DATA_FILE

wanted_keys = ['download', 'upload', 'timestamp', 'lat', 'lon', 'isp']

def speed_test():
    s = speedtest.Speedtest()
    s.download()
    s.upload()
    results_dict = s.results.dict()
    # convert bits to megabits
    results_dict['download'] =  results_dict['download'] / 1048576
    results_dict['upload'] =  results_dict['upload'] / 1048576
    # unpack a few client details
    results_dict['lon'] = results_dict['client']['lon']
    results_dict['lat'] = results_dict['client']['lat']
    results_dict['isp'] = results_dict['client']['isp']

    filtered_results = dict((k, results_dict[k]) for k in wanted_keys)
    return filtered_results

def main():
    # fetch data
    data = speed_test()
    df_result = pd.DataFrame.from_records([data])
    # check the presence of the data file
    if (FILE_PATH).is_file():
        df_history = pd.read_pickle(FILE_PATH)
        df_final = pd.concat([df_history, df_result]).reset_index(drop=True)
        df_final.to_pickle(FILE_PATH)
    else:
        df_result.to_pickle(FILE_PATH)


if __name__ == '__main__':
    main()
