#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' check hash conflict '''

import os
import time
import sys
import re
import cPickle
import tempfile
import argparse
import platform
import traceback
import subprocess
from threading import Timer
from collections import defaultdict
from multiprocessing import Process, active_children, Manager
from setproctitle import setproctitle         # pylint:disable=no-name-in-module


ENV_LIST = (
    'AFL_BENCH_JUST_ONE',
    'AFL_BENCH_UNTIL_CRASH',
    'AFL_DEFER_FORKSRV',
    'AFL_DUMB_FORKSRV',
    'AFL_EXIT_WHEN_DONE',
    'AFL_FAST_CAL',
    'AFL_HANG_TMOUT',
    'AFL_IMPORT_FIRST',
    'AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES',
    'AFL_LD_PRELOAD',
    'AFL_NO_AFFINITY',
    'AFL_NO_ARITH',
    'AFL_NO_CPU_RED',
    'AFL_NO_FORKSRV',
    'AFL_NO_UI',
    'AFL_PATH',
    'AFL_PERSISTENT',
    'AFL_POST_LIBRARY',
    'AFL_PRELOAD',
    'AFL_SHUFFLE_QUEUE',
    'AFL_SKIP_BIN_CHECK',
    'AFL_SKIP_CPUFREQ',
    'AFL_SKIP_CRASHES',
    'ASAN_OPTIONS',
    'LD_BIND_LAZY',
    'MSAN_OPTIONS',
    'PATH',
    '__AFL_DEFER_FORKSRV',
    'AFL_INST_LIBS',
    'AFL_INST_RATIO',
    '__AFL_SHM_ID'
)


CURPATH = os.path.dirname(os.path.realpath(__file__))

class Executor(object):
    ''' execute target binary with modified QEMU and get the TB trace '''

    def __init__(self, cmd, qemu, timeout=20):
        ''' init '''
        self._qemu = qemu
        self._cmd = cmd
        self._timeout = timeout


    def build_exec_cmd(self, fifo_name, testcase):
        ''' build target execution command for qemu usermode '''
        cmd_list = self._cmd[:]
        if '@@' in cmd_list:
            cmd_list[cmd_list.index('@@')] = testcase
        else:
            cmd_list.append('< {}'.format(testcase))
        cmd = ' '.join(cmd_list)

        template = '{QEMU} -d nochain,tb -D {TRACE} {CMD}'
        exec_cmd = template.format(QEMU=self._qemu,
                                   TRACE=fifo_name,
                                   CMD=cmd)

        return exec_cmd


    def run_command_noret(self, command, timeout=None):
        ''' execute command with subprocess and capture output '''
        with open(os.devnull, 'wb') as devnull:
            process = subprocess.Popen(command,
                                       stdout=devnull,
                                       stderr=devnull,
                                       shell=True)

            try:
                if timeout is not None:
                    timer = Timer(timeout, self.kill_process, args=(process, timeout))
                    timer.start()

                process.communicate()
            except subprocess.CalledProcessError:
                print 'process communicate error'
            finally:
                self.kill_process(process)
                if timeout is not None:
                    timer.cancel()


    @staticmethod
    def kill_process(process, timeout=None):
        ''' try to kill the subprocess.Popen() ed process '''
        pid = process.pid
        try:
            os.kill(pid, 9)
        except OSError:
            pass
        if timeout is not None:
            print '''process terminated with timeout ({})'''.format(timeout)


    @staticmethod
    def parse_trace(trace_file):
        ''' read from fifo and parse into dictionary '''
        current = 0              # current basic block being parsed
        previous = 0             # previous basic block beding parsed
        trace = set()
        with open(trace_file, 'r') as fifo:
            for line in fifo:
                current = int(line.split(':')[0], 16)

                parse_edge = (previous, current)
                trace.add(parse_edge)
                previous = current

        return trace


    @staticmethod
    def mkfifo(fifo=None):
        ''' create FIFO '''
        if fifo is None:
            fifo = 'fifo'
        tmpdir = tempfile.mkdtemp()
        fifo_name = os.path.join(tmpdir, fifo)
        try:
            os.mkfifo(fifo_name)
        except OSError as excp:
            print 'Failed to create FIFO'
            traceback.print_exc()
            os.rmdir(tmpdir)
            raise excp

        return (tmpdir, fifo_name)


    def execute(self, testcase):
        ''' analyze the dynamic translation block coverage with qemu '''
        # 1. create a named pipe for qemu to write to
        tmpdir, fifo_name = self.mkfifo()

        # 2. build command and launch QEMU
        cmd = self.build_exec_cmd(fifo_name, testcase)
        process = Process(target=self.run_command_noret, args=[cmd, self._timeout])
        process.start()

        # 3. read from fifo after QEMU finished executing
        try:
            return self.parse_trace(fifo_name)
        except (IOError, ValueError):
            print 'error when parsing qemu trace'
            traceback.print_exc()
        finally:
            active_children()
            os.remove(fifo_name)
            os.rmdir(tmpdir)


class BitmapBuilder(object):
    ''' check for hash conflict '''

    def __init__(self, executor, map_size_pow2=16):
        ''' init '''
        self._trace = dict()                          # edge coverage for each testcase
        self._edges = set()                           # overall edge coverage
        self._bitmap_indv = dict()                    # bitmap coverage for each testcase
        self._bitmap = dict()                         # overall bitmap coverage
        self._edge_idx = dict()
        self._map_size = 1 << map_size_pow2
        self._executor = executor


    @staticmethod
    def merge_dict_set(src, target):
        ''' merge two dictionaries, keeping original key values '''
        for key in set(src.keys()) | set(target.keys()):
            src[key] = src.get(key, set()) | target.get(key, set())


    def load_bitmap_from_log(self, directory):
        ''' load bitmap calculated by previous run(s) '''
        last_file = 0
        trace_file = os.path.join(directory, '.py_trace')
        try:
            print 'loading edge coverage for each testcase from LOG file'
            with open(trace_file) as trace:
                log_trace = cPickle.load(trace)

            self._trace = log_trace['trace']
            last_file = log_trace['last_file']
        except IOError:
            # open or read fail, ignore the logfile
            pass
        # return the last file
        return last_file


    def write_bitmap_to_log(self, directory, last_file):
        ''' load bitmap calculated by previous run(s) '''
        trace_file = os.path.join(directory, '.py_trace')

        log_trace = {'last_file': last_file, 'trace': self._trace}
        try:
            print 'write edge coverage for each testcase into LOG file'
            with open(trace_file, 'w') as trace:
                cPickle.dump(log_trace, trace, protocol=2)
        except IOError:
            # open or write fail, ignore the logfile
            traceback.print_exc()


    def build_bitmap_individual(self, testcase, trace):
        ''' build bitmap coverage for individual testcase '''
        self._bitmap_indv[testcase] = defaultdict(set)

        # calculate bitmap from trace
        for edge in trace:
            prev = edge[0]
            cur = edge[1]
            value = ((cur >> 4)^(cur << 8))
            value &= (self._map_size - 1)
            value ^= ((((prev >> 4)^(prev << 8)) & (self._map_size - 1)) >> 1)
            self._bitmap_indv[testcase][value].add(edge)


    @staticmethod
    def progress(count, total, current=None, inteval=50, rep='.'):
        ''' progress bar '''
        tick = count*inteval/total
        line = '''\x1b[2K\r[%-{}s] [{} / {}]'''.format(inteval, count, total)
        if current:
            line = line + ''' [{}]'''.format(current)
        sys.stderr.write(line % (rep*tick))


    def build_bitmap(self, target_files, recalculate=False):
        ''' build bitmap according to execution trace of the target testcases '''
        last_processed = 0
        if not recalculate:
            # load from previous calculated results
            target_dir = os.path.dirname(target_files[0])
            last_processed = self.load_bitmap_from_log(target_dir)

        print 'Collecting execution trace of each testcase'
        latest, trace = self.execute_target_files(target_files, last_processed)

        # update overall edge coverage, bitmap and reverse bitmap
        self.merge_dict_set(self._trace, dict(trace))

        print 'Calculating bitmap coverage for each testcase'
        count = 0
        for testcase, trace in self._trace.iteritems():
            count += 1
            self.progress(count, len(self._trace))

            self.build_bitmap_individual(testcase, trace)

        print ''
        print 'Calculating overall edge coverage'
        count = 0
        for testcase, trace in self._trace.iteritems():
            count += 1
            self.progress(count, len(self._trace))

            self._edges.update(trace)

        print ''
        print 'Calculating overall bitmap coverage'
        count = 0
        for bitmap in self._bitmap_indv.itervalues():
            count += 1
            self.progress(count, len(self._bitmap_indv))

            self.merge_dict_set(self._bitmap, bitmap)

        print ''
        print 'Calculating reverse bitmap dictionary (k:edge, v:bitmap_idx)'
        count = 0
        for idx, edges in self._bitmap.iteritems():
            for edge in edges:
                self._edge_idx[edge] = idx

            count += 1
            self.progress(count, len(self._bitmap))

        print ''

        target_dir = os.path.dirname(target_files[0])
        self.write_bitmap_to_log(target_dir, latest)


    def execute(self, testcase, _trace):
        ''' execute the target binary for bitmap coverage '''
        setproctitle('Executing [{}]'.format(os.path.basename(testcase)))
        trace = self._executor.execute(testcase)
        _trace[testcase] = trace


    def execute_target_files(self, target_files, last_processed):
        ''' evaluate testcases in target directory '''
        latest = last_processed
        trace = Manager().dict()
        n_files = len(target_files)

        for idx, testcase in enumerate(target_files):
            self.progress(idx+1, n_files, os.path.basename(testcase))

            ctime = os.stat(testcase).st_ctime
            if ctime < last_processed:
                continue

            if ctime > latest:
                latest = ctime

            # # single process
            # self.execute(testcase, trace)

            # multiprocessing
            Process(target=self.execute, args=[testcase, trace]).start()

            while len(active_children()) > 10:
                time.sleep(0.01)

        while len(active_children()) > 1:
            time.sleep(0.1)

        print ''
        return (latest, trace)


    @property
    def bitmap(self):
        ''' getter for bitmap '''
        return self._bitmap


    @property
    def trace(self):
        ''' getter for trace '''
        return self._trace


    @property
    def edges(self):
        ''' getter for edges '''
        return self._edges

    @property
    def bitmap_indv(self):
        ''' getter for individual bitmap dictionary '''
        return self._bitmap_indv

    @property
    def edge_idx(self):
        ''' return the dictionary of the bitmap index over each edge  '''
        return self._edge_idx


def check_conflict(afl, target):
    ''' check if edges in target bitmap are having hash conflict in afl bitmap '''
    conflict = dict()

    for testcase, edges in target.trace.iteritems():
        edges_diff = edges - afl.edges
        if not edges_diff:
            continue

        # bitmap_diff = set(target.bitmap_indv[testcase].keys()) - set(afl.bitmap.keys())

        # if len(bitmap_diff) != len(edges_diff):
        conflict[testcase] = edges_diff

    return conflict


def get_files(target, pattern):
    ''' get files from directory '''
    if os.path.isfile(target):
        return [target]

    items = sorted(os.listdir(target))
    return [os.path.join(target, item) for item in items if re.search(pattern, item)]


def get_file_arch(binary):
    ''' get the architecture of the input binary '''
    return platform.architecture(binary)


def build_cmd(afl_out, binary):
    ''' build execution command of target binary according to fuzzer_stats file '''
    # the command line in fuzzer_stats looks like:
    # command_line      : afl-fuzz -o /out -i /in -Q -S sec_001 -m none -- /binary/cb @@

    fuzzer_stats = os.path.join(afl_out, 'fuzzer_stats')
    with open(fuzzer_stats) as f_stats:
        lines = f_stats.readlines()
    command_line = lines[-1]

    # get the actual AFL launching command in list format
    afl_cmd = command_line.strip().split(':', 1)[1].strip().split()

    # parse AFL launching command and get binary execution command
    # the actual command starts when there is two consecutive element not start with '-'
    cmd_begin = 0
    opt = True
    for idx, element in enumerate(afl_cmd):
        if element == '--' or element.startswith(ENV_LIST):
            continue
        if not element.startswith('-'):
            if opt is False:
                cmd_begin = idx
                break
            else:
                opt = False
        else:
            opt = True

    if binary:
        afl_cmd[cmd_begin] = binary

    if not os.path.isfile(afl_cmd[cmd_begin]):
        print ('Target executable [ {} ] cannot be found, '
               'please specify the executable with "--binary" option and try again'
               .format(afl_cmd[cmd_begin]))
        exit(1)

    return afl_cmd[cmd_begin:]


def main(args):
    ''' main '''
    # 0. build command according to fuzzer_stats file
    cmd = build_cmd(args['afl_out'], args['binary'])

    if not args['qemu']:
        bin_arch = get_file_arch(cmd[0])[0]
        if bin_arch not in ['32bit', '64bit']:
            print 'unsupported file arch!, exiting now'
            exit(0)

        if bin_arch == '64bit':
            args['qemu'] = os.path.join(CURPATH, 'qemu-x86_64')
        if bin_arch == '32bit':
            args['qemu'] = os.path.join(CURPATH, 'qemu-i386')

    if not os.path.isfile(args['qemu']):
        print 'QEMU not found at given path [{}]'.format(args['qemu'])
        exit(0)

    # 1. create Executor
    executor = Executor(cmd, args['qemu'], args['timeout'])

    # 2. create Analyzer
    afl_analyzer = BitmapBuilder(executor, args['map_size_pow2'])
    target_analyzer = BitmapBuilder(executor, args['map_size_pow2'])

    # 3. generate bitmap of AFL queue, and save result to file
    print '-'*50
    print '> Analyzing afl output directory'

    afl_files = get_files(os.path.join(args['afl_out'], 'queue'), 'id.*')
    afl_analyzer.build_bitmap(afl_files, recalculate=args['recalculate'])

    # 4. analyze target and generate bitmap
    print ''
    print '-'*50
    print '> Analyze target {}\n'.format('file' if os.path.isfile(args['target']) else 'directory')

    target_files = get_files(args['target'], args['target_pattern'])
    target_analyzer.build_bitmap(target_files, recalculate=args['recalculate'])

    # 5. result
    print ''
    print '-'*50
    print '> bitmap with size of [{}]'.format(1<<args['map_size_pow2'])

    conflict = check_conflict(afl_analyzer, target_analyzer)

    for testcase, diff in conflict.iteritems():
        print 'testcase [{}] intoduced [{}] new edges'.format(os.path.basename(testcase), len(diff))
        for edge in diff:
            idx_edge = target_analyzer.edge_idx[edge]
            print ('    [0x{}, 0x{}] at index [{}] in target bitmap'
                   .format(edge[0], edge[1], idx_edge))

            conflict_edges = afl_analyzer.bitmap.get(idx_edge, [])
            for conflict_edge in conflict_edges:
                print '      ->    [0x{}, 0x{}]'.format(conflict_edge[0], conflict_edge[1])


def setup_argparse():
    ''' parse arguments '''
    parser = argparse.ArgumentParser()

    class IsDir(argparse.Action):                 #pylint: disable=R0903
        ''' check if target is a directory '''
        def __call__(self, parser, namespace, value, option_string=None):
            setattr(namespace, self.dest, value)
            if not os.path.isdir(value):
                parser.error("Directory [ {} ] does not exist".format(option_string))
                exit(1)

    class IsDirFile(argparse.Action):                 #pylint: disable=R0903
        ''' check if target is a file or directory '''
        def __call__(self, parser, namespace, value, option_string=None):
            setattr(namespace, self.dest, value)
            if not os.path.isdir(value) and not os.path.isfile(value):
                parser.error("File/Directory [ {} ] does not exist".format(option_string))
                exit(1)

    parser.add_argument('--afl_out', type=str, required=True, action=IsDir,
                        help='The output directory of AFL')

    parser.add_argument('--target', type=str, required=True, action=IsDirFile,
                        help='The target testcase or testcase directory to be checked')

    parser.add_argument('--target_pattern', type=str, default='^[^.].*$',
                        help='The target testcase pattern (in regex), default is "^[^.].*$"')

    parser.add_argument('--qemu', type=str, help='The qemu binary used for the analyzing')

    parser.add_argument('--timeout', type=int, default=20,
                        help='The timeout of qemu, default is 20s')

    parser.add_argument('--binary', type=str, default='',
                        help='The target executable binary of the test, '
                             'will try to retrieve from fuzzer_stats if not specified')

    parser.add_argument('--map_size_pow2', type=int, default=16,
                        help='the bitmap size of AFL under test(in power of 2), default is 16')

    parser.add_argument('--recalculate', action='store_true',
                        help='By default the script will save the result to file and only do the '
                             'increamental calculation during future invocation against the same '
                             'directory, add this if you want to ignore the previous result')

    args = parser.parse_args()
    kwargs = vars(args)

    return kwargs


if __name__ == '__main__':
    main(setup_argparse())
