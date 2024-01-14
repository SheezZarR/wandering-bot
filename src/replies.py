HELP_CMD = "help"
SET_CMD = "std"
REMOVE_CMD = "rmd"
LIST_CMD = "lsd"

SET_CMD_FULL = f"`/{SET_CMD} TIMER_NAME DESTINATION(URL) FREQUENCY(IN SECONDS)`"
REMOVE_CMD_FULL = f"`/{REMOVE_CMD} TIMER_NAME`"


SET_TIMER_EXPLAIN = f"Usage: {SET_CMD_FULL}"
REMOVE_TIMER_EXPLAIN = f"Usage: {REMOVE_CMD_FULL}"

AVAILABLE_ACTIONS_EXPLAIN = (
    f"Available commands:\n"
    f"{SET_CMD_FULL} - to add a resource to be visited\n"
    f"{REMOVE_CMD_FULL} - to remove an existing visit destination\n"
    f"`/{LIST_CMD}`- to list added destinations"
)


STARTUP_EXPLAIN = (
    f"Hello! Use `/help` to list available commands at any point.\n"
    f"{AVAILABLE_ACTIONS_EXPLAIN}"
)
