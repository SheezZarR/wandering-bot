HELP_CMD = "help"
SET_CMD = "std"
REMOVE_CMD = "rmd"
EDIT_CMD = "edd"
LIST_CMD = "lsd"

SET_CMD_FULL = f'`/{SET_CMD} TIMER_NAME DESTINATION(URL) FREQUENCY(IN SECONDS)`'
REMOVE_CMD_FULL = f'`/{REMOVE_CMD} TIMER_NAME`'
EDIT_CMD_FULL = f'`/{EDIT_CMD} TIMER_NAME NEW_DESTINATION(OPTIONAL) FREQUENCY(OPTIONAL)`'


SET_TIMER_EXPLAIN = f"Usage: {SET_CMD_FULL}" 
REMOVE_TIMER_EXPLAIN = f"Usage: {REMOVE_CMD_FULL}"
EDIT_TIMER_EXPLAIN = f"Usage: {EDIT_CMD_FULL}"

AVAILABLE_ACTIONS_EXPLAIN = f'Available commands:\n' \
f'{SET_CMD_FULL} - to add a resource to be visited\n' \
f'{REMOVE_CMD_FULL} - to remove an existing visit destination\n' \
f'{EDIT_CMD_FULL} - to replace a link of adjust visit interval\n' \
f'`/{LIST_CMD}`- to list added destinations'


STARTUP_EXPLAIN = f'Hello! Use `/help` to list available commands at any point.\n' \
f'{AVAILABLE_ACTIONS_EXPLAIN}'
