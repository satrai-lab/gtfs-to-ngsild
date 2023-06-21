import csv
import json
import datetime
import uuid
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import sys
from collections import defaultdict



version="0.04"
context="https://raw.githubusercontent.com/SAMSGBLab/iotspaces-DataModels/main/transportation-models/context.json"



import tkinter as tk
from tkinter import ttk

# Define the global options dictionary
options_dict = {
    "All (default)": False,
    "Agency": False,
    "CalendarRule": False,
    "Routes": False,
    "Shapes": False,
    "Stops": False,
    "Trips": False,
    "StopTimes": False,
}

Conversion=False


# Function to handle the selection event
def on_selection(event):
    global options_dict  # Access the global options_dict variable
    selected_option = combo.get()
    
    # Set all options to False, except for the selected one
    for key in options_dict.keys():
        options_dict[key] = False

    options_dict[selected_option] = True
    print(f"Selected option: {selected_option}")
    print(f"Options dictionary: {options_dict}")




# Create the main window
root = ThemedTk(theme="arc")
root.title("GTFS to NGSI-LD converter")


# Create a welcome label
label2 = ttk.Label(root, text="Welcome to the GTFS to NGSI-LD entities converter, version " + version)
label2.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="w")

# Create a label for selecting options
label = ttk.Label(root, text="Select an option:")
label.grid(column=0, row=1, padx=10, pady=10, sticky="w")

# Create a combobox for selecting options
options = list(options_dict.keys())
combo = ttk.Combobox(root, values=options)
combo.grid(column=1, row=1, padx=10, pady=10, sticky="w")

combo.bind("<<ComboboxSelected>>", on_selection)


# Create a button to close the application
close_button = ttk.Button(root, text="Close", command=root.quit)
close_button.grid(column=2, row=2, padx=10, pady=10, sticky="w")


def begin_conversion():
    
    if(options_dict["Agency"]==False and options_dict["All (default)"]==False):

        print("Skipping Agency...")
    else:

        print("Converting agency...")
        with open('agency.txt') as csvfile, open('Gtfsagency.ngsild', 'w') as outfile:
            reader = csv.DictReader(csvfile)
            outfile.write("[" + '\n')
            total_lines = sum(1 for row in reader)
            csvfile.seek(0)
            next(reader) # skip header

            current_line = 1
            for row in reader:
                entity = {
                    "id": "urn:ngsi-ld:GtfsAgency:Ioannina:SmartCitiesdomain:SmartCityBus:{}".format(row['agency_url']),
                    "type": "GtfsAgency",
                    "agencyName": {
                        "type": "Property",
                        "value": row['agency_name']
                    },
                    "language": {
                        "type": "Property",
                        "value": row['agency_lang']
                    },
                    "page": {
                        "type": "Property",
                        "value": row['agency_url']
                    },
                    "phone": {
                        "type": "Property",
                        "value": row['agency_phone']
                    },
                    "timezone": {
                        "type": "Property",
                        "value": row['agency_timezone']
                    },
                    "@context": [
                        context,
                        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
                    ]
                }
                outfile.write(json.dumps(entity, indent=2, ensure_ascii=False) + '\n')
                percentage_done = current_line / total_lines * 100
                if percentage_done!=100:
                    outfile.write("," + '\n')
                    
                print(f"Processed {current_line} out of {total_lines} lines ({percentage_done:.2f}%)")
                current_line += 1
            outfile.write("]" + '\n')     
        print("agency done!")

    print("------------------------------------------------------------------------------------------------------------------------------------")

    if(options_dict["CalendarRule"]==False and options_dict["All (default)"]==False):

        print("Skipping CalendarRule...")
    else:

        print("Converting calendar..")
        def convert_date(date_str):
            date_obj = datetime.datetime.strptime(date_str, '%Y%m%d')
            return {
                '@type': 'Date',
                '@value': date_obj.date().isoformat()
            }

        def convert_boolean(bool_str):
            return bool(int(bool_str))

        with open('calendar.txt', 'r', encoding='utf-8-sig') as csvfile,open('Gtfscalendar.ngsild', 'w') as outfile:
            reader = csv.DictReader(csvfile)
            outfile.write("[" + '\n')
            total_lines = sum(1 for row in reader)
            csvfile.seek(0)
            next(reader) # skip header

            current_line = 1
            for row in reader:
                #print(row)
                entity_id = f'urn:ngsi-ld:GtfsCalendarRule:Ioannina:SmartCitiesdomain:SmartCityBus:{row["service_id"]}'
                entity = {
                    'id': entity_id,
                    'type': 'GtfsCalendarRule',
                    "@context": [
                        context,
                        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
                    ]
                }
                if row.get("start_date"):
                        entity["startDate"] = {"type": "Property", "value": convert_date(row["start_date"])}

                if row.get("end_date"):
                    entity["endDate"] = {"type": "Property", "value": convert_date(row["end_date"])}

                if row.get("monday"):
                    entity["monday"] = {"type": "Property", "value": convert_boolean(row["monday"])}

                if row.get("tuesday"):
                    entity["tuesday"] = {"type": "Property", "value": convert_boolean(row["tuesday"])}

                if row.get("wednesday"):
                    entity["wednesday"] = {"type": "Property", "value": convert_boolean(row["wednesday"])}

                if row.get("thursday"):
                    entity["thursday"] = {"type": "Property", "value": convert_boolean(row["thursday"])}

                if row.get("friday"):
                    entity["friday"] = {"type": "Property", "value": convert_boolean(row["friday"])}

                if row.get("saturday"):
                    entity["saturday"] = {"type": "Property", "value": convert_boolean(row["saturday"])}

                if row.get("sunday"):
                    entity["sunday"] = {"type": "Property", "value": convert_boolean(row["sunday"])}

                if row.get("service_id"):
                    entity["name"] = {"type": "Property", "value": row["service_id"]}
                    entity["hasService"] = {"type": "Relationship", "object": f"urn:ngsi-ld:GtfsService:Ioannina:SmartCitiesdomain:SmartCityBus:{row['service_id']}"} 

                outfile.write(json.dumps(entity, indent=2, ensure_ascii=False) + '\n')
                percentage_done = current_line / total_lines * 100
                if percentage_done!=100:
                    outfile.write("," + '\n')
                    
                print(f"Processed {current_line} out of {total_lines} lines ({percentage_done:.2f}%)")
                current_line += 1
            outfile.write("]" + '\n')    
        print("Calendar done!")

    print("------------------------------------------------------------------------------------------------------------------------------------")

    if(options_dict["Routes"]==False and options_dict["All (default)"]==False):

        print("Skipping Routes...")
    else:

        print("Converting routes..")

        with open('routes.txt', 'r', encoding='utf-8-sig') as csvfile,open('Gtfsroutes.ngsild', 'w') as outfile:
            reader = csv.DictReader(csvfile)
            outfile.write("[" + '\n')
            entities = []
            total_lines = sum(1 for row in reader)
            csvfile.seek(0)
            next(reader) # skip header

            current_line = 1
            for row in reader:
                entity_id = f'urn:ngsi-ld:GtfsRoute:Ioannina:SmartCitiesdomain:SmartCityBus:{row["route_id"]}'
                entity = {
                    'id': entity_id,
                    'type': 'GtfsRoute',
                    'name': {
                        'type': 'Property',
                        'value': row['route_long_name']
                    },
                    'shortName': {
                        'type': 'Property',
                        'value': row['route_short_name']
                    },
                    'description': {
                        'type': 'Property',
                        'value': row['route_desc']
                    },
                    'routeType': {
                        'type': 'Property',
                        'value': row['route_type']
                    },
                    'routeColor': {
                        'type': 'Property',
                        'value': row['route_color']
                    },
                    'routeTextColor': {
                        'type': 'Property',
                        'value': row['route_text_color']
                    },
                    'operatedBy': {
                        'type': 'Relationship',
                        'object': f'urn:ngsi-ld:GtfsAgency:Ioannina:SmartCitiesdomain:SmartCityBus:astiko-ioannina'
                    },
                    "@context": [
                        context,
                        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
                    ]
                }
                outfile.write(json.dumps(entity, indent=2, ensure_ascii=False) + '\n')
                percentage_done = current_line / total_lines * 100
                if percentage_done!=100:
                    outfile.write("," + '\n')
                    
                print(f"Processed {current_line} out of {total_lines} lines ({percentage_done:.2f}%)")
                current_line += 1
            outfile.write("]" + '\n')  
        print("routes done!")
    print("------------------------------------------------------------------------------------------------------------------------------------")

    if(options_dict["Shapes"]==False and options_dict["All (default)"]==False):

        print("Skipping Shapes...")
    else:

        print("Converting shapes..")
        with open('shapes.txt', 'r', encoding='utf-8-sig') as csvfile, open('Gtfsshapes.ngsild', 'w') as outfile:
            reader = csv.DictReader(csvfile)
            
            # Create a dictionary to store line string for each shape_id
            lines_dict = defaultdict(list)

            for row in reader:
                # Add the current point to the shape line
                lines_dict[row["shape_id"]].append([
                    float(row['shape_pt_lon']),
                    float(row['shape_pt_lat'])
                ])

            entities = []
            for shape_id, coordinates in lines_dict.items():
                entity_id = f'urn:ngsi-ld:GtfsShape:Ioannina:SmartCitiesdomain:SmartCityBus:{shape_id}'

                entity = {
                    'id': entity_id,
                    'type': 'GtfsShape',
                    'location': {
                        'type': 'GeoProperty',
                        'value': {
                            'type': 'LineString',
                            'coordinates': coordinates
                        }
                    },
                    "@context": [
                        context,
                        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
                    ]
                }

                entities.append(entity)

            # Dump the JSON array into the output file
            json.dump(entities, outfile, indent=2, ensure_ascii=False)

        print("shapes done!")
    print("------------------------------------------------------------------------------------------------------------------------------------")

    if(options_dict["StopTimes"]==False and options_dict["All (default)"]==False):

        print("Skipping StopTimes...")
    else:
        print("Converting Stop_times..")
                

        with open('stop_times.txt', 'r', encoding='utf-8-sig') as csvfile,open('GtfsStopTimes.ngsild', 'w') as outfile:
            reader = csv.DictReader(csvfile)
            outfile.write("[" + '\n')

            # Loop over each row in the file and create an NGSI-LD entity
            total_lines = sum(1 for row in reader)
            csvfile.seek(0)
            next(reader) # skip header

            current_line = 1

            for row in reader:
                #print(row)
                entity_id = uuid.uuid4()
                entity = {
                    "id": f"urn:ngsi-ld:GtfsStopTime:Ioannina:SmartCitiesdomain:SmartCityBus:{entity_id}",
                    "type": "GtfsStopTime",
                    
                    "@context": [
                        context,
                        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
                    ]
                }


                # Check if optional attributes exist in the row and add them to the entity, I should do everything like this 
                if row.get("arrival_time"):
                    entity["arrivalTime"] = {"type": "Property", "value": row["arrival_time"]}
                if row.get("departure_time"):
                    entity["departureTime"] = {"type": "Property", "value": row["departure_time"]}
                if row.get("stop_sequence"):
                    entity["stopSequence"] = {"type": "Property", "value": row["stop_sequence"]}
                if row.get("pickup_type"):
                    entity["pickupType"] = {"type": "Property", "value": row["pickup_type"]}
                if row.get("drop_off_type"):
                    entity["dropOffType"] = {"type": "Property", "value": row["drop_off_type"]}
                if row.get("timepoint"):
                    entity["timepoint"] = {"type": "Property", "value": row["timepoint"]}



                if row.get("stop_headsign"):
                    entity["stopHeadsign"] = {"type": "Property", "value": row["stop_headsign"]}
                if row.get("shape_dist_traveled"):
                    entity["distanceTravelled"] = {"type": "Property", "value": row["shape_dist_traveled"]}
                if row.get("trip_id"):
                    entity["hasTrip"] = {"type": "Relationship", "object": f"urn:ngsi-ld:GtfsTrip:Ioannina:SmartCitiesdomain:SmartCityBus:{row['trip_id']}"}
                if row.get("stop_id"):
                    entity["hasStop"] = {"type": "Relationship", "object": f"urn:ngsi-ld:GtfsStop:Ioannina:SmartCitiesdomain:SmartCityBus:{row['stop_id']}"
                    }
                outfile.write(json.dumps(entity, indent=2, ensure_ascii=False) + '\n')
                percentage_done = current_line / total_lines * 100
                if percentage_done!=100:
                    outfile.write("," + '\n')
                    
                print(f"Processed {current_line} out of {total_lines} lines ({percentage_done:.2f}%)")

                current_line += 1
            outfile.write("]" + '\n')    
                
        print("Stop_Times done!")
    print("------------------------------------------------------------------------------------------------------------------------------------")

    if(options_dict["Stops"]==False and options_dict["All (default)"]==False):

        print("Skipping Stops...")
    else:

        print("Converting Stops..")        

        with open('stops.txt', 'r', encoding='utf-8-sig') as csvfile, open('GtfsStops.ngsild', 'w') as outfile:
            reader = csv.DictReader(csvfile)
            outfile.write("[" + '\n')

            # Loop over each row in the file and create an NGSI-LD entity
            total_lines = sum(1 for row in reader)
            csvfile.seek(0)
            next(reader) # skip header

            current_line = 1
            for row in reader:
                entity_id = uuid.uuid4()
                entity = {
                    "id": f"urn:ngsi-ld:GtfsStop:Ioannina:SmartCitiesdomain:SmartCityBus:{row['stop_id']}",
                    "type": "GtfsStop",
                    
                    "@context": [
                        context,
                        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
                    ],
                    "name": {"type": "Property", "value": row["stop_name"]},
                    'location': {
                        'type': 'GeoProperty',
                        'value': {
                            'type': 'Point',
                            'coordinates': [
                                float(row['stop_lon']),
                                float(row['stop_lat'])
                            ]
                        }
                    }
                }

                if row.get("stop_code"):
                    entity["code"] = {"type": "Property", "value": row["stop_code"]}
                if row.get("stop_desc"):
                    entity["description"] = {"type": "Property", "value": row["stop_desc"]}
                if row.get("zone_id"):
                    entity["zoneId"] = {"type": "Property", "value": row["zone_id"]}
                if row.get("stop_url"):
                    entity["page"] = {"type": "Property", "value": row["stop_url"]}
                if row.get("location_type"):
                    entity["locationType"] = {"type": "Property", "value": row["location_type"]}
                if row.get("parent_station"):
                    entity["parentStation"] = {"type": "Property", "value": row["parent_station"]}
                if row.get("stop_timezone"):
                    entity["timezone"] = {"type": "Property", "value": row["stop_timezone"]}
                if row.get("wheelchair_boarding"):
                    entity["wheelChairAccessible"] = {"type": "Property", "value": row["wheelchair_boarding"]}
                
                outfile.write(json.dumps(entity, indent=2, ensure_ascii=False) + '\n')

        
                percentage_done = current_line / total_lines * 100
                if percentage_done!=100:
                    outfile.write("," + '\n')
                    
                print(f"Processed {current_line} out of {total_lines} lines ({percentage_done:.2f}%)")

                current_line += 1
            outfile.write("]" + '\n')
        print("Stops done!")

    print("------------------------------------------------------------------------------------------------------------------------------------")

    if(options_dict["Trips"]==False and options_dict["All (default)"]==False):

        print("Skipping Trips...")
    else:
        print("Converting Trips..")     

        with open('trips.txt', 'r', encoding='utf-8-sig') as csvfile, open('GtfsTrips.ngsild', 'w') as outfile:
            reader = csv.DictReader(csvfile)
            outfile.write("[" + '\n')

            # Loop over each row in the file and create an NGSI-LD entity
            total_lines = sum(1 for row in reader)
            csvfile.seek(0)
            next(reader) # skip header

            current_line = 1

            for row in reader:
                entity_id = uuid.uuid4()
                entity = {
                    "id": f"urn:ngsi-ld:GtfsTrip:Ioannina:SmartCitiesdomain:SmartCityBus:{row['trip_id']}",
                    "type": "GtfsTrip",
                    
                    "@context": [
                        context,
                        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
                    ]
                }

                if row.get("trip_short_name"):
                    entity["name"] = {"type": "Property", "value": row["trip_short_name"]}

                if row.get("trip_headsign"):
                    entity["headSign"] = {"type": "Property", "value": row["trip_headsign"]}

                if row.get("route_id"):
                    entity["hasRoute"] = {"type": "Relationship", "object": f"urn:ngsi-ld:GtfsRoute:Ioannina:SmartCitiesdomain:SmartCityBus:{row['route_id']}"}

                if row.get("service_id"):
                    entity["hasService"] = {"type": "Relationship", "object": f"urn:ngsi-ld:GtfsCalendarRule:Ioannina:SmartCitiesdomain:SmartCityBus:{row['service_id']}"}
                
                if row.get("shape_id"):
                    entity["hasShape"] = {"type": "Relationship", "object": f"urn:ngsi-ld:GtfsShape:Ioannina:SmartCitiesdomain:SmartCityBus:{row['shape_id']}"}
                if row.get("block_id"):
                    entity["block"] = {"type": "Property", "value": row["block_id"]}

                if row.get("direction_id"):
                    entity["direction"] = {"type": "Property", "value": row["direction_id"]}

                if row.get("wheelchair_accessible"):
                    entity["wheelChairAccessible"] = {"type": "Property", "value": int(row["wheelchair_accessible"])}

                if row.get("bikes_allowed"):
                    entity["bikesAllowed"] = {"type": "Property", "value": int(row["bikes_allowed"])}

                if row.get("duty"):
                    entity["dataProvider"] = {"type": "Property", "value": row["duty"]}

                if row.get("duty_sequence_number"):
                    entity["dutySequenceNumber"] = {"type": "Property", "value": int(row["duty_sequence_number"])}

                if row.get("run_sequence_number"):
                    entity["runSequenceNumber"] = {"type": "Property", "value": int(row["run_sequence_number"])}
                
                outfile.write(json.dumps(entity, indent=2, ensure_ascii=False) + '\n')
                
                percentage_done = current_line / total_lines * 100
                if percentage_done!=100:
                    outfile.write("," + '\n')
                    
                print(f"Processed {current_line} out of {total_lines} lines ({percentage_done:.2f}%)") 
                current_line += 1
            outfile.write("]" + '\n')

apply_button = ttk.Button(root, text="Apply", command=begin_conversion)
apply_button.grid(column=1, row=2, padx=10, pady=10, sticky="w")

root.mainloop()
