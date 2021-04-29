#! /usr/bin/env python3

import json
from argparse import ArgumentParser
import random

# python noc_hetero_vc_gen.py -f test.json -m json

VC_COUNT = 'vc_count'
BUFFER_DEPTH = 'buffer_depth'
NOC_X = 'noc_x'
NOC_Y = 'noc_y'
NUM_ROUTERS = 'num_routers'
AVAILABLE_PORTS = 'available_ports'

MODE_GEN_MAP = 'json'
MODE_GEN_VHDL = 'vhdl'

# 0 => Local
# 1 => North
# 2 => East
# 3 => South
# 4 => West
LOCAL = 0
NORTH = 1
EAST  = 2
SOUTH = 3
WEST  = 4
PORT_STRING = ["Local", "North", "East", "South", "West"]
JSON_PORT_STRING = ["0", "1", "2", "3", "4"]
diff_vc_counts = [4, 5, 6, 7, 8, 9, 10, 11]

# custom_vcs schema
# {
#   "router00": [5, 6, 7],
#   "router01": [4, 5, 6, 7],
#   ...
# }

def get_num_of_vc(x_router, y_router, port, vc_map):
    router_string = 'router_' + str(x_router) + str(y_router)
    return vc_map[router_string][port][VC_COUNT]

def get_buffer_depth(x_router, y_router, port, vc_map):
    router_string = 'router_' + str(x_router) + str(y_router)
    return vc_map[router_string][port][BUFFER_DEPTH]

def get_array_of_vcs(vc_map):
    arr = []
    for x_router in range(vc_map[NOC_X]):
        router_arr = []
        for y_router in range(vc_map[NOC_Y]):
            router_string = 'router_' + str(x_router) + str(y_router)
            router = vc_map[router_string]
            port_arr = []
            for port in router[AVAILABLE_PORTS]:
                port_arr.append(router[port][VC_COUNT])
            router_arr.append(port_arr)
        arr.append(router_arr)
    return arr

def get_array_of_all_vcs(vc_map):
    arr = []
    for x_router in range(vc_map[NOC_X]):
        for y_router in range(vc_map[NOC_Y]):
            router_string = 'router_' + str(x_router) + str(y_router)
            router = vc_map[router_string]
            for port in router[AVAILABLE_PORTS]:
                arr.append(router[port][VC_COUNT])
    return arr

def get_array_of_all_buffer_depths(vc_map):
    arr = []
    for x_router in range(vc_map[NOC_X]):
        for y_router in range(vc_map[NOC_Y]):
            router_string = 'router_' + str(x_router) + str(y_router)
            router = vc_map[router_string]
            for port in router[AVAILABLE_PORTS]:
                arr.append(router[port][BUFFER_DEPTH])
    return arr

def get_router(x_router, y_router, vc_map):
    router_string = 'router_' + str(x_router) + str(y_router)
    return vc_map[router_string]

def get_max_buffer_depth(vc_map):
    return max(get_array_of_all_buffer_depths(vc_map))

def get_max_vc(vc_map):
    return max(get_array_of_all_vcs(vc_map))

def get_sum_vc(vc_map):
    return sum(get_array_of_all_vcs(vc_map))
                
def get_array_of_vc_depths(vc_map):
    arr = []
    for x_router in range(vc_map[NOC_X]):
        router_arr = []
        for y_router in range(vc_map[NOC_Y]):
            router_string = 'router_' + str(x_router) + str(y_router)
            router = vc_map[router_string]
            port_arr = []
            for port in router[AVAILABLE_PORTS]:
                port_arr.append(router[port][BUFFER_DEPTH])
            router_arr.append(port_arr)
        arr.append(router_arr)
    return arr

def sum_of_vcs_per_port(x, y, vc_map):
    summing = 0
    for x_router in range(vc_map[NOC_X]):
        for y_router in range(vc_map[NOC_Y]):
            router_string = 'router_' + str(x_router) + str(y_router)
            router = vc_map[router_string]
            for port in router[AVAILABLE_PORTS]:
                summing = summing + router[port][VC_COUNT]
    return summing

def sum_of_vcs_depth_per_port(x, y, vc_map):
    summing = 0
    for x_router in range(x):
        for y_router in range(y):
            router_string = 'router_' + str(x_router) + str(y_router)
            router = vc_map[router_string]
            for port in router[AVAILABLE_PORTS]:
                summing = summing + router[port][BUFFER_DEPTH]
    return summing

def json_vc_gen(json_file='router_vc_map.json', x=8, y=8, max_ports=5, custom_vcs={}):
    json_file = open(json_file, 'w')
    vc_map = {}
    num_routers = x * y
    
    vc_map[NOC_X] = x
    vc_map[NOC_Y] = y
    vc_map[NUM_ROUTERS] = num_routers

    for x_router in range(x):
        for y_router in range(y):
            router_string = 'router_' + str(x_router) + str(y_router)
            vc_map[router_string] = {}

            possible_ports = [0, 1, 2, 3, 4]
            if x_router == x - 1:
                possible_ports.remove(EAST)
            if x_router == 0:
                possible_ports.remove(WEST)
            if y_router == y - 1:
                possible_ports.remove(NORTH)
            if y_router == 0:
                possible_ports.remove(SOUTH)

            port_string_arr = []
            for i in possible_ports:
                port_string_arr.append(str(i))
            
            vc_map[router_string]["available_ports"] = port_string_arr
            
            for port in possible_ports:
                vc_map[router_string][port] = {}
                vc_map[router_string][port]["name"] = PORT_STRING[port]
                vc_map[router_string][port][VC_COUNT] = 4 # random.randint(1,10)
                vc_map[router_string][port][BUFFER_DEPTH] = 4 # random.randint(1,10)
    
    json_file.write(json.dumps(vc_map, indent=4))
    json_file.close()

def vhdl_vc_gen(json_file='router_vc_map.json'):
    # Parsing vc maps
    json_file = open(json_file, 'r')
    vc_map = json.loads(json_file.read())

    # for router in range(num_routers):
    #     router_string = 'router' + str(router)
    #     print(router_string)
    #     for direction in router_directions:
    #         vc_count = vc_map[router_string][direction][VC_COUNT]
    #         buffer_depth = vc_map[router_string][direction][BUFFER_DEPTH]
    #         print('  direction [' + str(direction) + ']:')
    #         print('    vc_count: ' + str(vc_count))
    #         print('    buffer_depth: ' + str(buffer_depth))
    #     print('\n')

    json_file.close()

    return vc_map

def main():
    p = ArgumentParser()
    p.add_argument('-m', '--mode', required=True, type=str  , help="[REQUIRED] Script Modes: {\n\"json\" for create a vc json map}  {\"vhdl\" for generating VHDL with vc map}")
    p.add_argument('-f', '--json_file', default='router_vc_map.json', type=str, help="JSON File with Router VC Maps.")
    p.add_argument('-x', '--num_x_routers', default=8, type=int, help="Number of Routers for Crossbar on X Axis (Horizontal)")
    p.add_argument('-y', '--num_y_routers', default=8, type=int, help="Number of Routers for Crossbar on Y Axis (Vertical)")
    p.add_argument('-p', '--max_ports', default=5, type=int, help="Maximum number of ports per router.")
    args = p.parse_args()

    if args.mode == MODE_GEN_MAP:
        json_vc_gen(json_file=args.json_file, x=args.num_x_routers, y=args.num_y_routers, max_ports=args.max_ports)
    elif args.mode == MODE_GEN_VHDL:
        vhdl_vc_gen(json_file=args.json_file)
    else:
        print('No correct mode was selected.')
    

if __name__ == '__main__':
    main()