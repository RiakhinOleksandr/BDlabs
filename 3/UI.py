import domain
import sqlalchemy as sa
from datetime import datetime

if __name__ == "__main__":
    try:
        print("Choose option:\n1 - find weather by country, location and time\n2 - find weather by country and location for a whole day\n0 - End program:")
        choose = input()
        print()
        while choose != "0":
            if choose == "1":
                print("Enter country:")
                country = input()
                print("Enter location:")
                location_name = input()
                print("Enter time (year-month-day hour:minute):")
                last_updated = input()
                res = domain.get_weather_conditions(country, location_name, last_updated)
                if res is None:
                    print("We have no information about this place or this time")
                else:
                    print("This is what we've got about this time and place")
                    print(f"Temperature will be: {res[0]} C")
                    print(f"Speed of wind will be: {res[1]} kilometers per hour")
                    print(f"Direction of wind will be: {res[2]}")
                    print(f"There will be: {res[3]} millimeters of precipitation")
                    print(f"Humidity will be: {res[4]}%")
                    print(f"Cloud will be covered by: {res[5]}%")
                    if res[6]:
                        print("The weather is good. Maybe you should go for a walk")
                    else:
                        print("The weather is not that good. We don't recommend you to go for a walk")
                    print()
            elif choose == "2":
                print("Enter country:")
                country = input()
                print("Enter location:")
                location_name = input()
                print("Enter time (year-month-day):")
                date = input()
                res = domain.get_weather_for_day(country, location_name, date)
                if res is None:
                    print("we have no information about this day")
                else:
                    for row in res:
                        print(f"The weather at {row[0].strftime("%H:%M:%S")} will be:")
                        print(f"Temperature will be: {row[1]} C")
                        print(f"Speed of wind will be: {row[2]} kilometers per hour")
                        print(f"Direction of wind will be: {row[3]}")
                        print(f"There will be: {row[4]} millimeters of precipitation")
                        print(f"Humidity will be: {row[5]}%")
                        print(f"Cloud will be covered by: {row[6]}%")
                        if row[7]:
                            print("The weather is good. Maybe you should go for a walk")
                        else:
                            print("The weather is not that good. We don't recommend you to go for a walk")
                        print()
            print("Choose option:\n1 - find weather by country, location and time\n2 - find weather by country and location for a whole day\n0 - End program:")
            choose = input()
    except Exception as e:
        print(repr(e))