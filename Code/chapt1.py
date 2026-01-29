#Here are some exercises in Chapter 1

#How many seconds are there in 42 minutes 42 seconds
min = 42
sec = 42
ans = (60*min)+sec
print(ans)

#How many miles are there in 10 km?
kmpermile = 1.61
miles = 10/kmpermile
print(miles)

#If you run a 10 kilometer race in 42 minutes 42 seconds, what is your average pace in seconds per mile?
pacesec = ans/miles
print(pacesec)

#What is your average pace in minutes per mile?
pacemin = pacesec/60
print(pacemin)
#or
pacemin = ans/miles*60
print(pacemin)

#What is your average speed in miles per hour?
speed = pacemin/60
print(speed)
#or
speed = (ans*360)/miles
print(speed)