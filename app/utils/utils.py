import logging
import os
import re
import socket
import subprocess
import sys
import time
import unicodedata
from pathlib import Path
from shutil import which
from typing import Any, Dict

import click
from progressbar import ETA, Bar, Counter, ProgressBar, Timer
from stringcolor import bold
from tqdm import tqdm

from .config import BASE_PATH, ENV_MODE, LOGGING_LEVEL, PROJECT_NAME, VERSION
from .defaultLogBanner import log_runBanner

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


class Context:

    progress: Dict[int, ProgressBar] = {}

    def __init__(self):

        logging.log(logging.DEBUG, 'init context...')
        self.project = PROJECT_NAME
        self.base_path = BASE_PATH

        self.utils: Utils = None

        self.logging_verbose = None
        self.disable_split_project = None
        self.disable_split_host = None
        self.print_only_mode = None


pass_context = click.make_pass_decorator(Context, ensure=True)

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


class Utils:

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def __init__(self, ctx: Context):
        self.update(ctx, is_init=True)

    def update(self, ctx: Context, is_init: bold = False):
        self.ctx = ctx

        if not is_init and LOGGING_LEVEL == logging.getLevelName(logging.DEBUG):
            print()
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            logging.log(logging.DEBUG, f'LOGGING-LEVEL          : {bold(LOGGING_LEVEL)}')
            logging.log(logging.DEBUG, f'LOGGING-VERBOSITY      : {bold(self.ctx.logging_verbose)}')
            logging.log(logging.DEBUG, f'DISABLED SPLIT PROJECT : {bold(self.ctx.disable_split_project)}')
            logging.log(logging.DEBUG, f'DISABLED SPLIT HOST    : {bold(self.ctx.disable_split_host)}')
            logging.log(logging.DEBUG, f'PRINT ONLY MODE        : {bold(self.ctx.print_only_mode)}')
            logging.log(logging.DEBUG, f'PROJECT-PATH           : {bold(self.create_service_path("host_example"))}{bold("/")}')
            logging.log(logging.DEBUG, f'PROJECT-VERSION        : {bold(VERSION)}')
            logging.log(logging.DEBUG, f'ENV-MODE               : {bold(ENV_MODE)}')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print()

    # --------------------------------------------------------------------------
    #
    # path | folder | file - helper
    #
    # --------------------------------------------------------------------------

    def create_folder(self, path: str) -> None:
        Path(path).mkdir(parents=True, exist_ok=True, mode=0o700)

    def get_user_path(self) -> str:
        return str(Path.home())

    def create_service_folder(self, name: str, host: str = None) -> str:
        path = f'{self.create_service_path(host)}/{name}'
        self.create_folder(path)
        return path

    def create_service_path(self, host: str = None):
        if not self.ctx.disable_split_host:
            host = self.slugify(host)
            host = '' if host == None else f'/{host}'
        else:
            host = ''
        if not self.ctx.disable_split_project:
            project = '' if self.ctx.project == None else f'/{self.ctx.project}'
        else:
            project = ''

        if self.ctx.base_path[-1] == '/':
            self.ctx.base_path = self.ctx.base_path[0:-1]

        return f'{self.ctx.base_path}{project}{host}'

    # --------------------------------------------------------------------------
    #
    # command exec - helper
    #
    # --------------------------------------------------------------------------

    def run_command_endless(self, command_list=[]) -> None:
        sub_p: subprocess.Popen = None
        is_running = True
        try:
            index_to_check = 0
            index_to_check = 1 if command_list[index_to_check] == 'sudo' else index_to_check

            if self.is_tool(command_list[index_to_check]):
                sub_p = subprocess.Popen(command_list)
                while is_running:
                    time.sleep(600)
            else:
                logging.log(logging.ERROR, f'the command "{command_list[index_to_check]}", did not exist')
        # termination with Ctrl+C
        except KeyboardInterrupt:
            print('process killed!')
        except Exception as e:
            logging.log(logging.CRITICAL, e)
        is_running = False
        try:
            if sub_p != None:
                sub_p.terminate()
        except:
            pass
        try:
            if sub_p != None:
                while sub_p.poll() == None:
                    time.sleep(1)
        except:
            pass

    def run_command(self, command_list=[], input: str = None, inner_loop: bool = False) -> str:
        sub_p = None
        result = None

        if not self.ctx.print_only_mode:
            try:
                index_to_check = 0
                index_to_check = 1 if command_list[index_to_check] == 'sudo' else index_to_check

                if self.is_tool(command_list[index_to_check]):
                    if input == None:
                        sub_p: subprocess.CompletedProcess = subprocess.run(command_list, stdout=subprocess.PIPE)  # , shell=True
                        result = sub_p.stdout
                    else:
                        sub_p: subprocess.Popen = subprocess.Popen(command_list, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                        sub_p = sub_p.communicate(input.encode())[0]
                        result = sub_p
                else:
                    logging.log(logging.ERROR, f'the command "{command_list[index_to_check]}", did not exist')
            # termination with Ctrl+C
            except KeyboardInterrupt as k:
                if sub_p != None and type(sub_p) == subprocess.Popen:
                    sub_p.kill()
                logging.log(logging.DEBUG, f'process interupted! ({k})')
                if inner_loop:
                    raise KeyboardInterrupt
            except Exception as e:
                logging.log(logging.CRITICAL, e)
            if result != None:
                return result.decode()

    def is_tool(self, name: str) -> bool:
        '''
            Check whether `name` is on PATH and marked as executable.
        '''
        return which(name) is not None

    def run_command_output_loop(self, msg: str, cmds=[], output: bool = True) -> str:
        '''
            run command from list in a loop, and also optional pipe them into each other
            default exec function is "run_command" with different
        '''
        log_runBanner(msg)
        cmd_result = None
        try:
            for cmd in cmds:
                logging.log(logging.NOTICE, ' '.join(cmd))
                if output:
                    cmd_result = self.run_command(command_list=cmd, input=cmd_result, inner_loop=True)
                else:
                    cmd_result = self.run_command(command_list=cmd, inner_loop=True)
                if cmd_result != None and len(cmd_result) > 0:
                    logging.log(logging.DEBUG, cmd_result)
            return cmd_result
        except KeyboardInterrupt as k:
            logging.log(logging.DEBUG, f'process interupted! ({k})')
        except Exception as e:
            logging.log(logging.CRITICAL, e)
        return cmd_result

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def group(self, flat, size):
        '''
            group list a flat list into a matrix of "size"
        '''
        return [flat[i:i+size] for i in range(0, len(flat), size)]

    def normalize_caseless(self, text):
        '''
            lowercase a string, for any unicode
        '''
        return unicodedata.normalize('NFKD', text.casefold())

    def slugify(self, value, allow_unicode=False):
        '''
            https://github.com/django/django/blob/main/django/utils/text.py
        '''
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def in_sudo_mode(self):
        '''
            If the user doesn't run the program with super user privileges, don't allow them to continue.
        '''
        if not 'SUDO_UID' in os.environ.keys():
            logging.log(logging.ERROR, 'Try running this program with sudo.')
            sys.exit(1)

    def get_ip_address(self):
        st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            st.connect(('10.255.255.255', 1))
            IP = st.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            st.close()
        return IP

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def progress(self, id: int, value: int, description: str = "Processing", maxval: int = 100):
        try:

            # if self.ctx.progress.get(id) is None:
            #     self.ctx.progress[id] = tqdm(total=maxval, desc=description, colour="#000", leave=False)

            # if self.ctx.progress.get(id) is not None:
            #     bar = self.ctx.progress.get(id)
            #     bar.update(value)

            if self.ctx.progress.get(id) is None:
                self.ctx.progress[id] = ProgressBar(
                    widgets=[description, ' [', Timer(), '] ', Bar(marker='O'), ' [', Counter(format='%(value)02d/%(max_value)d'), ']', ' (', ETA(), ') '],
                    maxval=maxval).start()
            bar: ProgressBar = self.ctx.progress.get(id)
            bar.update(value=value)
            if value >= maxval:
                print()
        except Exception as e:
            logging.log(logging.CRITICAL, e)

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def define_option_list(self, options, default_options=[], options_append=False, default_split_by=';'):
        '''
            defines a list of option to use in a callable service
            to define how to create this list
            by:
                - create it from a default only
                - create it from params only
                - create it by combine default and params
        '''
        try:
            # add options from params
            if options != None and not options_append:
                options = options.split(default_split_by)
            # add options from params to existing options
            elif options != None and options_append:
                options = default_options + options.split(default_split_by)
            # use existing options
            else:
                options = default_options
            return options
        except Exception as e:
            logging.log(logging.CRITICAL, e)
        return []
