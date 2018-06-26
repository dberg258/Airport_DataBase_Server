def fileParser(fileName):
    file = open(fileName)
    locations = []
    for line in file:
        line = line.split(';')
        line[2] = line[2][0:-1]
        line = [float(number) for number in line]
        locations.append(line)
    # print(locations)
    return locations
