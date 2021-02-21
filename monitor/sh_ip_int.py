from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from user_login import user_login
from nornir.core.filter import F
import ipdb

user_login()
nr = InitNornir(config_file="config.yaml")
task1 = nr.filter(F(groups__contains='IOS'))


def version_task(task):
    r = task.run(netmiko_send_command,
                 command_string=" show ip int br | inc down ")
    task.host['facts'] = r.result
    #result1 = task.host['facts']['cdp']['index']
    #for i in result1:
    #    local_inter = result1[i]['local_interface']
    #    remote_port = result1[i]['port_id']
    #    remote_id = result1[i]['device_id']
    #    cdp_config = task.run(netmiko_send_config, name="CDP Config",
        #                      config_commands=[
        #                        f"interface {local_inter}",
        #                        f"description {remote_id} on {remote_port}"
        #                        ])


sh_version = task1.run(task=version_task)
print_result(sh_version)
#ipdb.set_trace()
