# WL-Monitor-Pi-Alexa
Alexa Skill for [WL-Monitor-Pi](https://github.com/mabe-at/WL-Monitor-Pi) (more infos can be found there)

Data Source: City of Vienna (Stadt Wien) - https://data.wien.gv.at

Quick and dirty python script for monitoring departures of lines at certain stations towards certain directions.

Have a look at this [youtube tutorial](https://www.youtube.com/watch?v=DFiCsMcipr4) about implementing this.

```
usage: wlmonitor_alexa.py [-h] [-p port] -k apikey rbl [rbl ...]

arguments:
  -k, --key=    API key
  rbl           RBL number

optional arguments:
  -p, --port=   Port to open (default 5001)
  -h, --help    show this help
  ```
  
