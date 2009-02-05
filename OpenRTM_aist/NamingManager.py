#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file NamingManager.py
# @brief naming Service helper class
# @date $Date: 2007/08/27$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import threading
import traceback
import sys

import OpenRTM_aist



##
# @if jp
# @class ScopedLock
# @brief ScopedLock ���饹
#
# ��¾�����ѥ��å����饹��
#
# @since 0.4.0
#
# @else
#
# @endif
class ScopedLock:



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param mutex ���å��ѥߥ塼�ƥå���
  #
  # @else
  #
  # @endif
  def __init__(self, mutex):
    self.mutex = mutex
    self.mutex.acquire()


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @param self
  #
  # @else
  #
  # @endif
  def __del__(self):
    self.mutex.release()



##
# @if jp
#
# @class NamingBase
# @brief NamingService ��������ݥ��饹
#
# NamingServer ��������ݥ��󥿡��ե��������饹��
# ��ݴ������饹�ϡ��ʲ��δؿ��μ������󶡤��ʤ���Фʤ�ʤ���
# - bindObject() : ���ꤷ�����֥������Ȥ�NamingService�ؤΥХ����
# - unbindObject() : ���ꤷ�����֥������Ȥ�NamingService����Υ���Х����
#
# @since 0.4.0
#
# @else
#
# @endif
class NamingBase:



  ##
  # @if jp
  #
  # @brief NamingService�إХ���ɤ���ؿ�(���֥��饹������)
  #
  # ���ꤷ�����֥������Ȥ�NamingService�إХ���ɤ���<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param name �Х���ɻ���̾��
  # @param rtobj �Х�����оݥ��֥�������
  #
  # @else
  #
  # @endif
  def bindObject(self, name, rtobj):
    pass


  ##
  # @if jp
  #
  # @brief NamingService���饢��Х���ɤ���ؿ�(���֥��饹������)
  #
  # ���ꤷ�����֥������Ȥ�NamingService���饢��Х���ɤ���<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param name ����Х�����оݥ��֥�������
  #
  # @else
  #
  # @endif
  def unbindObject(self, name):
    pass



##
# @if jp
#
# @class NamingOnCorba
# @brief CORBA �� NamingServer �������饹
#
# CORBA �� NamingServer �����ѥ��饹��
# CORBA ����ݡ��ͥ�Ȥ�NamingService�ؤ���Ͽ������ʤɤ�������롣
#
# @since 0.4.0
#
# @else
#
# @biref ModuleManager class
#
# @endif
class NamingOnCorba(NamingBase):



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param orb ORB
  # @param names NamingServer ̾��
  #
  # @else
  #
  # @endif
  def __init__(self, orb, names):
    self._cosnaming = OpenRTM_aist.CorbaNaming(orb,names)


  ##
  # @if jp
  #
  # @brief ���ꤷ�� CORBA ���֥������Ȥ�NamingService�إХ����
  # 
  # ���ꤷ�� CORBA ���֥������Ȥ���ꤷ��̾�Τ� CORBA NamingService ��
  # �Х���ɤ��롣
  # 
  # @param self
  # @param name �Х���ɻ���̾��
  # @param rtobj �Х�����оݥ��֥�������
  #
  # @else
  #
  # @endif
  def bindObject(self, name, rtobj):
    try:
      self._cosnaming.rebindByString(name, rtobj.getObjRef(), True)
    except:
      pass


  ##
  # @if jp
  #
  # @brief ���ꤷ�� CORBA ���֥������Ȥ�NamingService���饢��Х����
  # 
  # ���ꤷ�� CORBA ���֥������Ȥ� CORBA NamingService ���饢��Х���ɤ��롣
  # 
  # @param self
  # @param name ����Х�����оݥ��֥�������
  #
  # @else
  #
  # @endif
  def unbindObject(self, name):
    try:
      self._cosnaming.unbind(name)
    except:
      traceback.print_exception(*sys.exc_info())



##
# @if jp
#
# @class NamingManager
# @brief NamingServer �������饹
#
# NamingServer �����ѥ��饹��
# ����ݡ��ͥ�Ȥ�NamingService�ؤ���Ͽ������ʤɤ�������롣
#
# @since 0.4.0
#
# @else
#
# @biref ModuleManager class
#
# @endif
class NamingManager:
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param manager �ޥ͡����㥪�֥�������
  #
  # @else
  #
  # @endif
  def __init__(self, manager):
    self._manager = manager
    self._rtcout = manager.getLogbuf()
    #self._rtcout.setLogLevel(manager.getConfig().getProperty("logger.log_level"))
    #self._rtcout.setLogLock(OpenRTM_aist.toBool(manager.getConfig().getProperty("logger.stream_lock"), "enable", "disable", False))
    self._names = []
    self._namesMutex = threading.RLock()
    self._compNames = []
    self._compNamesMutex = threading.RLock()


  ##
  # @if jp
  #
  # @brief NameServer ����Ͽ
  #
  # ���ꤷ�������� NameServer ����Ͽ���롣
  # ���߻����ǽ�ʷ����� CORBA �Τߡ�
  #
  # @param self
  # @param method NamingService �η���
  # @param name_server ��Ͽ���� NameServer ��̾��
  #
  # @else
  #
  # @endif
  def registerNameServer(self, method, name_server):
    self._rtcout.RTC_TRACE("NamingManager::registerNameServer(%s, %s)",
                           (method, name_server))
    name = self.createNamingObj(method, name_server)
    self._names.append(self.Names(method, name_server, name))


  ##
  # @if jp
  #
  # @brief ���ꤷ�����֥������Ȥ�NamingService�إХ����
  # 
  # ���ꤷ�����֥������Ȥ���ꤷ��̾�Τ� CORBA NamingService �إХ���ɤ��롣
  # 
  # @param self
  # @param name �Х���ɻ���̾��
  # @param rtobj �Х�����оݥ��֥�������
  #
  # @else
  #
  # @endif
  def bindObject(self, name, rtobj):
    self._rtcout.RTC_TRACE("NamingManager::bindObject(%s)", name)
    guard = ScopedLock(self._namesMutex)
    for i in range(len(self._names)):
      if self._names[i].ns:
        self._names[i].ns.bindObject(name, rtobj)
    self.registerCompName(name, rtobj)

  def bindManagerObject(self, name, mgr):
    self._rtcout.RTC_TRACE("NamingManager::bindManagerObject(%s)", name)
    guard = ScopedLock(self._namesMutex)
    for i in range(len(self._names)):
      if self._names[i].ns:
        self._names[i].ns.bindObject(name, mgr)


  ##
  # @if jp
  #
  # @brief NamingServer �ξ���ι���
  # 
  # ���ꤵ��Ƥ��� NameServer �����Ͽ����Ƥ��륪�֥������Ȥξ����
  # �������롣
  # 
  # @param self
  # 
  # @else
  #
  # @endif
  def update(self):
    self._rtcout.RTC_TRACE("NamingManager::update()")
    guard = ScopedLock(self._namesMutex)
    for i in range(len(self._names)):
      if self._names[i].ns is None:
        nsobj = self.createNamingObj(self._names[i].method,
                                     self._names[i].nsname)
        if nsobj:
          self._rtcout.RTC_INFO("New name server found: %s/%s",
                                (self._names[i].method,
                                 self._names[i].nsname))
          self._names[i].ns = nsobj
          self.bindCompsTo(nsobj)


  ##
  # @if jp
  #
  # @brief ���ꤷ�����֥������Ȥ�NamingService���饢��Х����
  # 
  # ���ꤷ�����֥������Ȥ� NamingService ���饢��Х���ɤ��롣
  # 
  # @param self
  # @param name ����Х�����оݥ��֥�������
  #
  # @else
  #
  # @endif
  def unbindObject(self, name):
    self._rtcout.RTC_TRACE("NamingManager::unbindObject(%s)", name)
    guard = ScopedLock(self._namesMutex)
    for i in range(len(self._names)):
      if self._names[i].ns:
        self._names[i].ns.unbindObject(name)
    self.unregisterCompName(name)


  ##
  # @if jp
  #
  # @brief ���ƤΥ��֥������Ȥ�NamingService���饢��Х����
  # 
  # ���ƤΥ��֥������Ȥ� CORBA NamingService ���饢��Х���ɤ��롣
  # 
  # @param self
  # 
  # @else
  #
  # @endif
  def unbindAll(self):
    self._rtcout.RTC_TRACE("NamingManager::unbindAll(): %d names.", len(self._compNames))
    guard = ScopedLock(self._compNamesMutex)
    for i in range(len(self._compNames)):
      self.unbindObject(self._compNames[i].name)


  ##
  # @if jp
  #
  # @brief �Х���ɤ���Ƥ������ƤΥ��֥������Ȥ����
  # 
  # �Х���ɤ���Ƥ������ƤΥ��֥������Ȥ� �������롣
  # 
  # @param self
  #
  # @return �Х���ɺѤߥ��֥������� �ꥹ��
  # 
  # @else
  #
  # @endif
  def getObjects(self):
    comps = []
    guard = ScopedLock(self._compNamesMutex)
    for i in range(len(self._compNames)):
      comps.append(self._compNames[i].rtobj)
    return comps


  ##
  # @if jp
  #
  # @brief NameServer �����ѥ��֥������Ȥ�����
  # 
  # ���ꤷ������NameServer �����ѥ��֥������Ȥ��������롣
  #
  # @param self
  # @param method NamingService ����
  # @param name_server NameServer ̾��
  # 
  # @return �������� NameServer ���֥�������
  # 
  # @else
  #
  # @endif
  def createNamingObj(self, method, name_server):
    mth = method
    if mth == "corba":
      try:
        name = OpenRTM_aist.NamingOnCorba(self._manager.getORB(),name_server)
        if name is None:
          return None
        self._rtcout.RTC_INFO("NameServer connection succeeded: %s/%s",
                              (method, name_server))
        return name
      except:
        self._rtcout.RTC_INFO("NameServer connection failed: %s/%s",
                              (method, name_server))
        return None

    return None


  ##
  # @if jp
  #
  # @brief ����Ѥߥ���ݡ��ͥ�Ȥ� NameServer ����Ͽ
  # 
  # ����Ѥߥ���ݡ��ͥ�Ȥ���ꤷ�� NameServer ����Ͽ���롣
  #
  # @param self
  # @param ns ��Ͽ�о� NameServer
  # 
  # @else
  #
  # @endif
  def bindCompsTo(self, ns):
    for i in range(len(self._compNames)):
      ns.bindObject(self._compNames[i].name, self._compNames[i].rtobj)


  ##
  # @if jp
  #
  # @brief NameServer ����Ͽ���륳��ݡ��ͥ�Ȥ�����
  # 
  # NameServer ����Ͽ���륳��ݡ��ͥ�Ȥ����ꤹ�롣
  #
  # @param self
  # @param name ����ݡ��ͥ�Ȥ���Ͽ��̾��
  # @param rtobj ��Ͽ�оݥ��֥�������
  # 
  # @else
  #
  # @endif
  def registerCompName(self, name, rtobj):
    for i in range(len(self._compNames)):
      if self._compNames[i].name == name:
        self._compNames[i].rtobj = rtobj
        return

    self._compNames.append(self.Comps(name, rtobj))
    return


  ##
  # @if jp
  #
  # @brief NameServer ����Ͽ���륳��ݡ��ͥ�Ȥ�������
  # 
  # NameServer ����Ͽ���륳��ݡ��ͥ�Ȥ�����������롣
  #
  # @param self
  # @param name �������оݥ���ݡ��ͥ�Ȥ�̾��
  # 
  # @else
  #
  # @endif
  def unregisterCompName(self, name):
    len_ = len(self._compNames)
    for i in range(len_):
      idx = (len_-1) - i
      if self._compNames[idx].name == name:
        del self._compNames[idx]
        return
    return
    


  # Name Servers' method/name and object
  ##
  # @if jp
  # @class Names
  # @brief NameServer �����ѥ��饹
  # @else
  #
  # @endif
  class Names:
    def __init__(self, meth, name, naming):
      self.method = meth
      self.nsname = name
      self.ns     = naming


  # Components' name and object
  ##
  # @if jp
  # @class Comps
  # @brief ����ݡ��ͥ�ȴ����ѥ��饹
  # @else
  #
  # @endif
  class Comps:
    def __init__(self, n, obj):
      self.name = n
      self.rtobj = obj