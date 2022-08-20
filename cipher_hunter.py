import os
import argparse
import concurrent.futures
from datetime import datetime
import requests
import re

#----- Argument Handling -------
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

group_parser = parser.add_mutually_exclusive_group(required=True)                   # To Force Either cipher or Input File
group_parser.add_argument('-i','--cipher',help='Single Cipher to check')
group_parser.add_argument('-f','--file', help='Text file containing Ciphers separated by linefeed')

args = parser.parse_args()

#------------------- ****** ---------------------#

# ---------------- BANNER --------------------
BANNER = """
IDGAF-Cipher_Hunter
Coded by:
-----------
  ___        ____ ___      _ _____ 
 / _ \__  __/ ___/ _ \  __| |___ / 
| | | \ \/ / |  | | | |/ _` | |_ \ 
| |_| |>  <| |__| |_| | (_| |___) |
 \___//_/\_\\\\____\___/ \__,_|____/ 
                                   
   
---------- """

print(BANNER)
#------------------ CONSTANT Variables ----------

#----------------- Env Setup ------------------------
def check_cipher(cipher):
    URL = 'https://ciphersuite.info/api/cs/'
    ciphersuite = requests.get(URL+cipher)
    if ciphersuite.status_code == 200:
        return cipher+","+ciphersuite.json()[cipher]['security']
    else:
        return cipher+','+'ERROR'


# ----------------------- Operation for Single IP search --------------------------------------------
if args.cipher:
    print(check_cipher(args.cipher))


# --------------------------------  ******************  ----------------------------------------------

# ------------------------ Operations for File based inputs ------------------------------------------
elif args.file:
    #------ TODO -------
    # 1. Add input file validation/sanitisation

    try:                    # Try to get Input File
        in_file = open (args.file,'r')
        in_buffer = in_file.read()
        ciphers = re.sub("\(.*\)",'',in_buffer).split()
        # print (ciphers)
    except Exception:
        print (Exception)
        exit()

    # -- Check for Output directory, if not exist it creates --
    if os.path.exists('Outputs') == 0:
        os.makedirs('Outputs') 

    # -- Open a write mode file --
    cipher_out_file = open('Outputs/ciphersuite_'+ datetime.now().strftime("%d-%b-%Y_%H-%M-%S")+'.csv','w')
    cipher_out_file.write('Cipher Name,Security/Strength\n')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(check_cipher,ciphers)

        for strength in results:
            print(strength)
            cipher_out_file.write(strength+'\n')



