# papernest
 
This sample is the response to the **Backend developer technical test** given to me.

## Worksplace
- Visual Studio Code
- Python 3.10.9
- Virtual environment with FastApi / Uvicorn, Pandas, Pyproj

## Objectives
- Build an API to get the mobile network coverage of a given address.

### Restrictions
- Use the given CSV file listing places (Lambert93 geographic coordinates) with the providers and their network coverages;
- Use the https://adresse.data.gouv.fr/api API;
- Work on city-level precision.

## Input
- A string assumed as a postal address
- [TEST] Only the postcode 29242 (Ouessant) is in the database

## Output
- HTTP 200: A JSON object listing the providers and their network coverages;
- HTTP 400: When database file doesn't exist or the request is not valid;
- HTTP 404: When the network coverage data couldn't not be found in the database file.

## Installation
- Create a virtual environment with `python -m venv <env_name>`
- Activate this environment; the command is OS-specific.
- Install dependencies with following commands:
```
pip install fastapi
pip install "uvicorn[standard]"
pip install pandas
pip install pyproj
``` 
- Clone or download / extract the project within the virtual environment folder.
- Launch project on localhost with `uvicorn main:api`.
- Go to http://127.0.0.1:8000/docs to access the documentation and try the API from there.

## Process
1. [Offline] Create new CSV from the given CSV to add GPS coordinates (latitude and longitude) from Lambert93 coordinates with `python .\process.py -f coordinates`.
1. [Offline] Reduce data from the new CSV according to GPS coordinates by removing redundancy and produce database table  with `python .\process.py -f addresses`.
1. Get the official postal informations from the request. City-level precision implies that only the postcode is extracted.
1. Search postcode in new CSV.
1. Set output.