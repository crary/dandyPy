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

## Frontload stop script
stopScript = "bash -c; sshpass -p xxxxx ssh -o StrictHostKeyChecking=no moo@" + str(linux_host) +  str(' "') \
+ ". ~/Desktop/Automation_linux/copy_stopScript.sh " + str(ip1) +  str('"')
subprocess.run(stopScript, shell=True)
print("Stop script loaded onto DUT ", ip1)


## Print the number of lines in the choosen CSV file
kpi_csv = pd.read_csv(csvFile)
print("file has " + str(len(kpi_csv)) + " lines")

## Reset count files to 1
kpis = []
kpis.append("nr-ido_num_new.txt")
kpis.append("lvp_num.txt")
kpis.append("plt_num.txt")
kpis.append("sOix_num.txt")
kpis.append("meets_num.txt")


for i in range(len(kpis)):
    file = open(kpis[i], 'w')
    file.write(str(1))
    file.close()

## define kpis to run
## No Reboot PACS IDO
def nrIDO():
    nrIDO = 'bash ./start_nr-ido.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
    subprocess.run(nrIDO, shell=True)
    print ("Starting NR_IDO on Linux Host...")
    print("NR_IDO running on host: ", linux_host )

## LVP PACS 
def lvp():
    print ("Starting LVP on Linux Host...")
    print("LVP running on host: ", linux_host )
    runLvp = 'bash ./start_LVP.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
    subprocess.run(runLvp, shell=True)

## PLT PACS
def plt():
    print ("Starting PLT on Linux Host...")
    print("PLT running on host: ", linux_host )
    runPlt = 'bash ./start_PLT.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
    subprocess.run(runPlt, shell=True)

## Gmeet
def gmeet():
    print ("Starting gmeet on Linux Host...")
    print("Gmeet running on host: ", linux_host )
    gmeets = "bash ./start_gmeets.sh " + str(ip1) + ' ' + str(ip2) + ' ' + str(linux_host) + ' ' + str(boot_delay)
    subprocess.run(gmeets) 

## S0ix PACS
def s0ix():
    print ("Starting s0ix on Linux Host...")
    print("s0ix running on host: ", linux_host )
    soixRun = 'bash ./prep_s0ix.sh ' + str(ip1) + ' ' + str(linux_host) + ' ' + str(boot_delay)
    subprocess.run(soixRun, shell=True) 


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
            if kpi == 'ido' and runType == 'pac':
                for _ in range(int(iterate)):
                    nrIDO()

            elif kpi == 'lvp' and runType == 'pac':
                for _ in range(int(iterate)):
                    lvp()

            elif kpi == 'plt' and runType == 'pac':
                for _ in range(int(iterate)):
                    plt()

            elif kpi == 'gmeet' and runType == 'pac':
                for _ in range(int(iterate)):
                    gmeet()            

            elif kpi == 's0ix' and runType == 'pac':
                for _ in range(int(iterate)):
                    s0ix()
                


        run_kpi(kpi, iterate, runType)

