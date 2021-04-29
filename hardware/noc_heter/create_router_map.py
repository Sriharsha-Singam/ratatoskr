#! /usr/bin/env python3

from argparse import ArgumentParser

map = {
    'routers': {}
}

file_size = 0

def pull_file(file):
    global file_size
    return open(file).read()

def next_line_index(read_file, index):
    line_end = "\n"
    local_index = index

    while local_index < len(read_file):
        text_part = read_file[local_index:(local_index+len(line_end))]
        if text_part == line_end:
            return local_index
        local_index = local_index + 1

    return -1


    

def create_map(read_file, num_of_routers):

    router_map = {}
    router_map['local'] = {}
    router_map['routers'] = {}


    router_index = read_file.find("begin\n")
    router_index = router_index + len("begin\n")

    for i in range(num_of_routers):
        next_router_index = next_line_index(read_file, router_index)
        if next_router_index == 0:
            print('ERROR: Wrong number of routers found.')
        router_index = next_router_index

def main():
    p = ArgumentParser()
    p.add_argument('-f', '--file', required=True, type=str, help="full_noc.vhd file")
    p.add_argument('-n', '--num_of_routers', required=True, type=int, help="number of routers")
    args = p.parse_args()
    
    read_file = pull_file(args.file)

if __name__ == '__main__':
    main()