# Python-BticinoThermostatInflux

A remake of (this Golang version)[https://github.com/Knocks83/Go-BticinoThermostatInflux], just because.

---
## Requirements
- InfluxDB 1.8
- Legrand API credentials
    - Create your API credentials at <https://portal.developer.legrand.com/>products. The default API (Starter Kit, which is free) has 500 API calls/day. It could take a few days for your API to get approved.
        - Just a suggestion: if you don't have a website to set for the redirect, you can use something like <https://httpbin.org/get>, so that when you do the first login it'll redirect you to a page with the code instead of copying it from the address bar.
---
## Configuration
- Add the required data in the config/config.go file
    - InfluxDB Section (**SERVER VERSION: 1.8**)
        - InfluxHost -> The address of the InfluxDB server
        - InfluxPort -> The prot used by InfluxDB (default: 8086)
        - InfluxDatabase -> The database where you want to write the data
        - InfluxMeasurementName -> I don't know how else I should explain it, I usually use `environment`.
    - Thermostat Section
        - ClientID -> The Client ID of your API.
        - ClientSecret -> The Client Secret of your API.
        - Redirect -> The website you specified when you created the API credentials (**IT CANNOT BE DIFFERENT, OTHERWISE IT'LL GIVE YOU AN ERROR**).
        - PlantID -> The ID of the location where your Thermostat is.
        - ModuleID -> The ID of the Thermostat.
    - Various Section
        - CalculateAbsolutePath -> Whether the software should make the file names absolute (eg. from refresh.txt to /opt/Thermostat/refresh.txt). Leave it on true if you're gonna run it from a different folder (or just to be sure), false if you want to use the file in the folder the terminal is in.
    - Advanced Section (EDIT ONLY IF YOU KNOW WHAT YOU'RE DOING)
        - RefreshFileName -> The name of the file that'll contain the refresh token.
        - RequestDelay -> The time between the requests, the default value is 182 so you'll make about 500 requests per day (with a little margin, just to be sure).

---
## Installation
- Install the pip dependencies
    - `pip3 install -r requirements.txt`
- Configure the software
- Run it
    - `python3 run.py`
___

That's all Folks!
For help just [ask me on Telegram](https://t.me/Knocks)!

This Source Code Form is subject to the terms of the Apache-v2.0 License. If a copy of the Apache-V2.0 License was not distributed with this
file, You can obtain one at <https://www.apache.org/licenses/LICENSE-2.0>.