import csv
#basically used to compute time in seconds
def computeSeconds(data):
    data = data.split(":")
    seconds = int(data[0])*3600+int(data[1])*60+int(data[2]) 
    return int(seconds)


def dateSplit(data):
    data = data.split()
    return data

def creatingDates():
    # pass
    with open('dataset.csv','r') as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
            Date = row['timestamp'].split()
            # print(f"\t{date}")
            # print(Date[0])
            # if(date != Date[0]):
            if Date[0] not in markedDates:
                markedDates.append(Date[0])


def generateHeader():
    with open('dataset1.csv','w') as file:
        writer=csv.DictWriter(file,fieldnames=['UserId','Date','Active_Duration_(in Minutes)'])
        writer.writeheader()


def generatingReport(data,userDetails,time):
    user=[]
    with open('dataset.csv','r') as file:
        csvFile = csv.DictReader(file)
        with open('dataset1.csv','a') as appendFile:
            writer=csv.DictWriter(appendFile,fieldnames=['UserId','Date','Active_Duration_(in Minutes)'])
            # writer.writeheader()    
            i=0
            for row in csvFile:
                dictionary1={}
                Date = row['timestamp'].split()
                if data == Date[0] and userDetails == row['userId']:
                    if i==0:
                        dictionary1 = {'UserId':f"{row['userId']}",'Date':f"{Date[0]}",'Active_Duration_(in Minutes)':f"{time}"}
                    # user.append(dictionary)
                        writer.writerow(dictionary1)
                        i+=1          

#declaring empty dictionaries
markedDates=[]
sessionStartDictionary={}
sessionEndDictionary={}
dictionary={}
actionDictionary={}
def main():
    with open("dataset.csv","r") as file:
        csvFile = csv.DictReader(file)

        for rows in csvFile:
            if rows['userId'] not in dictionary:
                dictionary[rows['userId']]=1
            else:
                dictionary[rows['userId']]+=1

            if rows['action']=='Login':
                dateTime = rows['timestamp'].split()
                # print(dateSplit(dateTime[0]))
                if rows['userId'] not in sessionStartDictionary:
                    sessionStartDictionary[rows['userId']]=computeSeconds(dateTime[1])
                else:
                    sessionStartDictionary[rows['userId']]+=computeSeconds(dateTime[1])

            if rows['action']=='LogOut':
                dateTime = rows['timestamp'].split()
                if rows['userId'] not in sessionEndDictionary:
                    sessionEndDictionary[rows['userId']]=computeSeconds(dateTime[1])
                else:
                    sessionEndDictionary[rows['userId']]+=computeSeconds(dateTime[1])
            

            #procedure for determining most common action
            # getCount = len(dictionary)
            if rows['action'] not in actionDictionary:
                actionDictionary[rows['action']] = 1
            else:
                actionDictionary[rows['action']] +=1

            time = rows['timestamp'].split()
    creatingDates()
    # print(markedDates)

    #Displaying the total number of actions performed by each user
    print("\n\n\033[1mFollowing Number of actions performed by each user : \n")
    for i in dictionary:
        print(f"{i} \t\t\t{dictionary[i]} actions") 
        print("--------------------------------------------")    



    # #Displaying max number of actions performed by a single user
    print("\n\nFollowing User has the highest number of engagements: \n")

    highAct=max(zip(dictionary.values(),dictionary.keys()))
    print(f"{highAct[1]} \t\t\t {highAct[0]}")
    print("--------------------------------------------")
    


    #Displaying statistics of User in minutes
    print("\n\nFollowing is the statistics of daily usage: \n")
    print("\033[1mUser \t\t\t Time Spend(in mins)")
    print("--------------------------------------------")
    # print(len(markedDates))
    generateHeader()
    for i in dictionary:
        time = int((sessionEndDictionary[i]-sessionStartDictionary[i])/60)
        for j in range(len(markedDates)):
            # print(markedDates[j])
            generatingReport(markedDates[j],i,time)
        print(f"{i} \t\t\t {time}")
        print("--------------------------------------------")



    #Displaying common actions performed by user
    print("\n\nFollowing are the common actions performed by all user \n")
    print("Action \t\t\t No. of times")
    print("--------------------------------------------")
    for i in actionDictionary:
        print(f"{i}\t\t\t\t {actionDictionary[i]}")
        print("--------------------------------------------")

    
main()