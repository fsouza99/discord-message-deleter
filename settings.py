# Might be useful.
INFINITE = 2**31-1

# Access control.
LOGIN_ATTEMPTS = 3
SELECTION_ATTEMPTS = 3

"""
Autorestart control

NIL_TOLERANCE: How many zero status (errors and undeleted messages) will be tolerated.
TARGET_COUNT: How many messages to delete.
"""
NIL_TOLERANCE = 3
TARGET_COUNT = 100

# User information.
EMAIL = "myemail@domain.com"
USERNAME = "username"
PASSWORD = "password"

"""
Search keys

Set dates on yyyy-mm-dd format. Assign an empty string to the filter you don't want to apply.

Alternatively, you can set a complete SEARCHKEY directly. Set it to None if you don't want to use it. Hint: You can run a search on Discord and paste the search box's content into SEARCHKEY.
"""
SERVER = "TargetServer"
CHANNEL = "TargetChannel"
ITEM = ""
DURING = ""
AFTER = "2022-01-01"
BEFORE = "2022-12-31"
SENTENCE = ""
MENTION = "Friend"
SEARCHKEY = None

