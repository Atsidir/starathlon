from dataclasses import dataclass
from typing import List
import random
from app import calc_path

activity_types = ['run', 'ride', 'walk']
ss_units = ['CO1', 'CO2', 'TA2', 'TA1', 'MS1', 'MS2']

persons = ['torit', 'bertam', 'geza', 'pisu',
           'julcsi', 'adorjan', 'peter', 'foldit',
           'judit', 'edithr', 'csecsia', 'csernia',
           'ledenyin', 'zempleib', 'feketea', 'szilvi',
           'seppno', 'seppakos', 'busb', 'pbarna', 'anjanb']


@dataclass
class SSEmployee:
    name: str
    unit: str


@dataclass
class Activity:
    employee: SSEmployee
    type: str
    distance: int


def gen_activities() -> List[Activity]:
    employees = [SSEmployee(person, random.choice(ss_units)) for person in persons]
    routes = []
    for employee in employees:
        for i in range(random.randint(1, 20)):
            act_type = random.choice(activity_types)
            length = random.randint(3, 10)
            if act_type == 'ride':
                length = length * 2.5
            routes.append(Activity(employee=employee,
                                   type=act_type,
                                   distance=length))
    return routes


#budapest_location = {'latitude': (47.4979), 'longitude': 19.0402}
#istambul_location = {'latitude': 40.4168, 'longitude': 3.7038}

#from geopy import distance

#print(distance.distance((47.4979, 19.0402), (40.4168, 3.7038)))

import pandas as pd


def gen_data(activity_filter=None):
    activities = gen_activities()
    units = {}
    for activity in activities:
        if activity.employee.unit not in units:
            units[activity.employee.unit] = {'name': activity.employee.unit,
                                             'distance': activity.distance,
                                             'color': "#%06x" % random.randint(0, 0xFFFFFF)}
        else:
            units[activity.employee.unit]['distance'] += activity.distance

    for unit_name in units:
        units[unit_name]['path'] = calc_path(units[unit_name]['distance'])
    import pprint
    pprint.pprint(units.values())
    data_tmp = pd.DataFrame(units.values())
    print(data_tmp.head(10))
    data_tmp.to_json('dummy_data.json', indent=4, orient='records')


gen_data()