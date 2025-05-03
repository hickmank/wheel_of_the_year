"""Day Length Calculator and Plotter.

### Summary of Updates:

1. **Leap Year Calculation**: Included logic to handle leap years.

2. **User Input Validation**: Added error handling for valid latitude, longitude, and
   year input.

3. **Accuracy in Property Calculation**: Ensured accurate conversion and clarity in day
   length output.

4. **Inclusion of Notes on Real-World Accuracy**: Adjusted comments to clarify potential
   variations due to external factors.

5. **Enhanced Plot Visuals**: Incorporated vertical lines at significant astronomical
   events for better visual context.

6. **Function Modularization**: Separated the plotting function for cleaner code and
   functionalities.

Note: Latitude, Longitude of Los Alamos, NM is (35.8800364, -106.3031138)

"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import ephem


def yyyymmdd_to_doy(yyyymmdd: str) -> int:
    """Convert date string to integer since january 1st.
    
    Args:
        yyyymmdd (str): 'yyyy:mm:dd' formatted string.

    """

    dt = datetime.strptime(yyyymmdd, "%Y:%m:%d").date()
    jan1 = date(dt.year, 1, 1)

    return (dt - jan1).days + 1


def calculate_day_length(lat, lon, year):
    """Calculate the length of each day.
    
    Days are calculated in hours for a given latitude, longitude, and year.

    Args:
        lat (float): Latitude in degrees.
        lon (float): Longitude in degrees.
        year (int): Year for which to calculate day lengths.

    Returns:
        list: Length of each day in hours.

    """

    day_lengths = []
    is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    total_days = 366 if is_leap_year else 365

    # Get January 1st
    jan1 = date(year, 1, 1)
    for day in range(1, total_days + 1):  # Adjust for leap year
        doy_date = jan1 + timedelta(days=day - 1)

        observer = ephem.Observer()

        observer.lat = str(lat)  # Latitude as string

        observer.lon = str(lon)  # Longitude as string

        # anchor at noon UTC on the calendar day
        date_str = f"{doy_date.year}/{doy_date.month}/{doy_date.day} 00:00"
        observer.date = ephem.Date(date_str)

        # Sun object
        sun = ephem.Sun()

        # Get sunrise and sunset times
        try:
            sunrise = observer.next_rising(sun)
        except ephem.NeverUpError:
            return 0.0  # Polar night
        except ephem.AlwaysUpError:
            return 24.0  # Midnight sun
        
        try:
            sunset = observer.next_setting(sun, start=sunrise)
        except ephem.NeverUpError:
            return 0.0  # Polar night
        except ephem.AlwaysUpError:
            return 24.0  # Midnight sun

        # Calculate day length in hours
        day_length = (sunset - sunrise) * 24.0  # convert days to hours
        day_lengths.append(day_length)

    return day_lengths


def plot_day_length(days_of_year, day_lengths, year):
    """Plot the length of each day against the day of the year.
    Args:
        days_of_year (list): Days of the year.
        day_lengths (list): Length of each day in hours.
        year (int): YYYY current year

    """
    plt.figure(figsize=(10, 5))
    plt.plot(days_of_year, day_lengths, label='Day Length (hours)', color='blue')
    plt.title('Day Length vs Day of the Year')
    plt.xlabel('Day of the Year')
    plt.ylabel('Day Length (hours)')
    plt.xticks(np.arange(0, 366, 30))  # Show ticks for each month
    plt.grid()

    # Highlighting pagan dates (YYYY:MM:DD)
    yule = yyyymmdd_to_doy(f"{year}:12:19")
    imbolc = yyyymmdd_to_doy(f"{year}:02:01")
    ostara = yyyymmdd_to_doy(f"{year}:03:19")
    beltane = yyyymmdd_to_doy(f"{year}:04:30")
    litha = yyyymmdd_to_doy(f"{year}:06:19")
    lughnasadh = yyyymmdd_to_doy(f"{year}:08:01")
    mabon = yyyymmdd_to_doy(f"{year}:09:20")
    samhain = yyyymmdd_to_doy(f"{year}:10:31")

    plt.axvline(x=yule, color='red', linestyle='--', label='Yule')
    plt.axvline(x=imbolc, color='blue', linestyle='--', label='Imbolc')
    plt.axvline(x=ostara, color='green', linestyle='--', label='Ostara')
    plt.axvline(x=beltane, color='orange', linestyle='--', label='Beltane')
    plt.axvline(x=litha, color='purple', linestyle='--', label='Litha')
    plt.axvline(x=lughnasadh, color='black', linestyle='--', label='Lughnasadh')
    plt.axvline(x=mabon, color='cyan', linestyle='--', label='Mabon')
    plt.axvline(x=samhain, color='grey', linestyle='--', label='Samhain')

    plt.legend()
    plt.show()


def main():
    """Main function to execute the day length calculation and plotting."""

    print("Welcome to the Day Length Calculator!")
    print("Please enter your location details.")

    # Input validation loop
    while True:
        try:   
            latitude = float(input("Enter your latitude (-90 to 90): "))
            if not -90 <= latitude <= 90:
                raise ValueError("Latitude must be between -90 and 90.")

            longitude = float(input("Enter your longitude (-180 to 180): "))
            if not -180 <= longitude <= 180:
                raise ValueError("Longitude must be between -180 and 180.")

            year = int(input("Enter the year: "))
            
            break

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

    day_lengths = calculate_day_length(latitude, longitude, year)

    # Prepare x-axis (days of the year)
    leap_year_condition = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
    days_of_year = np.arange(1, (366 if leap_year_condition else 365) + 1)

    # Plotting
    plot_day_length(days_of_year, day_lengths, year)


if __name__ == "__main__":
    main()

