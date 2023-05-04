import os, sys, datetime, shutil, subprocess


class integrity:
    def __init__(self,args=[]):
        '''
            input_dir -> str:
                    Input directory for integrity analysis
            
            report_path -> str:
                    Integrity report path

            mode -> str: c or v
                    c = create: To generate integrity report
                    v = verify: To verify integrity report

            options -> dict:
                    Other flags and options for execution
                    - force -> str: Overwrite any existing reports

            other intermittent variables used:
                    - resp: response of user inputs or subprocess outputs
        '''

        # defining object variables
        self.input_dir: str = ''
        self.report_path: str = ''
        self.mode: str = ''
        self.options: dict = {
            'force': False
        }

        # execution
        self.parse_inputs(args)
        self.exec()
    
    # Functions for inputs ----------------------------------
    def parse_inputs(self,args):
        if args:
            self.get_argument_inputs(args)
            self.stats()
        else:
            self.intro()
            self.get_manual_inputs()

    
    def get_argument_inputs(self,args):
        '''
            flags:
                    -i: set input folder
                    -r: set report path
                    -f: set force flag
        '''

        self.input_dir = args[args.index('-i')+1]

        if 'c' in args: self.mode = 'c'
        elif 'v' in args: self.mode = 'v'

        if '-r' in args:
            resp = args[args.index('-r')+1]
            if os.path.isdir(resp): resp += '\\integrity_report.txt'
        else: resp = self.input_dir + '\\integrity_report.txt'
        self.report_path = resp
        
        if '-f' in args: self.options['force'] = True


    def get_manual_inputs(self):
        self.input_dir = input('\nEnter input folder: ')

        resp = int(input('\nSelect operation: 1. Create, 2. Verify\nSelection: '))
        self.mode = ['c','v'][resp-1]

        ops = [
            'Enter path to save report file (leave blank if you want to save it in the input folder)',
            'Enter path of report file (leave blank if the report is present in the input folder)'
        ]
        resp = input(f'\n{ops[resp-1]}\nReport path: ')
        if not resp: resp = self.input_dir
        if os.path.isdir(resp): resp += '\\integrity_report.txt'
        self.report_path = resp


    # Execution --------------------------------------------
    def exec(self):
        if self.mode == 'c': self.create_report()
        elif self.mode == 'v': self.verify_report()

    
    def create_report(self):
        # checking if report file already exists
        if os.path.isfile(self.report_path) and not self.options['force']:
            resp = input('\nReport already exists. Do you want to overwrite? (y/n): ').lower()
            if resp == 'y': pass
            elif resp == 'n': exit()
            else: raise ValueError(f'Invalid response: "{resp}" ')

        # priting execution time
        timestamp = datetime.datetime.now()
        timestamp_formatted = timestamp.strftime("%B %d, %Y %I:%M:%S %p")
        print(f'\n* {timestamp_formatted}\n')
        
        # execution: getting current tree structure
        print('• Running tree command : running',end='\r',flush=True)
        cmd = f'tree /f /a "{self.input_dir}"'
        resp = subprocess.run(cmd, shell=True, capture_output=True)
        data = resp.stdout.decode('utf-8').split('\r\n')
        clear_line()
        print('• Running tree command : done',end='\n',flush=True)

        # execution: attaching timestamp
        print('• Attaching timestamp  : running',end='\r',flush=True)
        data[1] += f' | {timestamp_formatted}'
        clear_line()
        print('• Attaching timestamp  : done',end='\n',flush=True)

        # execution: saving report file
        print('• Saving report file   : running',end='\r',flush=True)
        with open(self.report_path, 'w') as file:
            file.write('\n'.join(data))
        clear_line()
        print('• Saving report file   : done',end='\n',flush=True)


    def verify_report(self):
        # excution: reading report data
        print('\n• Reading report data : running',end='\r',flush=True)
        with open(self.report_path,'r') as file:
            data = file.read()
        report_data = data.split('\n')
        clear_line()
        print('• Reading report data   : done',end='\n',flush=True)

        # execution: getting current tree structure
        print('• Running tree command  : running',end='\r',flush=True)
        cmd = f'tree /f /a "{self.input_dir}"'
        resp = subprocess.run(cmd, shell=True, capture_output=True)
        current_data = resp.stdout.decode('utf-8').split('\r\n')
        clear_line()
        print('• Running tree command  : done',end='\n',flush=True)

        # execution: remove if integrity file entry exists
        val = '|   integrity_report.txt'
        print('• Removing report entry : running',end='\r',flush=True)
        if val in report_data: report_data.remove(val)
        if val in current_data: current_data.remove(val)
        clear_line()
        print('• Removing report entry : done',end='\n',flush=True)        

        # execution: Integrity check
        print('\nIntegrity check:')
        timestamp = report_data[1].split(' | ')[-1]
        print(f'Report generated on     : {timestamp}')
        if report_data[3:] == current_data[3:]: print('Integrity test          : Passed',end='\n',flush=True)
        else: print('Integrity test          : Failed',end='\n',flush=True)
        pass

        

    # Object representation --------------------------------
    def __repr__(self):
        repr = f'Integrity(\n\tinput_dir: "{self.input_dir}"\n\toperation: {["create","verify"][["c","v"].index(self.mode)]}\n\treport_path: "{self.report_path}"\n\toptions: {self.options}\n)'
        return repr
    

    def intro(self):
        os.system('title Folder Integrity')
        term_width = shutil.get_terminal_size()[0]
        title = f'{"-"*5} FOLDER INTEGRITY {"-"*5}'.center(term_width)
        print(title)

    
    def stats(self):
        self.intro()
        print(f'\nInput folder: "{self.input_dir}"')
        print(f'Report path: "{self.report_path}"')
        print(f'Operation: {["CREATE","VERIFY"][["c","v"].index(self.mode)]}', end='')
        if self.options['force']: print(f' -FORCE')
        else: print()


def clear_line():
    width = shutil.get_terminal_size()[0]
    print(" "*width,end='\r')


if __name__ == '__main__':
    os.system('cls')
    args = sys.argv[1:]
    obj = integrity(args)
