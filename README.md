# LaunchHistory
Python script to read in rockets launch history

The script uses the launch database given by GCAT Jonathan C. McDowell (https://planet4589.org/space/gcat/)

Installation :
```
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

For the first use, you need to download the database :
```
python launcher.py --update
```

Help command :
```
python launcher.py -h
usage: launcher.py [-h] [--update] [--last LAST] [--list_launchers] [--list_operators] [--operator [OPERATOR ...]] [--mission [MISSION ...]] [--launcher [LAUNCHER ...]] [--year [YEAR ...]] [--fail]

Search in the launch history

options:
  -h, --help            show this help message and exit
  --update, -u          Update the launch list
  --last LAST           Print the n last results according the filters
  --list_launchers, -ll
                        Return the list of launchers
  --list_operators, -lo
                        Return the list of operators
  --operator [OPERATOR ...], -o [OPERATOR ...]
                        Filter on a list of operators
  --mission [MISSION ...], -m [MISSION ...]
                        Filter on a mission
  --launcher [LAUNCHER ...], -l [LAUNCHER ...]
                        Filter on a launcher
  --year [YEAR ...], -y [YEAR ...]
                        Filter on a list of years
  --fail, -f            Print all failures according to the operator and rocket chosen
  ```
  
  Example to see all launches for SpaceX and Arianespace in 2021 :
  ```
  python launcher.py -o SPX AE -y 2021
#Launch_Tag         Launch_Date      LV_Type          Flight_ID                 Flight                Mission Launch_Site Launch_Pad Agency Launch_Code      Category
  2021-001  2021-01-08 02:09:35     Falcon 9        105/B1060.4             Turksat 5A             Turksat 5A          CC       LC40    SPX          OS           Sat
  2021-005  2021-01-20 12:57:36     Falcon 9        106/B1051.8            Starlink-17      Starlink V1.0-L16         KSC      LC39A    SPX          OS           Sat
  2021-006  2021-01-24 14:52:48     Falcon 9        107/B1058.5          Transporter-1          Transporter-1          CC       LC40    SPX          OS           Sat
  2021-009  2021-02-04 06:14:23     Falcon 9        108/B1060.5            Starlink-19      Starlink V1.0-L18          CC       LC40    SPX          OS           Sat
  2021-012  2021-02-16 04:04:47     Falcon 9        109/B1059.6            Starlink-20      Starlink V1.0-L19          CC       LC40    SPX          OS           Sat
  2021-017  2021-03-04 08:24:00     Falcon 9        110/B1049.8            Starlink-21      Starlink V1.0-L17         KSC      LC39A    SPX          OS           Sat
  .........
  ```
