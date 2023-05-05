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
python gtfs_to_ngsi_ld.py

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

- csv
- json
- datetime
- uuid
- tkinter
- ttk
- ttkthemes

To install the required libraries, run the following command in your terminal or command prompt:

```
pip install csv json datetime uuid tkinter ttk ttkthemes
```

## Disclaimer
Please note that the GTFS to NGSI-LD converter is still in its early stages of development and is currently only capable of converting a limited subset of GTFS attributes to NGSI-LD format. We are actively working to expand the tool's capabilities and plan to include support for all GTFS attributes, as well as custom context and ID prefix selection in future releases.

While we have made every effort to ensure that the GTFS to NGSI-LD converter is accurate and reliable, there may be instances where errors or inaccuracies occur. We cannot be held responsible for any loss or damage that may arise from the use of this tool, and we recommend that you thoroughly test the converter on a small dataset before using it to convert a larger GTFS dataset.

If you encounter any issues or have any suggestions for how we can improve the GTFS to NGSI-LD converter, please don't hesitate to reach out to us through the contact channels listed above. We appreciate your feedback and will do our best to incorporate it into future releases of the tool.