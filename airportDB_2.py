from pymongo import MongoClient
from time import time
import time
import datetime
import requests
import schedule
import csv

APIKEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3Jl'\
         'ZGVudGlhbHxOMHFkRzVTd1hxM2VrYzJrblFFN0g1UEdZa0ciLCJhcHBsaWNhdGlvb' \
         'l9pZCI6ImFwcGxpY2F0aW9ufE5sbDY3RE1GdkJYcHk3aUtMOVgwWVR4RUI0NEsiLC' \
         'Jvcmdhbml6YXRpb25faWQiOiJkZXZlbG9wZXJ8NzNrUFgzZXUweXdxWUxGOUxET1hw' \
         'aWtnbm5iWiIsImlhdCI6MTUyOTgzODE1NH0.f43-dAkFA6VXdqoueqTUe6n9w1-TWD' \
         'w3zyVJEZ86GxM'


timingData = [["Time Stamp", "Location", "Radius", "Time Elapsed", "# of Outputs", "Exception Thrown"]]
schedule.clear()


def fileParser(fileName):
    doc = open(fileName)
    locations = []
    for line in doc:
        line = line.split(';')
        line[2] = line[2][0:-1]
        line = [float(number) for number in line]
        locations.append(line)
    return locations


def queryCreation(coordinateArray, radius):
    query = {
        'latitude': coordinateArray[1],
        'longitude': coordinateArray[0],
        'types': 'airport',
        # 'buffer': coordinates[2] // this is for when using just the location document
        'buffer': radius
    }
    return query


def apiResponseParse(apiResponse):
    airportDataDictionary = {}
    for info in apiResponse['data']['advisories']:
        if 'airport_name' in info['properties']:
            airport = info['properties']['airport_name']
            city = info['city']
            state = info['state']
            country = info['country']
            location = "{}, {}, {}".format(city, state, country)
            phone = info['properties']['phone']
            airportDataDictionary[airport] = [location, phone]
    return airportDataDictionary


def csvTimeDataInsertion(data):
    myFile = open('timeData3.csv', 'a')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(data)


def dataBaseCreation():
    global posts
    client = MongoClient()
    db = client['Airports']
    posts = db.posts
    db.posts.delete_many({})


def dataBaseInsertion(airportData):
    for airport in airportData:
        post_data = {
            'name': airport,
            'location': airportData[airport][0],
            'phone': airportData[airport][1]
        }
        posts.insert_one(post_data)


def dataBasePrint():
    for post in posts.find():
        print(post)


def apiRequest(query, headers):
    exceptionThrownBoolean = False
    while True:
        try:
            startTime = time.time()
            response = requests.get('https://api.airmap.com/status/v2/point', params=query, headers=headers)
            endTime = time.time()
        except:
            exceptionThrownBoolean = True
            time.sleep(1)
            continue
        else:
            break
    return exceptionThrownBoolean, response, endTime-startTime


def dataRequest(locations):

    headers = {
        'X-API-Key': APIKEY
    }

    for radius in range(250, 501, 250):
        locationCounter = 0
        for locationCoordinates in locations:
            locationCounter += 1

            timingDataSingleLocation = [datetime.datetime.now(), "Location {}".format(locationCounter), radius]

            query = queryCreation(locationCoordinates, radius)
            (exceptionThrownBoolean, response, timeElapsed) = apiRequest(query, headers)
            apiResponse = response.json()
            print(apiResponse)
            timingDataSingleLocation.extend((timeElapsed, len(apiResponse['data']['advisories']), exceptionThrownBoolean))

            airportData = apiResponseParse(apiResponse)
            dataBaseInsertion(airportData)

            timingData.append(timingDataSingleLocation)

        csvTimeDataInsertion(timingData)
        timingData.clear()

    dataBasePrint()
    return posts


def scheduler():
    # schedule.every(10).seconds.do(job)
    schedule.every(10).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(5)


def main():
    locationList = fileParser("locations.txt")
    dataBaseCreation()
    dataRequest(locationList)
    timingData.clear()


if __name__ == '__main__':
    main()
    scheduler()


