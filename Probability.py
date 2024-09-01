# -*- coding: utf-8 -*-

"""
Created on Tue Oct 31 08:39:15 2023

@author: Fang Xu
"""

import pandas as pd
import seaborn as sns

# The name of trip hourly file can be change to Friday or Saturday 
# and create relatively trips hours file

country_trips_df = pd.read_csv('Data/AvgDayHourlyTrips201819_1270_weekday_v1.csv')

study_area = pd.read_csv('Data/Jerusalem_Fixed_Weight.csv')
zone_code_list = study_area['Zone_Code']

Jerusalem_trips_df = country_trips_df[country_trips_df['fromZone'].isin(zone_code_list)]
Jerusalem_trips_df = Jerusalem_trips_df[Jerusalem_trips_df['ToZone'].isin(zone_code_list)]
Jerusalem_trips_df.to_csv('Data/Jerusalem_Trips_Weekday.csv', index=False)

# create distribution of trips of 90 zones per hour 
del Jerusalem_trips_df['fromZone']
Jerusalem_trips_time = Jerusalem_trips_df.groupby('ToZone',as_index=False).sum()
Jerusalem_trips_hours_df = pd.read_csv('Data/Jerusalem_Trips_Hours_Weekday.csv')

sns.set(rc={'figure.figsize':(8, 6)})
Jerusalem_trips_hours_graph = sns.violinplot(x="Trips",y="Hour",data=Jerusalem_trips_hours_df,linecolor=True)
Jerusalem_trips_hours_graph.set(xlabel="Trips of each zone per hour", ylabel="0-23 Hour")
Jerusalem_trips_hours_graph.set_title('Trips per hour for 90 zones of Jerusalem',fontweight='bold')

#test query: get trips between zones
zone_trips = Jerusalem_trips_df.query('fromZone == 100439 & ToZone == 100514')
zone_trips['h7']











