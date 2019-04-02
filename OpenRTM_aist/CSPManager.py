#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file CSPManager.py
# @brief CSP Manager class
# @date $Date: $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2019
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist
import copy
import threading



##
# @if jp
#
# @class CSPManager
#
# @brief CSPOutPort��CSPInPort��������륯�饹
# 
#
# @since 2.0.0
#
# @else
#
# @class CSPManager
#
# @brief 
#
#
# @since 2.0.0
#
# @endif
#
class CSPManager(object):
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  #
  # @else
  #
  # @brief A constructor.
  #
  # @param self
  #
  # @endif
  #
  def __init__(self):
    self._outports = []
    self._inports = []
    self._ctrl = OpenRTM_aist.CSPManager.CSPThreadCtrl()
    self._writableOutPort = None
    self._readableInPort = None
    
    
  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯����
  #
  # @else
  #
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self):
    pass

  ##
  # @if jp
  #
  # @brief �񤭹��߲�ǽ��OutPort�����򤹤�
  #
  # @param self
  # @return ret, port
  # ret��True(�񤭹��߲�ǽ��OutPort��¸�ߤ���)��False(¸�ߤ��ʤ�)
  # port���񤭹��߲�ǽ��OutPort������Ǥ��ʤ��ä�����None
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return 
  #
  # @endif
  #
  def selectOutPort(self):
    for port in self._outports:
      if port.select():
        return True, port
    return False,None

  ##
  # @if jp
  #
  # @brief �ɤ߹��߲�ǽ��InPort�����򤹤�
  #
  # @param self
  # @return ret, port
  # ret��True(�ɤ߹��߲�ǽ��InPort��¸�ߤ���)��False(¸�ߤ��ʤ�)
  # port���ɤ߹��߲�ǽ��InPort������Ǥ��ʤ��ä�����None
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return 
  #
  # @endif
  #
  def selectInPort(self):
    for port in self._inports:
      if port.select():
        return True, port
    return False,None

  ##
  # @if jp
  #
  # @brief �ɤ߹��߲�ǽ��InPort���⤷���Ͻ񤭹��߲�ǽ��OutPort�����򤹤�
  # �ɤ߹��߲�ǽ��InPort���񤭹��߲�ǽ��OutPort��¸�ߤ��ʤ����ϥ����ॢ���Ȥޤ��Ե�����
  # �Ե�����塢�ɤ߹��߲�ǽ��InPort���⤷���Ͻ񤭹��߲�ǽ��OutPort��������򤹤�
  #
  # @param self
  # @param timeout �Ե��Υ����ॢ���Ȼ���
  # @return ret, outport, inport
  # ret��Ture(�񤭹��ߡ��ɤ߹��߲�ǽ�ʥݡ��Ȥ�¸��)��False(�����ॢ����)
  # outport��OutPort�����򤷤����ˡ��񤭹��߲�ǽ��OutPort���Ǽ
  # inport��InPort�����򤷤����ˡ��ɤ߹��߲�ǽ��Inort���Ǽ
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param timeout 
  # @return 
  #
  # @endif
  #
  def select(self, timeout):
    ret, port = self.selectOutPort()
    if ret:
      return ret, port, None
    ret, port = self.selectInPort()
    if ret:
      return ret, None, port

    guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
    self._ctrl._waiting = True
    self._ctrl._timeout = True
    self._ctrl._cond.wait(timeout)
    self._ctrl._waiting = False
    del guard
    if self._ctrl._timeout:
      return False, None, None
    else:
      if self._writableOutPort or self._readableInPort:
        inport = self._readableInPort
        outport = self._writableOutPort
        self._writableOutPort = None
        self._readableInPort = None
        return True, outport, inport
      return False, None, None


  ##
  # @if jp
  #
  # @brief �Ե����ֲ��������
  # select�ؿ����Ե����Ƥ�����ˡ��Ե���������
  #
  # @param self
  # @return True���Ե����֤�����False���Ե����֤ǤϤʤ�
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return 
  #
  # @endif
  #
  def notify(self, outport=None, inport=None):
    guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
    if self._ctrl._waiting:
      self._ctrl._timeout = False
      if outport:
        self._writableOutPort = outport
      elif inport:
        self._readableInPort = inport
      self._ctrl._cond.notify()
      return True
    else:
      return False

  ##
  # @if jp
  #
  # @brief InPort���ɲ�
  #
  # @param self
  # @param port InPort
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param port 
  #
  # @endif
  #
  def addInPort(self, port):
    self._inports.append(port)

  ##
  # @if jp
  #
  # @brief OutPort���ɲ�
  #
  # @param self
  # @param port OutPort
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param port 
  #
  # @endif
  #
  def addOutPort(self, port):
    self._outports.append(port)

  ##
  # @if jp
  #
  # @brief InPort����
  #
  # @param self
  # @param port InPort
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param port 
  #
  # @endif
  #
  def removeInPort(self, port):
    self._inports.remove(port)

  ##
  # @if jp
  #
  # @brief Outort����
  #
  # @param self
  # @param port OutPort
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param port 
  #
  # @endif
  #
  def removeOutPort(self, port):
    self._outports.remove(port)


  class CSPThreadCtrl:
    def __init__(self):
      self._mutex = threading.RLock()
      self._cond = threading.Condition(self._mutex)
      self._port = None
      self._waiting = False
      self._timeout = True

