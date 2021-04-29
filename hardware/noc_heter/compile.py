from paramiko import SSHClient
from scp import SCPClient
import os

client = SSHClient()
client.load_system_host_keys()
client.connect(
                'ece-linlabsrv01.ece.gatech.edu',
                username='ssingam3',
                key_filename='/home/sriharsha/.ssh/id_rsa',
                timeout=5000
            )

scp = SCPClient(client.get_transport())

os.system('tar -czf full_noc.tar.gz full_noc/')
os.system('tar -czf traffic_generator_receiver.tar.gz ../traffic_generator_receiver/')
scp.put('full_noc.tar.gz')
scp.put('traffic_generator_receiver.tar.gz')

commands = [
    'pwd',
    'rm -rf /nethome/ssingam3/noc_synthesis/src',
    'mkdir -p /nethome/ssingam3/noc_synthesis/src',
    'tar -xvf full_noc.tar.gz -C /nethome/ssingam3/noc_synthesis/src/',
    'rm -rf /nethome/ssingam3/traffic_generator_receiver',
    'tar -xvf traffic_generator_receiver.tar.gz -C /nethome/ssingam3/',
    'rm -rf /nethome/ssingam3/traffic_generator_receiver/VHDL/traffic_gen_with_noc/rtl',
    'tar -xvf full_noc.tar.gz -C /nethome/ssingam3/traffic_generator_receiver/VHDL/traffic_gen_with_noc',
    'mv /nethome/ssingam3/traffic_generator_receiver/VHDL/traffic_gen_with_noc/full_noc /nethome/ssingam3/traffic_generator_receiver/VHDL/traffic_gen_with_noc/rtl',
    'mv /nethome/ssingam3/noc_synthesis/src/full_noc/* /nethome/ssingam3/noc_synthesis/src/',
    'rmdir /nethome/ssingam3/noc_synthesis/src/full_noc'
]

# /bin/tcsh && cd /nethome/ssingam3/noc_synthesis/ && source /tools/newsynopsys/cshrc.synopsys && source /tools/cadence/innovus1913/cshrc.meta && make flow
# source /tools/mentor/questa/q20191/cshrc.questa

stdins = []
stdouts = []
stderrs = []

for command in commands:
    stdin, stdout, stderr = client.exec_command(command)
    stdoutp = []
    for line in stdout:
        stdoutp.append(line.strip())
    stderrp = []
    for line in stderr:
        stderrp.append(line.strip())
    print('[' + command + '] -> STDOUT: ' + str(stdoutp))
    print('[' + command + '] -> STDERR: ' + str(stderrp))
    # stdins.append(stdin)
    stdouts.append(stdoutp)
    stderrs.append(stderrp)


scp.close()
client.close()
