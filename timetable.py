# Function to print the title and author information as mentioned in the assignment
def print_header():
    print("Timetable Generator")
    print()


# In the following section, we have worked on the validations and pre-requisites of the code.

# Function to create empty timetable based on 7 days of the week.
def create_timetable():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    timetable = {day: [] for day in days}
    return timetable


"""We have used all the 7 days of the week to create entries of the timetable in a list form"""


# Function to validate the days of the week
def validate_day(day):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if day.capitalize() in days:
        return day.capitalize()
    else:
        return None


"""For all the 7 days of the week, we have used the exact spellings of the days as a 
validation criterion. We have also used the capitalize function so that the validation 
relates with the original list in create_timetable."""


# Function to validate time format based on hour granularity.
def validate_time(time_str):
    if len(time_str) < 7 or len(time_str) > 8:
        return None
    if time_str[-2:].lower() not in ["am", "pm"]:
        return None
    time_part = time_str[:-2]
    if ':' not in time_part:
        return None
    hour_part, minute_part = time_part.split(":")
    if not (hour_part.isdigit() and minute_part.isdigit()):
        return None
    hour = int(hour_part)
    minute = int(minute_part)
    if hour < 1 or hour > 12 or minute < 0 or minute >= 60:
        return None
    return time_str


"""The validation criterion for the time input has been set here keeping in mind 
the hour and minute formats. We have also used split to inculcate the ':' for the time 
input."""

# Function to convert time string to 24-hour format for further validation
def convert_to_24_hour(time_str):
    period = time_str[-2:].lower()
    hour, minute = map(int, time_str[:-2].split(":"))
    if period == "pm" and hour != 12:
        hour += 12
    if period == "am" and hour == 12:
        hour = 0
    return hour, minute

"""We have converted the time into 24 hour format based on the am/pm input so that 
the overlap function can interpret overlapping in time of any scheduled event."""


# Function to check for time overlap
def check_overlap(day, start_time, end_time, timetable, exclude_index=None):
    start_hour, start_minute = convert_to_24_hour(start_time)
    end_hour, end_minute = convert_to_24_hour(end_time)

    for i, event in enumerate(timetable[day]):
        if exclude_index is not None and i == exclude_index:
            continue
        event_start_hour, event_start_minute = convert_to_24_hour(event[1])
        event_end_hour, event_end_minute = convert_to_24_hour(event[2])

        start_total_minutes = start_hour * 60 + start_minute
        end_total_minutes = end_hour * 60 + end_minute
        event_start_total_minutes = event_start_hour * 60 + event_start_minute
        event_end_total_minutes = event_end_hour * 60 + event_end_minute

        if start_total_minutes < event_end_total_minutes and end_total_minutes > event_start_total_minutes:
            return True
    return False


"""In this section of the code, we have converted the time into minutes for the start and end time of the 
 overall day so that overlap of time can be checked and avoid any overlaps in the timetable events."""


# We have now established the pre-requisites of the code as well as the input validations.
# We will now work on creating the functions of the menu.

# Function to add an activity to the timetable
def add_activity(timetable):
    day = None
    while not day:
        day_input = input("Enter the day of the week: ")
        day = validate_day(day_input)
        if not day:
            print("Invalid day. Please enter a valid day of the week.")

    """We have requested an input from the user for entering the day of the week to analyze the entry of the event. 
    The entry will correspond to create_timetable and validate the entry using validate_day."""

    title = input("Enter the event title: ")

    start_time = None
    while not start_time:
        start_time_input = input("Enter the start time (e.g., 09:30am): ")
        start_time = validate_time(start_time_input)
        if not start_time:
            print("Invalid time format. Please enter a valid start time (e.g., 09:30am).")

    end_time = None
    while not end_time:
        end_time_input = input("Enter the end time (e.g., 11:00am): ")
        end_time = validate_time(end_time_input)
        if not end_time:
            print("Invalid time format. Please enter a valid end time (e.g., 11:00am).")

    if check_overlap(day, start_time, end_time, timetable):
        print("The specified time overlaps with an existing event. Please reschedule.")
        return

    """After validation of the day, we request the start and end time from the user which is 
    then validated using check_overlap criterion"""

    location = input("Enter the location (optional): ")

    timetable[day].append((title, start_time, end_time, location))
    print("Activity added successfully!")

    """After checking all the validations and overlap of time, the user is then 
    asked to enter a location for the event which is an optional area of information."""


# Function to update an activity in the timetable
def update_activity(timetable):
    day = None
    while not day:
        day_input = input("Enter the day of the week: ")
        day = validate_day(day_input)
        if not day:
            print("Invalid day. Please enter a valid day of the week.")

    title = input("Enter the title of the event to update: ")

    for i, activity in enumerate(timetable[day]):
        if title.lower() in activity[0].lower():
            print(f"Updating event: {activity[0]} from {activity[1]} to {activity[2]} at {activity[3]}")
            new_title = input("Enter new event title (or press Enter to keep current): ") or activity[0]
            new_start_time = input("Enter new start time (or press Enter to keep current): ") or activity[1]
            new_end_time = input("Enter new end time (or press Enter to keep current): ") or activity[2]

            if check_overlap(day, new_start_time, new_end_time, timetable, exclude_index=i):
                print("The specified time overlaps with an existing event. Please reschedule.")
                return

            location = input("Enter new location (or press Enter to keep current): ") or activity[3]
            timetable[day][i] = (new_title, new_start_time, new_end_time, location)
            print("Activity updated successfully!")
            return

    print("No event found with the specified title.")

    """To update any event we have used a number of steps as specified below:- 
    1.) The user is asked for the day the event to be updated is on which is validated through 'validate_day'.
    2.) After the day has been specified, the user will be required to enter the title of the event.
    3.) Once both the inputs are validated and relate to an event in the timetable, the program will ask for
    new inputs for changing the title, start time, and end time which will again be validated 
    through 'validate_time'. The new time inputs before registering will also be checked for time overlap through
    check_overlap"""

# Function to delete an activity from the timetable
def delete_activity(timetable):
    day = None
    while not day:
        day_input = input("Enter the day of the week: ")
        day = validate_day(day_input)
        if not day:
            print("Invalid day. Please enter a valid day of the week.")

    title = input("Enter the title of the event to delete: ")

    for i, activity in enumerate(timetable[day]):
        if title.lower() in activity[0].lower():
            print(f"Deleting event: {activity[0]} from {activity[1]} to {activity[2]} at {activity[3]}")
            del timetable[day][i]
            print("Activity deleted successfully!")
            return

    print("No event found with the specified title.")
"""This section of the code has been written to delete an event from the timetable which has the following functions:-
1.) The user is asked for the day of the week on which the event to be deleted is one which is 
validated through 'validate_day'. 
2.) After the day has been defined and validated, the user is asked for the title of the event.
3.) After the day has been defined and validated, the user is asked for the start time of the event which 
is validated through 'validate_time'.
"""
# Function to display the timetable
def display_timetable(timetable):
    start_day = input("Enter the first day of the week : ")
    start_day = validate_day(start_day)
    if not start_day:
        print("Invalid day entered. Please enter a valid day of the week.")
        return

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    start_index = days.index(start_day)
    ordered_days = days[start_index:] + days[:start_index]

    for day in ordered_days:
        print(f"\n{day}:")
        if not timetable[day]:
            print("  No activities scheduled.")
        else:
            for activity in timetable[day]:
                location_str = f" at {activity[3]}" if activity[3] else ""
                print(f"  {activity[1]} - {activity[2]}: {activity[0]}{location_str}")
"""To display the events of the timetable, we have first asked for the first day of the week to be 
considered and related from the initial list 'days' which has been referenced here again. """
# Function to save the timetable to a file
def save_timetable(timetable):
    file_name = input("Enter the file name to save the timetable: ")
    with open(file_name, 'w') as file:
        for day, activities in timetable.items():
            for activity in activities:
                file.write(f"{day},{activity[0]},{activity[1]},{activity[2]},{activity[3]}\n")
    print("Timetable saved successfully!")
"""When the user wants to save the timetable as a file we will ask for a file name input and use 
a write function to save the file with the dedicated file name. Further 'for' loops have been 
used to cumulate all the events of the timetable."""

# Function to load the timetable from a file
def load_timetable():
    file_name = input("Enter the file name to load the timetable: ")
    try:
        with open(file_name, 'r') as file:
            timetable = create_timetable()
            for line in file:
                day, title, start_time, end_time, location = line.strip().split(',')
                timetable[day].append((title, start_time, end_time, location))
        print("Timetable loaded successfully!")
        return timetable
    except FileNotFoundError:
        print("File not found. Please try again.")
        return create_timetable()

"""To load a file from the local directory of the computer's python project, we have asked 
for the file name as an input from the user and a 'read' function to read the file and load 
the contents of the file. We have used a 'FileNotFoundError' in the case the file is not found 
on the local directory."""

# Function to print events for a specific day in chronological order
def print_events_for_day(timetable):
    day = None
    while not day:
        day_input = input("Enter the day of the week to print events: ")
        day = validate_day(day_input)
        if not day:
            print("Invalid day. Please enter a valid day of the week.")

    events = timetable[day]
    if not events:
        print(f"No events scheduled for {day}.")
        return

    events.sort(key=lambda event: convert_to_24_hour(event[1]))
    print(f"\nEvents scheduled for {day}:")
    for event in events:
        print(f"  {event[1]} - {event[2]}: {event[0]} at {event[3]}")

"""For printing events specific to a day we have first asked the user for the day he/she 
wants to print the events for and the input is validated through 'validate_day. 
 Once the day has been validated, the events will be sorted through the lambda function and
 the output will be printed"""


def search_event(timetable):
    search_criterion = input("Enter search criterion (title/location): ").strip().lower()
    if search_criterion not in ["title", "location"]:
        print("Invalid search criterion. Please enter 'title' or 'location'.")
        return

    search_value = input(f"Enter the {search_criterion} to search for: ").strip().lower()
    events_found = []

    for day, events in timetable.items():
        for event in events:
            if search_criterion == "title" and search_value in event[0].lower():  # event[0] is title
                events_found.append((day, event))
            elif search_criterion == "location" and search_value in event[3].lower():  # event[3] is location
                events_found.append((day, event))

    if events_found:
        print(f"Events found matching {search_criterion} '{search_value}':")
        for day, event in events_found:
            print(f"{day}: {event[0]} ({event[1]} - {event[2]}) at {event[3]}")
    else:
        print(f"No events found matching {search_criterion} '{search_value}'.")



# Main function
def main():
    print_header()
    timetable = create_timetable()

    while True:
        print("\nTimetable Generator")
        print("1. Add an activity")
        print("2. Update an activity")
        print("3. Delete an activity")
        print("4. Display timetable")
        print("5. Save timetable")
        print("6. Load timetable")
        print("7. Print events for a specific day")
        print("8. Search event")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_activity(timetable)
        elif choice == '2':
            update_activity(timetable)
        elif choice == '3':
            delete_activity(timetable)
        elif choice == '4':
            display_timetable(timetable)
        elif choice == '5':
            save_timetable(timetable)
        elif choice == '6':
            timetable = load_timetable()
        elif choice == '7':
            print_events_for_day(timetable)
        elif choice == '8':
            search_event(timetable)
        elif choice == '9':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()