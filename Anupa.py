# Author: S.T.Gallage
# Date: 2024-12-09
# Student ID: w2121292

# Task A: Input Validation
import csv
import tkinter as tk
import matplotlib.pyplot as plt

def validate_date():
    """Validates the user input and ensures correct format and range."""
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if day < 1 or day > 31:
                print("Out of range - values must be in the range 1 and 31.")
                continue
        except ValueError:
            print("Integer required")
            continue
        day = f"{day:02d}"

        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if month < 1 or month > 12:
                print("Out of range - values must be in the range 1 to 12.")
                continue
        except ValueError:
            print("Integer required")
            continue
        month = f"{month:02d}"

        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if year < 2000 or year > 2024:
                print("Out of range - values must range from 2000 and 2024.")
                continue
        except ValueError:
            print("Integer required")
            continue

        csvfile = f"traffic_data{day}{month}{year}.csv"
        return csvfile, day, month, year

def load_file(file_name):
    try:
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
            if not data:
                print("Empty file.")
                return False
    except FileNotFoundError:
        print(f"Error: File {file_name} does not exist.")
        return False
    print(f"CSV File loaded: {file_name}")
    return True

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input        
    """
    while True:
        choice = input("Do you want to select another data file for a different date? Y/N > ").strip().upper()
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print('Please enter “Y” or “N"')

# Task B: Processed Outcomes
def analyze_traffic_data(file_name):
    total_vehicles = 0
    total_trucks = 0
    total_electric_vehicles = 0
    two_wheeled_vehicles = 0
    buses_north_elm = 0
    vehicles_no_turn = 0
    total_bicycles = 0
    vehicles_over_speed_limit = 0
    vehicles_elm_avenue = 0
    vehicles_hanley = 0
    scooters = 0
    hanley_hours = {}
    rain_hours = set()
    traffic_data = []

    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_vehicles += 1

            if row['VehicleType'] == 'Truck':
                total_trucks += 1

            if row['elctricHybrid'] == 'True':
                total_electric_vehicles += 1

            if row['VehicleType'] in ['Bicycle', 'Motorcycle']:
                two_wheeled_vehicles += 1

            if row['JunctionName'] == 'Elm Avenue/Rabbit Road' and row['travel_Direction_out'] == 'N' and row['VehicleType'] == 'Buss':
                buses_north_elm += 1

            if row['travel_Direction_in'] == row['travel_Direction_out']:
                vehicles_no_turn += 1

            if row['VehicleType'] == 'Bicycle':
                total_bicycles += 1

            if float(row['VehicleSpeed']) > float(row['JunctionSpeedLimit']):
                vehicles_over_speed_limit += 1

            if row['JunctionName'] == 'Elm Avenue/Rabbit Road':
                vehicles_elm_avenue += 1
                if row['VehicleType'] == 'Motorcycle':
                    scooters += 1

            if row['JunctionName'] == 'Hanley Highway/Westway':
                vehicles_hanley += 1
                hour = int(row['timeOfDay'].split(':')[0])
                hanley_hours[hour] = hanley_hours.get(hour, 0) + 1

            if 'Rain' in row['Weather_Conditions']:
                hour = int(row['timeOfDay'].split(':')[0])
                rain_hours.add(hour)

            traffic_data.append(row)  # Collect raw data

    percentage_trucks = round((total_trucks / total_vehicles) * 100) if total_vehicles > 0 else 0
    percentage_scooters = int((scooters / vehicles_elm_avenue) * 100) if vehicles_elm_avenue > 0 else 0
    avg_bicycles_per_hour = round(total_bicycles / 24) if total_bicycles > 0 else 0
    peak_hour_hanley = max(hanley_hours, key=hanley_hours.get, default=None)
    peak_hour_count_hanley = hanley_hours.get(peak_hour_hanley, 0)
    no_rain_hours = len(rain_hours)

    outcomes = {
        "file_name": file_name,
        "total_vehicles": total_vehicles,
        "total_trucks": total_trucks,
        "total_electric_vehicles": total_electric_vehicles,
        "two_wheeled_vehicles": two_wheeled_vehicles,
        "buses_north_elm": buses_north_elm,
        "vehicles_no_turn": vehicles_no_turn,
        "percentage_trucks": percentage_trucks,
        "avg_bicycles_per_hour": avg_bicycles_per_hour,
        "vehicles_over_speed_limit": vehicles_over_speed_limit,
        "vehicles_elm_avenue": vehicles_elm_avenue,
        "vehicles_hanley": vehicles_hanley,
        "percentage_scooters": percentage_scooters,
        "peak_hour_hanley": peak_hour_hanley,
        "peak_hour_count_hanley": peak_hour_count_hanley,
        "no_rain_hours": no_rain_hours,
        "traffic_data": traffic_data  # Include raw data for histogram
    }

    return outcomes

def display_outcomes_and_save(outcomes, saveToFile=False):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    output = (
        f"\nData file selected is {outcomes['file_name'].split('/')[-1]}.\n\n"
        f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}.\n"
        f"The total number of trucks recorded for this date is {outcomes['total_trucks']}.\n"
        f"The total number of electric vehicles for this date is {outcomes['total_electric_vehicles']}.\n"
        f"The total number of two-wheeled vehicles for this date is {outcomes['two_wheeled_vehicles']}.\n"
        f"The total number of buses leaving Elm Avenue/Rabbit Road heading North is {outcomes['buses_north_elm']}.\n"
        f"The total number of vehicles through both junctions not turning left or right is {outcomes['vehicles_no_turn']}.\n"
        f"The average number of bikes per hour for this date is {outcomes['avg_bicycles_per_hour']}.\n"
        f"Percentage of total vehicles recorded that are trucks for this date is {outcomes['percentage_trucks']}%.\n"
        f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['vehicles_over_speed_limit']}.\n"
        f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['vehicles_elm_avenue']}.\n"
        f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['vehicles_hanley']}.\n"
        f"{outcomes['percentage_scooters']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n"
        f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['peak_hour_count_hanley']}.\n"
        f"The most vehicles through Hanley Highway/Westway were recorded between {outcomes['peak_hour_hanley']:02d}:00 and {outcomes['peak_hour_hanley'] + 1:02d}:00.\n"
        f"The number of hours of rain for this date is {outcomes['no_rain_hours']}.\n"
        f"****************************\n"
    )

    print(output)
    
    # Save to file if requested
    if saveToFile:
        with open("results.txt", mode="a") as f:
            f.write(output)
        print("Results saved to results.txt.")

# Task D: Histogram Display
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None  # Will hold the canvas for drawing

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title(f"Histogram of Vehicle Frequency per Hour ({self.date})")
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

    def draw_histogram(self):
        """
        Draws the histogram with two separate bars for each hour: one for Elm Avenue/Rabbit Road,
        and one for Hanley Highway/Westway.
        """
        hours = [str(i).zfill(2) for i in range(24)]
        elm_counts = [0] * 24  # Placeholder for Elm Avenue/Rabbit Road
        hanley_counts = [0] * 24  # Placeholder for Hanley Highway/Westway
        
        # Count vehicles per hour for each junction
        for row in self.traffic_data:
            hour = int(row['timeOfDay'].split(":")[0])
            if row['JunctionName'] == "Elm Avenue/Rabbit Road":
                elm_counts[hour] += 1
            elif row['JunctionName'] == "Hanley Highway/Westway":
                hanley_counts[hour] += 1

        # Plot the histogram using matplotlib
        bar_width = 0.35  # Set width for the bars
        index = range(24)
        
        plt.figure(figsize=(10,6))

        # Plot Elm Avenue/Rabbit Road bars (shifted to the left)
        plt.bar([i - bar_width / 2 for i in index], elm_counts, width=bar_width, color='green', label='Elm Avenue/Rabbit Road')

        # Plot Hanley Highway/Westway bars (shifted to the right)
        plt.bar([i + bar_width / 2 for i in index], hanley_counts, width=bar_width, color='red', label='Hanley Highway/Westway')
        
        plt.xlabel("Hours 00:00 to 24:00")
        plt.ylabel("Vehicle Frequency")
        plt.title(f"Histogram of Vehicle Frequency per Hour ({self.date})")
        plt.legend(loc='upper left')
        plt.xticks(index, hours)
        plt.tight_layout()
        plt.show()

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.root.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files
def main():
    while True:
        csvfile, day, month, year = validate_date()

        if load_file(csvfile):
            result = analyze_traffic_data(csvfile)
            display_outcomes_and_save(result, saveToFile=True)

            # After displaying results, show the histogram
            histogram_app = HistogramApp(result['traffic_data'], f"{day}/{month}/{year}")
            histogram_app.run()
        
        if not validate_continue_input():
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()
