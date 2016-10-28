#!/usr/bin/env python
# coding:utf-8
import sys
import subprocess


class AutoInstall(object):
    _loaded = set()

    @classmethod
    def find_module(cls, name, path, target=None):
        if path is None and name not in cls._loaded:
            cls._loaded.add(name)
            print("Installing", name)
            try:
                out = subprocess.check_output(['sudo', sys.executable, '-m', 'pip', 'install', name])
                print(out)
            except Exception as e:
                print("Failed" + e.message)
        return None

sys.meta_path.append(AutoInstall)
