"""
:Authors:  Jan Seynaeve
"""

import os
import getpass
from jinja2 import Template
from raw_axl import RawAxl

# ask some things
print("ucm server and user with UCM AXL privileges")
server = input('ucm hostname or IP: ')
username = input('username: ')
password = getpass.getpass('password: ')

print("We'll need a couple of details on the phone (9971)")
name = 'SEP' + input('MAC (SEP will be prefixed): ')
phone_css = input('Calling Search Space for the phone: ')
line_partition = input('Partition for the line: ')
line_css = input('Calling Search Space for the line: ')
device_pool = input('Device Pool: ')
dn = input('Number / DN: ')
reception = input('Reception or central number (for a speeddial): ')

# load the template for the line
with open(os.path.join('templates', 'em-line.xml')) as template_file:
    template = Template(template_file.read())

# do the necessary replacements
line_xml = template.render(
    {'line_css': line_css,
     'line_partition': line_partition,
     'dn': dn})
print(line_xml)

# load the template for the phone
with open(os.path.join('templates', 'em-phone.xml')) as template_file:
    template = Template(template_file.read())

# do the necessary replacements
phone_xml = template.render(
    {'name': name,
     'phone_css': phone_css,
     'device_pool': device_pool,
     'dn': dn,
     'line_partition': line_partition,
     'reception': reception})
print(phone_xml)

# add line
print("adding new line")
axl = RawAxl(username, password, server)
response = axl.execute('addLine', {}, xml=line_xml)
print(response)

# add phone
print("adding new phone")
response = axl.execute('addPhone', {}, xml=phone_xml)
print(response)
