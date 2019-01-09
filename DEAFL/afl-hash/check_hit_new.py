#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' check hash conflict '''

import tempfile
from multiprocessing import Process
import os
import traceback
import sys
from utils import run_command_noret

MAP_SIZE_INDEX = 16

TRACE_EDGES = set()

class DynamicAnalyzer(object):

    def __init__(self):
        """ init """
        self._fifo_name = ''
        self._tmpdir = ''

    def parse_trace(self):
        """ read from fifo and parse into dictionary """
        current = ''              # current basic block being parsed
        previous = '0'             # previous basic block beding parsed
        edge_count = 0
        uniq_count = 0
        with open(self._fifo_name, 'r') as fifo:
            for line in fifo:
                if line[6] == '4':
                    continue
                # process traceed tbs
                current = line.split(':')[0]

                parse_edge = (previous, current)
                edge_count += 1
                if not parse_edge in TRACE_EDGES:
                    TRACE_EDGES.add(parse_edge)
                    uniq_count += 1
                previous = current


    def mkfifo(self, fifo=None):
        """ create FIFO """
        if fifo is None:
            fifo = 'fifo'
        self._tmpdir = tempfile.mkdtemp()
        self._fifo_name = os.path.join(self._tmpdir, fifo)
        # print self._fifo_name
        try:
            os.mkfifo(self._fifo_name)
        except OSError as excp:
            traceback.print_exc()
            os.rmdir(self._tmpdir)
            print "Failed to create FIFO"
            print getattr(excp, 'message', repr(excp))
            raise excp


    def analyze_dynamic(self, test_input):
        """ analyze the dynamic translation block coverage with qemu """
        # Execute binary with qemu user mode while taking care of libraries
        # collect dynamic translation block execution information

        # 1. create a named pipe for qemu to write to
        self.mkfifo()

        # 2. build command and launch QEMU
        # cmd = self.build_qemu_cmd(test_input)
        cmdfile = open('command_file', 'r')
        run_cmd = cmdfile.readline()

        if '|' in run_cmd:
            cmd = run_cmd.format(test_input, self._fifo_name)
        else:
            cmd = run_cmd.format(self._fifo_name, test_input)

        print cmd
        process = Process(target=run_command_noret, args=[cmd, 120])
        process.start()

        # 3. read from fifo after QEMU finished executing
        try:
            self.parse_trace()
        except Exception as e:
            traceback.print_exc()
            print 'error when parsing qemu trace'
            print getattr(e, 'message', repr(e))
            raise e
        finally:
            os.remove(self._fifo_name)
            os.rmdir(self._tmpdir)


edge_map = set()
full_map = dict()
actual_map = dict()

queue_dir = sys.argv[1]
#print queue_dir

start_address = sys.argv[3]

# load the queue data

if queue_dir == 'FILE':
    edge_map = set(tuple(line.strip().split(',')) for line in open('edge_file','r'))
    TRACE_EDGES.update(edge_map)
else:
    for root, dirs, files in os.walk(queue_dir):
        for f in files:
            full_path= '{}/{}'.format(root, f)
            analyzer = DynamicAnalyzer()
            analyzer.analyze_dynamic(full_path)
            edge_map.update(TRACE_EDGES)
        # no ".state" dir
        break
    # save the edges into file
    edge_file = open('edge_file', 'w')
    for edge in edge_map:
        edge_file.write(edge[0]+','+edge[1]+'\n')



print len(edge_map)



# analyse the target testcase trace
test_case_dir = sys.argv[2]
for root, dirs, files in os.walk(test_case_dir):
    for f in files:
        full_path= '{}/{}'.format(root, f)
        analyzer = DynamicAnalyzer()
        analyzer.analyze_dynamic(full_path)


# Step1: is there any new edge?
print "> Step1: is there any new edge?"
new_edges = TRACE_EDGES - edge_map
num_new_edges = len(new_edges)

if num_new_edges == 0:
    print "no new edges"
print "Yes! {} new edges found.".format(num_new_edges)
for edge in sorted(new_edges):
    print edge
print
# Step2: is the bitmap value causing conflicts?
print "> Step2: is the bitmap value causing conflicts?"

same_hit = 1

for edge in edge_map:
    prev = int(edge[0], 16)
    cur = int(edge[1], 16)
    value = ((cur >> 4)^(cur << 8)) ^ (((prev >> 4)^(prev << 8)) >> 1)
    if value in full_map:
        full_map[value].append(edge)
    else:
        full_map[value] = [edge,]

for edge in new_edges:
    print edge
    print '......',
    prev = int(edge[0], 16)
    cur = int(edge[1], 16)
    value = ((cur >> 4)^(cur << 8)) ^ (((prev >> 4)^(prev << 8)) >> 1)
    print hex(value)
    if value in full_map:
        print "Confilct found: ", hex(value), full_map[value]
    else:
        print "No conflict"
        same_hit = 0
    print "---------------------------------------------------------------------------------------------------------------"
if same_hit:
    print "All the new edges caused location conflicts in bitmap, it is hard to sync this testcase."
else:
    print "Looks good, continue..."

print

# Step3: is the bitmap value causing conflicts?
print "> Step3: is the actual bitmap causing conflicts? [MAP_SIZE: 2**{}]".format(MAP_SIZE_INDEX)

MAP_SIZE = 2**MAP_SIZE_INDEX
should_in = 0
for edge in edge_map:
    prev = int(edge[0], 16)
    cur = int(edge[1], 16)
    value = ((cur >> 4)^(cur << 8))
    value &= (MAP_SIZE - 1)
    value ^= ((((prev >> 4)^(prev << 8)) & (MAP_SIZE - 1)) >> 1)
    if value in actual_map:
        actual_map[value].append(edge)
    else:
        actual_map[value] = [edge,]

start_fill = int(start_address, 16)
my_edges = {}
my_edge_end = []
my_edge_end.append(start_fill)
for edge in sorted(new_edges):
    print edge
    print '......',
    prev = int(edge[0], 16)
    cur = int(edge[1], 16)
    value = ((cur >> 4)^(cur << 8))
    value &= (MAP_SIZE - 1)
    value ^= ((((prev >> 4)^(prev << 8)) & (MAP_SIZE - 1)) >> 1)
    print hex(value)

    edge_found = 0
    fill_prev = my_edge_end[-1]
    fill_cur_start = my_edge_end[0] + 10
    print hex(fill_prev), hex(fill_cur_start)
    while edge_found != 1:
        fill_value = ((fill_cur_start >> 4)^(fill_cur_start << 8))
        fill_value &= (MAP_SIZE - 1)
        fill_value ^= ((((fill_prev >> 4)^(fill_prev << 8)) & (MAP_SIZE - 1)) >> 1)

        if fill_value == value:
            print "Recommend edge: [{}, {}], index value is {}".format(hex(fill_prev), hex(fill_cur_start), hex(fill_value))
            my_edges[fill_prev] = fill_cur_start
            my_edge_end.append(fill_cur_start)
            edge_found = 1
            break
        fill_cur_start += 1



    if value in actual_map:
        print "Confilct found in location {}: existing edges:{}".format(hex(value), actual_map[value])
    else:
        print "No conflict"
        should_in = 1
    print "---------------------------------------------------------------------------------------------------------------"

if should_in:
    print "The testcase looks very interesting!"
else:
    print "All the new edges caused conflicts, please try changing the `MAP_SIZE` in afl"
