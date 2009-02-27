#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PeriodicECSharedComposite.h
# @brief Periodic Execution Context Shared Composite Component class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#

import string
import sys

from omniORB import CORBA
import OpenRTM, OpenRTM__POA
import RTC,RTC__POA
import OpenRTM_aist


periodicecsharedcomposite_spec = ["implementation_id", "PeriodicECSharedComposite",
                                  "type_name",         "PeriodicECSharedComposite",
                                  "description",       "PeriodicECSharedComposite",
                                  "version",           "1.0",
                                  "vendor",            "jp.go.aist",
                                  "category",          "composite.PeriodicECShared",
                                  "activity_type",     "DataFlowComponent",
                                  "max_instance",      "0",
                                  "language",          "Python",
                                  "lang_type",         "script",
                                  "exported_ports",    "",
                                  "conf.default.members", "",
                                  "conf.default.exported_ports", "",
                                  ""]
                                  


def stringToStrVec(v, _is):
    v = _is.split(",")
    return True


##
# @if jp
# @namespace SDOPacakge
#
# @brief SDO
#
# @else
#
# @namespace SDOPackage
#
# @brief SDO
#
# @endif
#
class PeriodicECOrganization(OpenRTM_aist.Organization_impl):


    def __init__(self, rtobj):
        OpenRTM_aist.Organization_impl.__init__(self,rtobj.getObjRef())
        self._rtobj      = rtobj
        self._ec         = None
        self._rtcMembers = []


    ##
    # @if jp
    # 
    # @brief [CORBA interface] Organization���С����ɲä���
    #
    # Organization ���ݻ�������С��ꥹ�Ȥ�Ϳ����줿SDOList���ɲä��롣
    # 
    # @param sdo_list �ɲä���� SDO ���С��Υꥹ��
    # @return �ɲä������������ɤ�����bool���֤����
    #
    # @else
    # 
    # @brief [CORBA interface] Add Organization member
    #
    # This operation adds the given SDOList to the existing organization's 
    # member list
    # 
    # @param sdo_list SDO member list to be added
    # @return boolean will returned if the operation succeed
    #
    # @endif
    #
    # Boolean add_members(const SDOList& sdo_list)
    def add_members(self, sdo_list):
        for sdo in sdo_list:
            dfc = [None]
            if not self.sdoToDFC(sdo, dfc):
                continue
            member = self.Member(dfc[0])
            self.stopOwnedEC(member)
            self.addOrganizationToTarget(member)
            self.addParticipantToEC(member)
            self.delegatePort(member)
            self._rtcMembers.append(member)


        result = OpenRTM_aist.Organization_impl.add_members(self,sdo_list)

        return result


    ##
    # @if jp
    # 
    # @brief [CORBA interface] Organization���С��򥻥åȤ���
    #
    # Organization ���ݻ�������С��ꥹ�Ȥ�������Ϳ����줿
    # SDOList�򿷵��˥��åȤ��롣
    # 
    # @param sdo_list �����˥��åȤ���� SDO ���С��Υꥹ��
    # @return �ɲä������������ɤ�����bool���֤����
    #
    # @else
    # 
    # @brief [CORBA interface] Set Organization member
    #
    # This operation removes existing member list and sets the given
    # SDOList to the existing organization's member list
    # 
    # @param sdo_list SDO member list to be set
    # @return boolean will returned if the operation succeed
    #
    # @endif
    #
    # Boolean set_members(const SDOList& sdo_list)
    def set_members(self, sdo_list):
        self._rtcMembers = []

        for sdo in sdo_list:
          dfc = [None]
          if not self.sdoToDFC(sdo, dfc):
              print "SDO is not DFC"
              continue

          member = self.Member(dfc[0])
          self.stopOwnedEC(member)
          self.addOrganizationToTarget(member)
          self.addParticipantToEC(member)
          self.delegatePort(member)
          self._rtcMembers.append(member)

        result = OpenRTM_aist.Organization_impl.set_members(self, sdo_list)

        return result


    ##
    # @if jp
    # 
    # @brief [CORBA interface] Organization���С���������
    #
    # Organization ���ݻ�������С��ꥹ����������SDO�������롣
    # 
    # @param id �������� SDO �� ID
    # @return �ɲä������������ɤ�����bool���֤����
    #
    # @else
    # 
    # @brief [CORBA interface] Remove a member of Organization
    #
    # This operation removes a SDO from existing member list by specified ID.
    # 
    # @param id The ID of the SDO to be removed
    # @return boolean will returned if the operation succeed
    #
    # @endif
    #
    # Boolean remove_member(const char* id)
    def remove_member(self, id):
        rm_rtc = []
        for member in self._rtcMembers:
            if str(id) != str(member._profile.instance_name):
                continue
            self.removePort(member)
            self.removeParticipantFromEC(member)
            self.removeOrganizationFromTarget(member)
            self.startOwnedEC(member)
            rm_rtc.append(member)

        for m in rm_rtc:
            self._rtcMembers.remove(m)
            
        result = OpenRTM_aist.Organization_impl.remove_member(self, id)
        return result


    def removeAllMembers(self):
        for member in self._rtcMembers:
            self.removePort(member)
            self.removeParticipantFromEC(member)
            self.removeOrganizationFromTarget(member)
            self.startOwnedEC(member)
            OpenRTM_aist.Organization_impl.remove_member(self, member._profile.instance_name)

        self._rtcMembers = []

        
    ##
    # @if jp
    # @brief SDO����DFC�ؤ��Ѵ�
    # @else
    # @brief Conversion from SDO to DFC
    # @endif
    #
    # bool sdoToDFC(const SDO_ptr sdo, ::OpenRTM::DataFlowComponent_ptr& dfc);
    def sdoToDFC(self, sdo, dfc):
        if CORBA.is_nil(sdo):
            return False

        dfc[0] = sdo._narrow(OpenRTM.DataFlowComponent)
        if CORBA.is_nil(dfc[0]):
            return False

        return True


    ##
    # @if jp
    # @brief Owned ExecutionContext ����ߤ�����
    # @else
    # @brief Stop Owned ExecutionContexts
    # @endif
    #
    # void stopOwnedEC(Member& member);
    def stopOwnedEC(self, member):
        ecs = member._eclist
        for ec in ecs:
            ec.stop()

        return


    ##
    # @if jp
    # @brief Owned ExecutionContext ��ư����
    # @else
    # @brief Start Owned ExecutionContexts
    # @endif
    #
    def startOwnedEC(self, member):
        ecs = member._eclist
        for ec in ecs:
            ec.start()

        return


    ##
    # @if jp
    # @brief DFC �� Organization ���֥������Ȥ�Ϳ����
    # @else
    # @brief Set Organization object to target DFC 
    # @endif
    #
    # void addOrganizationToTarget(Member& member);
    def addOrganizationToTarget(self, member):
        conf = member._config
        if CORBA.is_nil(conf):
            return

        conf.add_organization(self._objref)


    ##
    # @if jp
    # @brief Organization ���֥������Ȥ� DFC����������
    # @else
    # @brief Remove Organization object from a target DFC 
    # @endif
    #
    # void removeOrganizationFromTarget(Member& member)
    def removeOrganizationFromTarget(self, member):
        # get given RTC's configuration object
        conf = member._config
        if CORBA.is_nil(conf):
            return
    
        # set organization to target RTC's conf
        conf.remove_organization(self._pId)


    ##
    # @if jp
    # @brief Composite �� ExecutionContext �� DFC �˥��åȤ���
    # @else
    # @brief Set CompositeRTC's ExecutionContext to the given DFC
    # @endif
    #
    # void addParticipantToEC(Member& member)
    def addParticipantToEC(self, member):
        if CORBA.is_nil(self._ec) or self._ec is None:
            ecs = self._rtobj.get_owned_contexts()
            if len(ecs) > 0:
                self._ec = ecs[0]
            else:
                return
        # set ec to target RTC
        self._ec.add_component(member._rtobj)


    ##
    # @if jp
    # @brief Composite �� ExecutionContext ���� DFC ��������
    # @else
    # @brief Remove participant DFC from CompositeRTC's ExecutionContext
    # @endif
    #
    # void PeriodicECOrganization::removeParticipantFromEC(Member& member)
    def removeParticipantFromEC(self, member):
        if CORBA.is_nil(self._ec) or self._ec is None:
            ecs = self._rtobj.get_owned_contexts()
            if len(ecs) > 0:
                self._ec = ecs[0]
            else:
                return
        self._ec.remove_component(member._rtobj)


    ##
    # @if jp
    # @brief Composite �� ExecutionContext �� DFC �˥��åȤ���
    # @else
    # @brief Set CompositeRTC's ExecutionContext to the given DFC
    # @endif
    #
    # void setCompositeECToTarget(::OpenRTM::DataFlowComponent_ptr dfc);
    #def setCompositeECToTarget(self, dfc):
    #    if CORBA.is_nil(dfc):
    #        return
    #
    #    if CORBA.is_nil(self._ec) or self._ec is None:
    #        ecs = self._rtobj.get_owned_contexts()
    #        if len(ecs) > 0:
    #            self._ec = ecs[0]
    #        else:
    #            return
    #
    #    self._ec.add_component(dfc)

    ##
    # @if jp
    # @brief �ݡ��Ȥ�Ѿ�����
    # @else
    # @brief Delegate given RTC's ports to the Composite
    # @endif
    #
    # void delegatePort(Member& member);
    def delegatePort(self, member):
        exported_ports = self._rtobj.getProperties().getProperty("exported_ports")
      
        # get comp's/ports's profile
        cprof = member._profile
        plist = cprof.port_profiles

        # port delegation
        for prof in plist:
            # port name -> comp_name.port_name
            port_name = cprof.instance_name
            port_name += "."
            port_name += prof.name

            pos = exported_ports.find(port_name)
            if pos == -1:
                continue

            self._rtobj.registerPort(prof.port_ref, "delegate")

    ##
    # @if jp
    # @brief �Ѿ����Ƥ����ݡ��Ȥ�������
    # @else
    # @brief Remove delegated participatns's ports from the composite
    # @endif
    #
    # void removePort(Member& member)
    def removePort(self, member):
        exported_ports = self._rtobj.getProperties().getProperty("exported_ports")
    
        # get comp's/ports's profile
        cprof = member._profile
        plist = cprof.port_profiles
    
        # port delegation
        for prof in plist:
            # port name -> comp_name.port_name
            port_name = cprof.instance_name
            port_name += "."
            port_name += prof.name
        
            pos = exported_ports.find(port_name)
            if pos == -1:
                continue
        
            self._rtobj.deletePort(prof.port_ref)



    class Member:
        def __init__(self, rtobj):
            self._rtobj   = rtobj
            self._profile = rtobj.get_component_profile()
            self._eclist  = rtobj.get_owned_contexts()
            self._config  = rtobj.get_configuration()

            
        def __call__(self, x):
            tmp = x
            tmp.swap(self)
            return self

        
        def swap(self, x):
            rtobj   = x._rtobj
            profile = x._profile
            eclist  = x._eclist
            config  = x._config

            x._rtobj   = self._rtobj
            x._profile = self._profile
            x._eclist  = self._eclist
            x._config  = self._config

            self._rtobj   = rtobj
            self._profile = profile
            self._eclist  = eclist
            self._config  = config

            
##
# @if jp
# @namespace RTC
#
# @brief RT����ݡ��ͥ��
#
# @else
#
# @namespace RTC
#
# @brief RT-Component
#
# @endif
#

##
# @if jp
# @class PeriodicECSharedComposite
# @brief PeriodicECSharedComposite ���饹
#
# �ǡ����ե�����RTComponent�δ��쥯�饹��
# �Ƽ�ǡ����ե�����RTComponent�����������ϡ��ܥ��饹��Ѿ�������Ǽ���
# ���롣
#
# @since 0.4.0
#
# @else
# @class PeriodicECSharedComposite
# @brief PeriodicECSharedComposite class
#
# This is a base class of the data flow type RT-Component.
# Inherit this class when implementing various data flow type RT-Components.
#
# @since 0.4.0
#
# @endif
#
class PeriodicECSharedComposite(OpenRTM_aist.RTObject_impl):


    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param manager �ޥ͡����㥪�֥�������
    #
    # @else
    # @brief Constructor
    #
    # Constructor
    #
    # @param manager Manager object
    #
    # @endif
    #
    def __init__(self, manager):
        OpenRTM_aist.RTObject_impl.__init__(self,manager)
        self._ref = self._this()
        self._objref = self._ref
        self._org = OpenRTM_aist.PeriodicECOrganization(self)
        OpenRTM_aist.CORBA_SeqUtil.push_back(self._sdoOwnedOrganizations,
                                             self._org.getObjRef())

        self._members = [[]]
        self.bindParameter("members", self._members, "", stringToStrVec)
    

    ##
    # @if jp
    # @brief �ǥ��ȥ饯��
    #
    # �ǥ��ȥ饯��
    #
    # @else
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
    # @brief �����
    #
    # �ǡ����ե����� RTComponent �ν������¹Ԥ��롣
    # �ºݤν���������ϡ��ƶ�ݥ��饹��˵��Ҥ��롣
    #
    # @else
    # @brief Initialization
    #
    # Initialization the data flow type RT-Component.
    # Write the actual initialization code in each concrete class.
    #
    # @endif
    #
    def onInitialize(self):
        print "number of member: " , len(self._members[0])

        mgr = OpenRTM_aist.Manager.instance()

        comps = mgr.getComponents()
        for comp in comps:
            print comp.getInstanceName()


        sdos = []
        for member in self._members[0]:
            print "member: ", member
            rtc = mgr.getComponent(member)

            if rtc is None:
                print "no RTC found: ", member
                continue

            print "RTC found: ", rtc.getInstanceName()
            sdo = rtc.getObjRef()
            if CORBA.is_nil(sdo):
                continue

            OpenRTM_aist.CORBA_SeqUtil.push_back(sdos, sdo)
            print "rtc added to list"
    
        try:
            self._org.set_members(sdos)
        except:
            print "exception cought"

        return RTC.RTC_OK


    def onActivated(self, exec_handle):
        ecs = self.get_owned_contexts()
        sdos = self._org.get_members()

        for sdo in sdos:
            rtc = sdo._narrow(RTC.RTObject)
            ecs[0].activate_component(rtc)

        print "num of mem:", len(self._members[0])

        return RTC.RTC_OK


    def onDeactivated(self, exec_handle):
        ecs = self.get_owned_contexts()
        sdos = self._org.get_members()

        for sdo in sdos:
            rtc = sdo._narrow(RTC.RTObject)
            ecs[0].deactivate_component(rtc)

        return RTC.RTC_OK


    def onReset(self, exec_handle):
        ecs = self.get_owned_contexts()
        sdos = self._org.get_members()

        for sdo in sdos:
            rtc = sdo._narrow(RTC.RTObject)
            ecs[0].reset_component(rtc)

        return RTC.RTC_OK


    def onFinalize(self):
        self._org.removeAllMembers()
        return RTC.RTC_OK


    
def PeriodicECSharedCompositeInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=periodicecsharedcomposite_spec)
    manager.registerFactory(profile,
                            OpenRTM_aist.PeriodicECSharedComposite,
                            OpenRTM_aist.Delete)
