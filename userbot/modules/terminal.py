# Copyright 2020 nunopenim @github
# Copyright 2020 prototype74 @github
#
# Licensed under the PEL (Penim Enterprises License), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the PE License

from userbot import tgclient, MODULE_DESC, MODULE_DICT
from userbot.include.language_processor import TerminalText as msgRep, ModuleDescriptions as descRep, ModuleUsages as usageRep
from telethon.events import NewMessage
from os.path import basename
from subprocess import check_output, CalledProcessError

@tgclient.on(NewMessage(pattern=r"^\.shell(?: |$)(.*)", outgoing=True))
async def bash(command):
    commandArray = command.text.split(" ")
    bashCmd = ""
    for word in commandArray: # building the command
        if not word == ".shell": # Probably I should find a way not to have this hardcoded
            bashCmd += word + " "
    try:
        cmd_output = check_output(bashCmd, shell=True).decode()
    except CalledProcessError:
        cmd_output = msgRep.BASH_ERROR
    output = "$ " + bashCmd + "\n\n" + cmd_output
    await command.edit("`" + output + "`")
    return

MODULE_DESC.update({basename(__file__)[:-3]: descRep.TERMINAL_DESC})
MODULE_DICT.update({basename(__file__)[:-3]: usageRep.TERMINAL_USAGE})
