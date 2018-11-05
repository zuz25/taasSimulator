from numpy import random
import numpy as np
import queue
from time import sleep

class vehicle:
 
    def __init__(self, id, simTime):
        self.id = id
        self.Location = Locations[random.randint(2)]
        self.numCompletedTrips = 0
        self.status = "Waiting for Request"
        self.timeLeftOnTrip = 99
        
    def incrementCompleteTrips(self):
        self.numCompletedTrips += 1
    
    def setStatus(self,status):
        self.status=status

    def assignRider(self,rider):
        self.assignedRider=rider

class rider:
 
    def __init__(self, id, simTime):
        self.id = id
        self.dropoff="None"
        self.requestTimes = []
        self.enRouteToPickupTimes =[]
        self.pickupTimes=[]
        self.dropoffTimes=[]
        self.queueWaitTimes = []
        self.waitTimes=[]
        self.totalWaitTimes =[]
        self.rideTimes=[]
        self.Location = Locations[random.randint(2)]
        self.numCompletedTrips = 0
        self.status = "Request Ride"
        self.timeLeftOnTrip = 99
        self.chooseDropoff()
        self.generateRequestTime(simTime, waveSpacing, mean, stdev)

    
    def __lt__(self, other):
        return self.numCompletedTrips < other    
    
    def chooseDropoff(self):
        if self.numCompletedTrips==0:
            if self.Location=="M":
                self.dropoff="W"
            else:
                self.dropoff="M"
        elif self.numCompletedTrips==1:
            self.dropoff="F"
        
    def time(self):
        return self.time
 
    def generateRequestTime(self, waveSpacing, simTime, mean, stdev):
        if self.id <= 6:
            self.nextRequestTime = simTime + random.normal(mean,stdev)
        if self.id > 6:
            self.nextRequestTime = waveSpacing + simTime + random.normal(mean,stdev)

    def saveRequestTime(self,simTime):
        self.requestTimes.append(simTime)
    
    def savePickupTime(self,simTime):
        self.pickupTimes.append(simTime)
    
    def saveDropoffTime(self,simTime):
        self.dropoffTimes.append(simTime)

    def assignVehicle(self,vehicle):
        self.assignedVehicle=vehicle
    
    def setStatus(self,status):
        self.status=status

def calcTravelTime(pickup,dropoff):
    if dropoff == "F":
        return 12 + random.normal(5,2)
    else:
        return 7 + random.normal(4,1)

def generateRiders(numRiders,simTime):
    i=0
    riders=[]
    while i < numRiders:
        i += 1
        riders.append(rider(i,simTime))
    return riders

def generateVehicles(numVehicles,simTime):
    i=0
    vehicles=[]
    while i < numVehicles:
        i += 1
        vehicles.append(vehicle(i,simTime))
    return vehicles

def chooseCancellers(riders):
    

## Setup

numVehicles = 6
numRiders = 12
rideRequestQueue= queue.Queue()
mean = 40
stdev = 10
waveSpacing = 15
Locations =["M", "W"]
finalLocation = ["F"]
simTime = 0
allQueueWaitTimes =[]
allWaitTimes =[]
allTotalWaitTimes =[]
allRideTimes =[]
per = 10%

riders = generateRiders(numRiders,simTime)
vehicles = generateVehicles(numVehicles,simTime)



#for elem in list(rideRequestQueue.queue):
    #print(elem.id,elem.dropoff)

for elem in riders:
    print(elem.id,elem.numCompletedTrips)    

for rider in riders:
    print("riderId: ",rider.id,"Ride Request Time: ",int(rider.nextRequestTime))

while min(riders,key=lambda rider:rider.numCompletedTrips) < 2:
#while simTime <500:
#Determine what riders are requesting Trips
    for rider in riders:
        #print(rider.id,int(rider.nextRequestTime))
        print("Rider Id: ",rider.id, "Sim Time: ", simTime, "Request Time: ",int(rider.nextRequestTime))
        if int(rider.nextRequestTime) == simTime and rider.id <=6:
            print("ride added to queue")
            rideRequestQueue.put(rider)
            rider.setStatus("Request Ride")
            rider.saveRequestTime(simTime)
    #print(rideRequestQueue.qsize)
    
    #print("Ride Request List: ", list(rideRequestQueue.queue))
    for ride in list(rideRequestQueue.queue):
       print("Ride Queue: ",ride.id,ride.dropoff)

    #print("Made it through determining what riders are requesting loop")
    #print("Length of vehicles",len(vehicles))
   
#Assign and Progress Rides
    for vehicle in vehicles:
        #print("I'm in the loop")
        #print("Vehicle: ",vehicle.id, vehicle.status)
        #print(rideRequestQueue.empty(),"if statement eval: ",vehicle.status == "Waiting for Request")# and not rideRequestQueue.empty())
        
        if vehicle.status == "Waiting for Request" and (not rideRequestQueue.empty()):
            print("I'm in the first if statement") 
            vehicle.assignRider(rideRequestQueue.get())
            print(vehicle.assignedRider)
            vehicle.assignedRider.assignVehicle(vehicle)
            vehicle.setStatus("En-route to pickup")
            vehicle.assignedRider.setStatus("Waiting for pickup")
            print(vehicle.status)
            vehicle.timeLeftOnTrip=calcTravelTime(vehicle.Location,vehicle.assignedRider.Location)
            print(vehicle.timeLeftOnTrip)
            vehicle.assignedRider.timeLeftOnTrip=calcTravelTime(vehicle.Location,vehicle.assignedRider.Location)
            print(vehicle.assignedRider.timeLeftOnTrip)
            print(vehicle.assignedRider.id, vehicle.assignedRider.assignedVehicle.id, vehicle.assignedRider.Location,vehicle.assignedRider.dropoff,vehicle.assignedRider.status, vehicle.status, vehicle.assignedRider.timeLeftOnTrip,vehicle.assignedRider.timeLeftOnTrip )
            vehicle.assignedRider.enRouteToPickupTimes.append(simTime)
        
        if vehicle.timeLeftOnTrip <= 0 and vehicle.status =="En-route to pickup":
            print("I'm in the second if statement")
            vehicle.assignedRider.savePickupTime(simTime)
            vehicle.Location = vehicle.assignedRider.Location
            vehicle.timeLeftOnTrip=calcTravelTime(vehicle.Location,vehicle.assignedRider.dropoff)
            vehicle.assignedRider.timeLeftOnTrip=calcTravelTime(vehicle.Location,vehicle.assignedRider.dropoff)        
            vehicle.assignedRider.setStatus("En-route to dropoff")
            vehicle.setStatus("En-route to dropoff")
            print(vehicle.assignedRider.id, vehicle.assignedRider.assignedVehicle.id, vehicle.assignedRider.Location,vehicle.assignedRider.dropoff,vehicle.assignedRider.status, vehicle.status, vehicle.assignedRider.timeLeftOnTrip,vehicle.assignedRider.timeLeftOnTrip )
        
        if vehicle.timeLeftOnTrip <= 0 and vehicle.status =="En-route to dropoff":
            print("I'm in the last if statement")
            vehicle.assignedRider.Location = vehicle.assignedRider.dropoff
            vehicle.assignedRider.saveDropoffTime(simTime)
            vehicle.Location = vehicle.assignedRider.Location   
            vehicle.assignedRider.setStatus("Waiting to Request")
            vehicle.setStatus("Waiting for Request")
            vehicle.assignedRider.numCompletedTrips += 1
            vehicle.assignedRider.chooseDropoff()
            if vehicle.assignedRider.numCompletedTrips <2:    
                vehicle.assignedRider.generateRequestTime(simTime, waveSpacing,mean,stdev)
            print(vehicle.assignedRider.id, vehicle.assignedRider.assignedVehicle.id, vehicle.assignedRider.Location,vehicle.assignedRider.dropoff,vehicle.assignedRider.status, vehicle.status, vehicle.assignedRider.timeLeftOnTrip,vehicle.assignedRider.timeLeftOnTrip )
        if vehicle.status =="En-route to pickup" or vehicle.status == "En-route to dropoff":
            vehicle.timeLeftOnTrip -= 1
            vehicle.assignedRider.timeLeftOnTrip -=1
    
    simTime +=1
    #print("simTime", simTime)
    #sleep(3)

for rider in riders:
    print(rider.requestTimes,rider.enRouteToPickupTimes,rider.pickupTimes, rider.dropoffTimes)
    rider.queueWaitTimes = [a - b for a, b in zip(rider.enRouteToPickupTimes,rider.requestTimes)]
    allQueueWaitTimes.append(rider.queueWaitTimes)
    rider.waitTimes = [a - b for a, b in zip(rider.pickupTimes,rider.enRouteToPickupTimes)]
    allWaitTimes.append(rider.waitTimes)
    rider.totalWaitTimes = [a - b for a, b in zip(rider.pickupTimes,rider.requestTimes)]
    allTotalWaitTimes.append(rider.totalWaitTimes)
    rider.rideTimes = [a - b for a, b in zip(rider.dropoffTimes,rider.pickupTimes)]
    allRideTimes.append(rider.rideTimes)
    
    #print(rider.waitTimes)
    print("Average Wait Time in the Queue: ",np.mean(rider.queueWaitTimes))
    print("Average Wait Time for pickup: ",np.mean(rider.waitTimes))
    print("Average Total Wait Time: ",np.mean(rider.totalWaitTimes))
    print("Average Ride Times: ", np.mean(rider.rideTimes))
    print("Total Time of Event: ", simTime)
          
    #print(calcWaitTimes(rider.pickupTimes,rider.requestTimes))
# while i < len(vehicles):
#     print(vehicles[i].assignedRider.id, riders[i].assignedVehicle.id, riders[i].Location,riders[i].dropoff,riders[i].status, vehicles[i].status, riders[i].timeLeftOnTrip,vehicles[i].timeLeftOnTrip )
#     i+=1
# print("***")
# 
# for elem in list(rideRequestQueue.queue):
#     print(elem.id, elem.dropoff)  