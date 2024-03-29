
"""
COVID Vaccine Slot Availability Notifier
"""

import requests
from pygame import mixer
from datetime import datetime, timedelta
import time
import json

AGE = int(input("Enter your age: \n"))
age = AGE

PIN = input("Enter your Pincode: \n")
pincode = PIN

DAYS = int(input("Enter no. of days for which you want to check availability of vaccine slots: \n"))
num_days = DAYS

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
#print(actual)

list_format = [actual + timedelta(days=i) for i in range(num_days)]
#print(list_format)

actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
#print(actual_dates)

while True:
    counter = 0

    for pin in pincode:

        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

            result = requests.get(URL, headers=header)
            #print(result.text)

            if result.ok:
                response_json = result.json()
                if response_json["centers"]:
                    if(print_flag.lower() =='y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                    print('Pincode: ' + pincode)
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])

                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                    print("\n")
                                    counter += 1
                                    mixer.init()
                                    mixer.music.load('sound_dingdong.wav')
                                    mixer.music.play()
                                    time.sleep(1)
            else:
                print("No Response!")

    if counter==0:
        print("No Vaccination slot available!")
    else:
        mixer.init()
        mixer.music.load('sound_dingdong.wav')
        mixer.music.play()
        print("Search Completed!")
        print(f"{str(counter)} Covid Vaccine Slot Available in next {str(num_days)} days")

    dt = datetime.now() + timedelta(minutes=3)

    while datetime.now() < dt:
        time.sleep(1)
