import os, sys
from jinja2 import Template
from raw_axl import RawAxl

# ask some things
name = 'SEPABCAAAAAAAAA'
sitename = 'KJK'
dn = '1234'
reception = '1111'

# load the template for the line
template_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'templates', 'em-line.xml')
with open(template_file) as _file:
    template = Template(_file.read())

# do the necessary replacements
line_xml = template.render(
    {'site': sitename,
     'dn': dn})
print(line_xml)

# load the template for the phone
template_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'templates', 'em-phone.xml')
with open(template_file) as _file:
    template = Template(_file.read())

# do the necessary replacements
phone_xml = template.render(
    {'name': name,
     'site': sitename,
     'dn': dn,
     'reception': reception})
print(phone_xml)

# add line
axl = RawAxl(*sys.argv[1:])
response = axl.execute('addLine', {}, xml=line_xml)
print(response)

# add phone
response = axl.execute('addPhone', {}, xml=phone_xml)
print(response)
