import yaml
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result, print_title
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_netmiko.tasks import netmiko_send_config
from user_login import user_login
from nornir.core.filter import F


user_login()
nr = InitNornir(config_file="config.yaml")
task1 = nr.filter(F(groups__contains='spine'))

vlan_list = []
name_list = []
multi_list = []
tenant_list = []
ip_list = []
vn_list = []
vn_seg_name = []
tenant = input('enter tenant name ')
tenant_list.append(tenant)
total = int(input('enter total vlan : '))
for i in range(1, total):
    while len(vlan_list) < total:
        vlan = int(input('Please enter vlan %d no: ' % i))
        name_vlan = str(input('Please enter vlan %d name: ' % i))
        ip = str(input('Please enter %d ip address no:  ' % i))
        multi = str(input('Please enter %d multicast address no:  ' % i))
        vlan_list.append(vlan)
        name_list.append(name_vlan)
        ip_list.append(ip)
        multi_list.append(multi)
        i = i+1


def vn_seg(vlan_list):
    for i in vlan_list:
        a = str(i)
        k = len(a)
        if k == 1:
            vn_seg1 = str(10000) + a
        elif k == 2:
            vn_seg1 = str(1000) + a
        elif k == 3:
            vn_seg1 = str(100) + a
        elif k == 4:
            vn_seg1 = str(10) + a
        else:
            print("high")
            exit()
        vn_list.append(int(vn_seg1))
    return int(vn_seg1)
    vn_seg(vlan_list)
    return vlan_list, name_list


def vlan_vn_seg_name(vlan_list, multi_list, vn_list, name_list, tenant_list):
    n = len(vlan_list)
    for i in range(n):
        list = {'id': vlan_list[i], 'segment': vn_list[i],
                'name': name_list[i], 'multicast': multi_list[i], 'tenant':
                tenant_list[0], 'ip': ip_list[i]}
        vn_seg_name.append(list)
    return vn_seg_name


vn_seg(vlan_list)
config1 = dict()
config1 = vlan_vn_seg_name(vlan_list, multi_list, vn_list, name_list,
                           tenant_list)

final_list = {'L2VNI': config1}
print(final_list)


with open(r'test1.yaml', 'w') as file:
    documents = yaml.dump(final_list, file, default_flow_style=False)


def load_vars(task1):
    data = task1.run(task=load_yaml, file='/home/sunil/my-nornir/test1.yaml')
    task1.host["facts"] = data.result
    print_result(data.result)
    basic_configuration(task1)


def basic_configuration(task1):
    r = task1.run(task=template_file, template="L2-VxLAN1.j2",
                  path='/home/sunil/my-nornir')
    task1.host["test1.yaml"] = r.result
    vlan_output = task1.host["test1.yaml"]
    vlan_send = vlan_output.splitlines()
    task1.run(task=netmiko_send_config, name="VLAN Commands",
              config_commands=vlan_send)


print_title("config")
result = nr.run(task=load_vars)
print_result(result)
