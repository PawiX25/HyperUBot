# Copyright 2021 nunopenim @github
# Copyright 2021 prototype74 @github
#
# Licensed under the PEL (Penim Enterprises License), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the PE License

from userbot import tgclient
from userbot.sysutils.registration import (getAllModules,
                                           getBuiltInModules,
                                           getHandlers,
                                           getLoadModules,
                                           getRegisteredCMDs,
                                           getUserModules,
                                           update_all_modules,
                                           update_built_in_modules,
                                           update_load_modules,
                                           update_handlers,
                                           update_user_modules,
                                           unregister_module_desc,
                                           unregister_module_info,
                                           unregister_cmd)
from inspect import currentframe, getouterframes
from logging import getLogger
import importlib
import os
import sys

log = getLogger(__name__)


class _ModuleLoader:
    def __init__(self):
        """
        Initialize the module loader
        """
        self.__imported_module = None
        # TODO:
        # self.__not_load_modules = getConfig("NOT_LOAD_MODULES", [])

    def _import_module(self, module: str, is_usermodule: bool):
        """
        Import a module and straight start it
        """
        special_caller = [os.path.join("userbot", "__main__.py"),
                          os.path.join("userbot", "modules",
                                       "_package_manager.py"),
                          os.path.join("userbot", "modules",
                                       "sideloader.py")]
        sys_caller = getouterframes(currentframe(), 2)[2].filename
        valid_caller = False
        for caller in special_caller:
            if sys_caller.endswith(caller):
                valid_caller = True
                break
        if not valid_caller:
            caller = getouterframes(currentframe(), 2)[2]
            caller = f"{os.path.basename(caller.filename)}:{caller.lineno}"
            log.warning(f"Not a valid caller (requested by {caller})")
            return

        if module.startswith("__"):
            log.warning(f"Illegal module name '{module}'")
            return

        path = f"userbot.modules_user.{module}" \
               if is_usermodule else f"userbot.modules.{module}"
        reinstall = False

        if is_usermodule:
            if module in getBuiltInModules():
                log.warning(f"Module '{module}' present as "
                            "built-in module already")
                return
            if path in sys.modules or module in getAllModules():
                self._unimport_module(module)
                reinstall = True

        update_all_modules(module)
        if is_usermodule:
            update_user_modules(module)
        else:
            update_built_in_modules(module)

        try:
            self.__imported_module = importlib.import_module(path)
            update_load_modules(module, True)
            if reinstall:
                log.info(f"[REINSTALL] Module '{module}' imported")
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except (BaseException, Exception):
            log.error(f"Failed to start module '{module}' due "
                      "to an unhandled exception",
                      exc_info=True)
            update_load_modules(module, False)
        finally:
            self.__imported_module = None
        return

    def _unimport_module(self, module: str):
        """
        Tries to remove all data from the target module and finally to
        unimport it from runtime
        """
        special_caller = [os.path.join("userbot", "_core",
                                       os.path.basename(__file__)),
                          os.path.join("userbot", "modules",
                                       "_package_manager.py")]
        sys_caller = getouterframes(currentframe(), 2)[2].filename
        valid_caller = False
        for caller in special_caller:
            if sys_caller.endswith(caller):
                valid_caller = True
                break
        if not valid_caller:
            caller = getouterframes(currentframe(), 2)[2]
            caller = f"{os.path.basename(caller.filename)}:{caller.lineno}"
            log.warning(f"Not a valid caller (requested by {caller})")
            return

        if module.startswith("__"):
            log.warning(f"Illegal module name '{module}'")
            return

        if module not in getUserModules():
            log.error(f"Target module '{module}' is not an user module!")
            return

        handlers_from_module = getHandlers().get(module)
        if handlers_from_module:
            for handler in handlers_from_module:
                tgclient.remove_event_handler(handler)
            log.info(f"Event handlers from '{module}' removed")
        else:
            log.info(f"Module '{module}' has no registered event handlers")
        update_handlers(module, None, True)
        unregister_module_desc(module)
        unregister_module_info(module)
        cmds_to_remove = []
        for cmd, cmd_attrs in getRegisteredCMDs().items():
            mod_name = cmd_attrs.get("module_name", "")
            if module == mod_name:
                cmds_to_remove.append(cmd)
        if cmds_to_remove:
            for cmd in cmds_to_remove:
                unregister_cmd(cmd)
        update_all_modules(module, True)
        update_load_modules(module, False, True)
        update_user_modules(module, True)
        try:
            path = f"userbot.modules_user.{module}"
            if path in sys.modules:
                sys.modules.pop(path)
                log.info(f"Module '{module}' unimported successfully")
            else:
                log.info(f"Removed module '{module}' from modules data "
                         "successfully")
        except KeyError:
            log.error(f"Failed to unimport module '{module}'")
        return


_moduleloader = _ModuleLoader()


def import_module(module: str, is_usermodule: bool):
    _moduleloader._import_module(module, is_usermodule)
    return

def unimport_module(module: str):
    _moduleloader._unimport_module(module)
    return

