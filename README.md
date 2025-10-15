# GTFS to NGSI-LD Converter
This Python script converts a GTFS (General Transit Feed Specification) dataset into NGSI-LD (Next Generation Service Interface - Linked Data) format. The NGSI-LD entities are written to .ngsild files, which can then be imported into an NGSI-LD compliant context broker.

## Features
Convert GTFS data into NGSI-LD entities
Select which GTFS components to convert (e.g., routes, shapes, stop times)
Outputs NGSI-LD entities in .ngsild files

## Usage
To use the GTFS to NGSI-LD Converter, you will need to have Python 3.7 or higher installed on your computer, along with the required libraries: csv, json, datetime, uuid, tkinter, ttk, and ttkthemes.

To run the converter, open the terminal or command prompt and navigate to the directory where the script is located. Then, type the following command and press enter:

```
python3 converter.py

```
This will launch the GTFS to NGSI-LD converter window, where you can select which GTFS components to convert. The available options are:

- All (default)
- Agency
- CalendarRule
- Routes
- Shapes
- Stops
- Trips
- StopTimes

To select an option, click on the drop-down menu and choose one of the options. You can only select one option at a time.

Once you have selected an option, click the "Convert" button to begin the conversion process. The converter will create NGSI-LD entities for the selected GTFS component and write them to a separate .ngsild file.

If you want to close the application, click the "Close" button.

## Code
The script processes the following GTFS components:

- Agency
- CalendarRule
- Routes
- Shapes
- Stops
- Trips
- StopTimes

For each component, the script:

Checks if the component should be processed based on the options_dict configuration.
Opens the file, parses its information, and according to the fields that exist, create the appropriate ngsi-ld entities.
The entities are then stored in a separate file per type.

## Requirements
To use this script, you will need Python 3.7 or higher installed on your computer. Additionally, the script uses the following libraries, which can be installed via pip:

- datetime
- uuid
- ttkthemes

To install the required libraries, run the following command in your terminal or command prompt:

```
pip install datetime uuid ttkthemes
```


## Disclaimer
While we have made every effort to ensure that the GTFS to NGSI-LD converter is accurate and reliable, there may be instances where errors or inaccuracies occur. We cannot be held responsible for any loss or damage that may arise from the use of this tool, and we recommend that you thoroughly test the converter on a small dataset before using it to convert a larger GTFS dataset.

This GTFS → NGSI-LD converter is no longer maintained and development has been abandoned. The tool remains experimental and only converts a limited subset of GTFS attributes to NGSI-LD.
If you need additional functionality, please fork the repository and maintain your own version.
