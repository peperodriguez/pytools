#!/usr/bin/env python3

import requests as rq
import datetime as dt
import pandas   as pd
import io

def get_sek_rate():
    entry    = 'https://sdw-wsrest.ecb.europa.eu/service/'
    resource = 'data'
    flow_ref = 'EXR'
    key      = 'D.SEK.EUR.SP00.A'

    td = dt.datetime.today()
    td = dt.date(td.year,td.month,td.day)
    dp = td + dt.timedelta(days=-5)

    parameters  = {
        'startPeriod':  dp.strftime('%Y-%m-%d'),
        'endPeriod'  :  td.strftime('%Y-%m-%d')
    }

    request_url = entry + resource + '/' + flow_ref + '/' + key
    response    = rq.get(request_url, params=parameters, headers={'Accept': 'text/csv'})
    df          = pd.read_csv(io.StringIO(response.text)).filter(items=['TIME_PERIOD','OBS_VALUE'])

    max_val_idx = df['OBS_VALUE'].idxmax()

    return df.iloc[max_val_idx].tolist()

eur_amount  = 25000
ex_rate     = get_sek_rate()
print('SEK to EUR exchange rate as of '+ex_rate[0]+' is '+str(ex_rate[1])+' SEK/EUR')
print('An invoice of '+str(eur_amount)+' eur is '+str(eur_amount*ex_rate[1])+' SEK')
