#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import OpenRTM_aist


class ProcessCallbackBase:
    def init(self, prop):
        pass

    def exit(self):
        pass

    def callback(self, id, options):
        pass



processcallbackfactory = None


class ProcessCallbackFactory(OpenRTM_aist.Factory, ProcessCallbackBase):
    def __init__(self):
        OpenRTM_aist.Factory.__init__(self)
        pass

    def __del__(self):
        pass

    def instance():
        global processcallbackfactory

        if processcallbackfactory is None:
            processcallbackfactory = ProcessCallbackFactory()

        return processcallbackfactory

    instance = staticmethod(instance)
