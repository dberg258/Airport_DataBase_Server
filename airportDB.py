from pymongo import MongoClient
from time import time
import requests
import schedule

file = open('timeData.txt', 'a')
timingData = []

schedule.clear()


def fileParser(fileName):
    file = open(fileName)
    locations = []
    for line in file:
        line = line.split(';')
        line[2] = line[2][0:-1]
        line = [float(number) for number in line]
        locations.append(line)
    #print(locations)
    return locations


def dataRequest(locations):
    headers = {
        'X-API-Key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlh'
                     'bHxOMHFkRzVTd1hxM2VrYzJrblFFN0g1UEdZa0ciLCJhcHBsaWNhdGlvbl9pZCI6ImFwcGxpY'
                     '2F0aW9ufE5sbDY3RE1GdkJYcHk3aUtMOVgwWVR4RUI0NEsiLCJvcmdhbml6YXRpb25faWQiOi'
                     'JkZXZlbG9wZXJ8NzNrUFgzZXUweXdxWUxGOUxET1hwaWtnbm5iWiIsImlhdCI6MTUyOTgzODE'
                     '1NH0.f43-dAkFA6VXdqoueqTUe6n9w1-TWDw3zyVJEZ86GxM'
    }

    for coordinates in locations:
        query = {
            'latitude': coordinates[1],
            'longitude': coordinates[0],
            'types': 'airport',
            'buffer': coordinates[2]
        }

        startTime = time()
        r = requests.get('https://api.airmap.com/status/v2/point', params=query, headers=headers)
        endTime = time()
        timingData.append((coordinates[2], endTime - startTime))
        request = r.json()

        data = {}

        for info in request['data']['advisories']:
            if 'airport_name' in info['properties']:
                airport = info['properties']['airport_name']
                city = info['city']
                state = info['state']
                country = info['country']
                location = "{}, {}, {}".format(city, state, country)
                phone = info['properties']['phone']
                data[airport] = [location, phone]

        for airport in data:
            post_data = {
                'name': airport,
                'location': data[airport][0],
                'phone': data[airport][1]
            }
            posts.insert_one(post_data)

    for post in posts.find():
        print(post)

    return posts


def analyzeTime(data):
    for radius, timeTaken in data:
        file.write("Radius: " + str(radius)[0:4] + "  Time: " + str(timeTaken)[0:10] + "  ")
    file.write("\n")


def job():
    if __name__ == "__main__":
        locationList = fileParser("locations.txt")

        # Mongo DB initialization
        client = MongoClient()
        db = client['Airports']
        global posts
        posts = db.posts
        db.posts.delete_many({})

        dataRequest(locationList)
        analyzeTime(timingData)
        timingData.clear()
        print(timingData)

job()
job()
job()
job()
#schedule.every(10).seconds.do(job)
#schedule.every(30).minutes.do(job)

#while True:
 #   schedule.run_pending()


