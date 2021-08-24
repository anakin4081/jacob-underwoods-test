### jacob Underwood
### built with python 3.9

from numpy.core.fromnumeric import sort
import requests, json, time
import pandas as pd
import numpy as np

def connect(FE):
    H = {
    'accept': 'application/json',
    }

    r = requests.get('https://eacp.energyaustralia.com.au/codingtest/api/v1/festivals', timeout = 5, headers=H)
    
    if(r.ok) == False:  ## checks if website is connected
        if Fail_Error == 5:   # failed connection
            print("program has failed 5 times try restarting")
            input("press any to keep trying")
            connect(Fail_Error = 0)
        else:
            print(f"failed to connect -Error Code {r.status_code}") ## gives status code
            print("retrying 3 seconds")
            time.sleep(3)
            connect(Fail_Error + 1)
    else:   #connected to site
        jsonfile = r.json()
        thread = json.dumps(jsonfile, indent=2) #formats the json text
        festivals = json.loads(r.text)
        if (len(thread)) <= 5:  #checks if the server throttled
            print("throttled retrying")
            time.sleep(3)
            connect(Fail_Error)
        else:   #data recieved
            print(f"connected")   #prints connected
            #print(thread) # only uncheck for dev purposes
            layout = pd.DataFrame(columns = ['event','band','recordLabel'])
            for festival in festivals:
                if 'name' in festival.keys():# checks if key is valid
                    if festival['name'] == '':
                        z = np.nan
                    else:
                        z = festival['name']
                else:
                    z = np.nan
                for band in festival['bands']:# checks if key is valid
                    y = band['name']
                    if 'recordLabel' in band.keys():
                        if band['recordLabel'] == '':
                            x = np.nan
                        else: 
                            x = band['recordLabel']
                    else:
                        x = np.nan
                    layout = layout.append({'event':z,'band':y,'recordLabel':x}, ignore_index=True)
                    #print(layout) #prints the full data structure
            for x in sort(layout['recordLabel'].dropna().unique()):
                print(x)
                for y in sort(layout[layout['recordLabel']==x]['band'].dropna().unique()):
                    print('\t{}'.format(y))
                    for z in sort(layout[layout['band']==y]['event'].dropna().unique()):
                        print('\t\t{}'.format(z))

Fail_Error = 0
connect(Fail_Error) #starts the script

ask=input("press any key to exit") 
if ask == "!":
    connect(Fail_Error) #sends a reconnect
else:
    pass