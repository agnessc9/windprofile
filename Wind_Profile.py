import requests, pandas as pd
import numpy as np
import math
import pprint
import matplotlib.pyplot as plt
import datetime

#Variable section for start_time and end_time:
year = 2022
month = "10"    #IMPORTANT - JAN, FEB, MARCH ...... SEP must be set to 01, 02, 03 ... 09 as a STRING
start_date = "27"  #IMPORTANT, all single digit dates must have 0 at front as STRING, Ex: 01, 02, 03
end_date = "28"    #IMPORTANT, all single digit dates must have 0 at front as STRING, Ex: 01, 02, 03
start_time = "01"  #IMPORTANT, all hours must have two digits, single digit hours must have 0 at front as a STRING
end_time = 23      #IMPORTANT, all hours must have two digits, single digit hours must have 0 at front as a STRING




data = pd.read_csv (r'C:\Users\yiyan\Downloads\ASC2022 (1).csv')
df = pd.DataFrame(data, columns= ["latitude", "longitude"])
#Read the csv file and only read the columns Latitude and Longitude
#print(df)



Lat_long_pairs = []
Lat = []
Long = []

for ind in df.index:
    Lat_long_pairs.append([df["latitude"][ind], df["longitude"][ind]])


#Create a loop to in take all the latitude and longitude pairs that we are looking to calculate the wind velocity and
#direction for and store them in a list




def get_API(lat, long): #Calls the API on the specific latitude and longitude and returns the output of the json file
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=windspeed_10m,winddirection_10m")
    #print(response.status_code)
    output = response.json()
    return(output)


def get_time(year, month, start_date, start_hour, end_date, end_hour): #Creates the time string that matches the format
    #of the json file
    #May switch to datetime later, currently datetime does not match up with the time strings in the dictionary

    #start_time = datetime.datetime(year,month, start_date, start_hour)
    #end_time = datetime.datetime(year, month, end_date, end_hour)


    start_time_ = str(year) + "-" + str(month) + "-" + str(start_date) + "T" + str(start_hour) + ":00"
    end_time_ = str(year) + "-" + str(month) + "-" + str(end_date) + "T" + str(end_hour) + ":00"
    return([start_time_, end_time_])


def get_average(lat, long, year, month, start_date, start_hour, end_date, end_hour): #Main function
    start_index = 0
    end_index = 0
    #Two variables above are meant to track which wind velocity and wind direction we want given a 7 day API wind forecast


    data_set = get_API(lat,long)
    #pprint.pprint(data_set)
    #Call the API, print function can be deleted

    time_set = get_time(year,month,start_date,start_hour,end_date,end_hour)
    for i in range(len(data_set['hourly']['time'])):
        if data_set['hourly']['time'][i] == time_set[0]:
            start_index += i
            pass
        elif data_set['hourly']['time'][i] == time_set[1]:
            end_index += i
            break

    #Find the starting wind_direction and wind_speed indeces and ending wind_direction and wind_speed indeces

    wind_speed_10m_list = (data_set['hourly']['windspeed_10m'][start_index:end_index])
    wind_direct_10m_list = (data_set['hourly']['winddirection_10m'][start_index:end_index])

    #Create two new lists consist of only the wind direction and wind speed during a specific time frame

    #print(wind_speed_10m_list)
    #print(wind_speed_10m_list)
    #print function can be deleted

    counter = 0
    speed_sum = 0
    direct_sum = 0
    for i in wind_speed_10m_list:
        counter += 1
        speed_sum += i

    for j in wind_direct_10m_list:
        try:
            direct_sum += j
        except:
            print("error occured at" + str(j))
            pass



    #Take the average of the two lists, since they have the same number of items use the same counter for both lists


    return(speed_sum/counter, direct_sum/counter)






#--------------------------------------------------

#Below is the calling of the function
average_velocity = []
average_angle = []


for i in range(len(Lat_long_pairs)):
    print(i)
    if i % 1000 == 0:
        average_velocity.append(get_average(Lat_long_pairs[i][0],Lat_long_pairs[i][1],year,month, start_date, start_time, end_date, end_time)[0])
        average_angle.append(get_average(Lat_long_pairs[i][0],Lat_long_pairs[i][1],year,month, start_date, start_time, end_date, end_time)[1])
        Lat.append(Lat_long_pairs[i][0])
        Long.append(Lat_long_pairs[i][1])
        print(average_velocity)
        print(average_angle)


print(average_angle)

u = []
for i in average_angle:
    u.append(math.cos(i))
v = []
for i in average_angle:
    v.append(math.sin(i))
North_Lat = []
North_Long = []
East_Lat = []
East_Long = []
South_Lat = []
South_Long = []
West_Lat = []
West_Long = []
for i in range(len(average_angle)):
    if (average_angle[i] >= 0 and average_angle[i] <= 45) or (average_angle[i] >= 315 and average_angle[i] <= 0):
        North_Lat.append(Lat[i])
        North_Long.append(Long[i])
    elif (average_angle[i] >= 45 and average_angle[i] <= 135):
        East_Lat.append(Lat[i])
        East_Long.append(Long[i])
    elif (average_angle[i] >= 135 and average_angle[i] <= 225):
        South_Lat.append(Lat[i])
        South_Long.append(Long[i])
    else:
        West_Lat.append(Lat[i])
        West_Long.append(Long[i])

min = min(average_velocity)
max = max(average_velocity)

plt.subplot(1,2,1)
plt.title("Average Wind Velocity")
plt.scatter(Lat, Long, s=100, c=average_velocity, cmap = "Greens", marker='o')
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.colorbar()

plt.subplot(1,2,2)
plt.title("Average Wind Direction")



plt.scatter(North_Lat,North_Long, s=100, marker ='^')
plt.scatter(East_Lat, East_Long, s=100, marker ='>')
plt.scatter(South_Lat, South_Long, s=100, marker ='v')
plt.scatter(West_Lat, West_Long, s=100, marker ='<')

plt.show()








