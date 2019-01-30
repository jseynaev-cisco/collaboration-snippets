# Spark BOT
access_token='prettylongstringofjibberjabber'
webhook_name = 'thehook'
webhook_url='http://someexposed.url.to.your.server.io'

# UCM AXL API
AXL_username='ucm_application_user_with_axl_rights'
AXL_password=''

# UCM EMAPI
EMAPI_username='ucm_application_user_with_em_proxy_rights'
EMAPI_password=''

# UCM Clusters to query
# name (just a reference), server where AXL is running, server where EMAPI is running
clusters = [
    ["Server1","axlserver.myorg.net","emserver.myorg.net"],
    ["Server2","axlserver2.myorg.net","emserver2.myorg.net"],
]

# Help message (markdown)
help_message = """
# I can log you in into your phone
Just say "log me in into <number>" and I'll do my best to do so.
When you are done for the day, just say "log me out" ...

### commands
- hello
- log me in into <number>
- log me out
- help

### limitation
- no EMCC
- Uses your primary profile only (cannot choose profile yet)
"""
