import csv
import pandas as pd
import subprocess

## Program Variables
csvFile = "run_template.csv"
ip1 = ""
ip2 = ""
linux_host = ""
boot_delay = "120s"
pac_rec_path = r""
pac_conf_path = r""

## Setup Logging 
### create timestamped file for logging
logDir = "logs/"
timestr = time.strftime("%m-%d-%H%M")
logfile = open(f"logs/{timestr}_logs.txt", "a")
logfile.close()

logfiles = os.listdir(logDir)
logFile = str(logfiles[-1])
logging.basicConfig(
                    filename=f"{logDir}{logFile}",
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s"
                    )

## Program Variables
csvFile = "run_template.csv"
ip1 = "192.168.3.149"
ip2 = "192.168.3.42"
linux_host = "10.23.15.214"
boot_delay = "30s"
pac_rec_path = r"F:\\ADLP-REDRIX-DVT2_OCH-6761"
pac_conf_path = r"F:\\ADLP-REDRIX-DVT2_OCH-6761\\0 .Config\\Redrix-DVT_OCH-6761_sys_rail_config_r2.csv"
driverless= True

## Create Vars variable file
# Writes to vars file so that variable are accesable globally within program
print("Creating variable file...")
with open("vars.py", "w") as varsfile:
    varsfile.write(
    "linux_host = " +  "'" + linux_host + "'" + "\n" 
    + "ip1 = " +  "'" + ip1 +  "'" + "\n" 
    + "ip2 = " +  "'" + ip2 +  "'" + "\n"
    + "pac_rec_path = " + "'" + pac_rec_path + "'" + "\n"
    + "pac_conf_path = " + "'" + pac_conf_path + "'" + "\n"
    + "boot_delay = " +  "'" + boot_delay + "'" + "\n"
    )
    varsfile.close()
print("Done creating variable file...")
logging.debug("Variable file created") 

## Frontload stop script
stopScript = "bash -c; sshpass -p Qwerty123! ssh -o StrictHostKeyChecking=no oem@" + str(linux_host) +  str(' "') \
+ ". ~/Desktop/Automation_linux/copy_stopScript.sh " + str(ip1) +  str('"')
subprocess.run(stopScript, shell=True)
print("Stop script loaded onto DUT ", ip1)
logging.debug(f"Stop script loaded onto DUT:{ip1}") 

## Print the number of lines in the choosen CSV file
kpi_csv = pd.read_csv(csvFile)
csvLen = str(len(kpi_csv))
print("CSV file has " + csvLen + " lines")
logging.debug(f"CSV file has {csvLen} lines") 

## Reset count files to 1
kpis = []
kpis.append("nr-ido_num_new.txt")
kpis.append("lvp_num.txt")
kpis.append("plt_num.txt")
kpis.append("sOix_num.txt")
kpis.append("meets_num.txt")
kpis.append("run_counter_ido_soc.txt")
kpis.append("run_counter_lvp_soc.txt")
kpis.append("run_counter_plt.txt")


for i in range(len(kpis)):
    file = open(kpis[i], 'w')
    file.write(str(1))
    file.close()

## define kpis to run
## No Reboot PACS IDO
def nrIDO(runtype):
    if runType == "pac":
        print ("Starting NR_IDO running on host: ", linux_host)
        logging.debug(f"Starting NR_IDO running on host:{linux_host}")
        nrIDO = 'bash ./start_nr-ido.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
        subprocess.run(nrIDO, shell=True)
    elif runType == "soc":
        print("Starting NR_IDO SOCWATCH collection, running on host: ", linux_host)
        logging.debug(f"Starting NR_IDO SOCWATCH collection, running on host: {linux_host}")
        ido_soc = 'cmd.exe /C python.exe "run_pacs_NR-IDO_wSOC.py"'
        subprocess.run(ido_soc, shell=True)


## LVP PACS 
def lvp(runtype):
    if runType == "pac":
        print ("Starting LVP running on host: ", linux_host)
        logging.debug(f"Starting LVP running on host: {linux_host}")
        runLvp = 'bash ./start_LVP.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
        subprocess.run(runLvp, shell=True)
    elif runType == "soc":
        print("Starting LVP SOCWATCH collection running on host: ", linux_host)
        logging.debug(f"Starting LVP SOCWATCH collection running on host: {linux_host}")
        lvp_soc = 'bash ./soc_LVP.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
        subprocess.run(lvp_soc, shell=True)

## PLT PACS
def plt(runtype):
    if runType == "pac":
        print ("Starting PLT running on host: ", linux_host )
        logging.debug(f"Starting PLT running on host: {linux_host}" )
        runPlt = 'bash ./start_PLT.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
        subprocess.run(runPlt, shell=True)
    elif runType == "soc":
        print("Starting PLT SOCWATCH collection running on host: ", linux_host)
        logging.debug(f"Starting PLT SOCWATCH collection running on host: {linux_host}")
        plt_soc = 'bash ./soc_PLT.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
        subprocess.run(plt_soc, shell=True)

## Gmeet
def gmeet(runtype):
    if runType == "pac":
        print ("Starting gmeet on Linux Host running on host: ", linux_host)
        logging.debug(f"Starting gmeet on Linux Host running on host: {linux_host}")
        gmeets = "bash ./start_gmeets.sh " + str(ip1) + ' ' + str(ip2) + ' ' + str(linux_host) + ' ' + str(boot_delay)
        subprocess.run(gmeets)
    elif runType == "soc": 
        print("Starting GMEET SOCWATCH collection running on host: ", linux_host)
        logging.debug(f"Starting GMEET SOCWATCH collection running on host: {linux_host}")
        gmeet_soc = 'cmd.exe /C python.exe "run_pacs_GMEET_wSOC.py"'
        subprocess.run(gmeet_soc, shell=True)

## S0ix PACS
def s0ix():
    print ("Starting s0ix running on host: ", linux_host)
    logging.debug(f"Starting s0ix running on host: {linux_host}")
    soixRun = 'bash ./prep_s0ix.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
    subprocess.run(soixRun, shell=True) 


## Front load socwatch
with open ( csvFile ) as templateFile:
    template = csv.DictReader( templateFile, dialect='excel', delimiter=',' )

    for row in template:
        if row['run_type'] == 'soc' and driverless == True:
            print("Socwatch run found")
            print("Installing driverless socwatch ", str(ip1))
            logging.debug(f"Installing driverless socwatch {str(ip1)}")
            installDriverless = 'bash ./csv_socFunctions.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay) + ' ' + str('true')
            subprocess.run(installDriverless, shell=True)
            socInstall = True 
            break
        if row['run_type'] == 'soc' and driverless == False:
            print("Installing Custom Socwatch")
            logging.debug(f"Installing Custom Socwatch {str(ip1)}")
            installDriverless = 'bash ./csv_socFunctions.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay) + ' ' + str('false')
            subprocess.run(installDriverless, shell=True)
            socInstall = False
            break
templateFile.close()

## Import KPIs from CSV file and run KPIs row by row
with open ( csvFile ) as templateFile:
    #heading = next(templateFile)
    template = csv.DictReader( templateFile, dialect='excel', delimiter=',' )

    for row in template:
        #print(row['kpi'], row['iterations'], row['run_type'])
        kpi = row['kpi']
        iterate = row['iterations']
        runType = row['run_type']

        def run_kpi(kpi, iterate, runType ):
            #print(kpi + iterate + runType)
            if kpi == 'ido':
                for _ in range(int(iterate)):
                    nrIDO(runType)

            elif kpi == 'lvp':
                for _ in range(int(iterate)):
                    lvp(runType)

            elif kpi == 'plt':
                for _ in range(int(iterate)):
                    plt(runType)

            elif kpi == 'gmeet':
                for _ in range(int(iterate)):
                    gmeet(runType)            

            elif kpi == 's0ix' and runType == 'pac':
                for _ in range(int(iterate)):
                    s0ix()
                


        run_kpi(kpi, iterate, runType)

    if socInstall == True:
        logging.debug(f"Copying socwatch files from DUT to Windows host")
        copySocFiles = 'bash ./csv_socFunctions.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay) + ' ' + str('copy')
        subprocess.run(copySocFiles, shell=True)
        logging.debug(f"Socwatch files copied to Windows Host")

exit()
