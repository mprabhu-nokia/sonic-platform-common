#
# module_base.py
#
# Base class for implementing a platform-specific class with which
# to interact with a module (as used in a modular chassis) SONiC.
#

import sys
from . import device_base


class ModuleBase(device_base.DeviceBase):
    """
    Base class for interfacing with a module (supervisor module, line card
    module, etc. (applicable for a modular chassis) 
    """
    # Device type definition. Note, this is a constant.
    DEVICE_TYPE = "module"

    # Possible card types
    MODULE_TYPE_SUPERVISOR = "SUPERVISOR"
    MODULE_TYPE_LINE    = "LINE-CARD"
    MODULE_TYPE_FABRIC  = "FABRIC-CARD"

    # Possible card status
    #Module state is Empty if no module is inserted in the slot
    MODULE_STATUS_EMPTY   = "Empty"
    #Module state if Offline if powered down. This is also the admin-down state.
    MODULE_STATUS_OFFLINE = "Offline"
    #Module state is Present when it is powered up, but not fully functional.
    MODULE_STATUS_PRESENT = "Present"
    #Module state is Present when it is powered up, but entered a fault state.
    #Module is not able to go Online.
    MODULE_STATUS_FAULT   = "Fault"
    #Module state is Online when fully operational
    MODULE_STATUS_ONLINE  = "Online"

    # List of ComponentBase-derived objects representing all components
    # available on the module
    _component_list = None

    # List of FanBase-derived objects representing all fans
    # available on the module 
    _fan_list = None

    # List of PsuBase-derived objects representing all power supply units
    # available on the module
    _psu_list = None

    # List of ThermalBase-derived objects representing all thermals
    # available on the module
    _thermal_list = None

    # List of SfpBase-derived objects representing all sfps
    # available on the module
    _sfp_list = None

    def __init__(self):
        self._component_list = []
        self._fan_list = []
        self._psu_list = []
        self._thermal_list = []
        self._sfp_list = []

    def get_base_mac(self):
        """
        Retrieves the base MAC address for the module

        Returns:
            A string containing the MAC address in the format
            'XX:XX:XX:XX:XX:XX'
        """
        raise NotImplementedError

    def get_system_eeprom_info(self):
        """
        Retrieves the full content of system EEPROM information for the module 

        Returns:
            A dictionary where keys are the type code defined in
            OCP ONIE TlvInfo EEPROM format and values are their corresponding
            values.
            Ex. { ‘0x21’:’AG9064’, ‘0x22’:’V1.0’, ‘0x23’:’AG9064-0109867821’,
                  ‘0x24’:’001c0f000fcd0a’, ‘0x25’:’02/03/2018 16:22:00’,
                  ‘0x26’:’01’, ‘0x27’:’REV01’, ‘0x28’:’AG9064-C2358-16G’}
        """
        raise NotImplementedError

    def get_name(self):
        """
        Retrieves the name of the module prefixed by SUPERVISOR, LINE-CARD,
        FABRIC-CARD

        Returns:
            string: A string providing the name of the card prefixed by one of the
            MODULE_TYPE_SUPERVISOR, MODULE_TYPE_LINE, MODULE_TYPE_FABRIC followed by
            an index.
            Ex. A Chassis having 1 control-card, 4 line-cards and 6 fabric-cards
            can provide names SUPERVISOR0, LINE-CARD0 to LINE-CARD3,
            FABRIC-CARD0 to FABRIC-CARD5
        """
        raise NotImplementedError

    def get_description(self):
        """
        Retrieves the platform vendor's product description of the module

        Returns:
            string: A string providing the product description of the module. This
            is vendor specific.
        """
        raise NotImplementedError

    def get_slot(self):
        """
        Retrieves the platform vendor's slot number of the module

        Returns:
            An integer, indicating the slot number in the chassis
        """
        raise NotImplementedError

    def get_type(self):
        """
        Retrieves the type of the module.

        Returns:
            string: A string providing the module-type. Supported values are
            MODULE_TYPE_SUPERVISOR, MODULE_TYPE_LINE, MODULE_TYPE_FABRIC
        """
        raise NotImplementedError

    def get_status(self):
        """
        Retrieves the status of the card

        Returns:
            string: A string providing the status of the module. Support values
            are MODULE_STATUS_EMPTY, MODULE_STATUS_OFFLINE, MODULE_STATUS_FAULT,
            MODULE_STATUS_PRESENT, MODULE_STATUS_ONLINE
        """
        raise NotImplementedError

    def reboot(self):
        """
        Request to reboot the module

        Returns:
            bool: True if the request has been issued successfully, False if not
        """
        raise NotImplementedError

    def set_admin_state(self, up):
        """
        Request to keep the card in administratively up/down state.
        The down state will power down the module and the status should show
        MODULE_STATUS_OFFLINE.
        The up state will take the module to MODULE_STATUS_PRESENT,
        MODULE_STATUS_FAULT or MODULE_STAUS_ONLINE states.

        Returns:
            bool: True if the request has been issued successfully, False if not
        """
        raise NotImplementedError

    ##############################################
    # Component methods
    ##############################################

    def get_num_components(self):
        """
        Retrieves the number of components available on this module

        Returns:
            An integer, the number of components available on this module
        """
        return len(self._component_list)

    def get_all_components(self):
        """
        Retrieves all components available on this module

        Returns:
            A list of objects derived from ComponentBase representing all components
            available on this module
        """
        return self._component_list

    def get_component(self, index):
        """
        Retrieves component represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the component to retrieve

        Returns:
            An object dervied from ComponentBase representing the specified component
        """
        component = None

        try:
            component = self._component_list[index]
        except IndexError:
            sys.stderr.write("Component index {} out of range (0-{})\n".format(
                             index, len(self._component_list)-1))

        return component

    ##############################################
    # Fan module methods
    ##############################################

    def get_num_fans(self):
        """
        Retrieves the number of fan modules available on this module

        Returns:
            An integer, the number of fan modules available on this module
        """
        return len(self._fan_list)

    def get_all_fans(self):
        """
        Retrieves all fan modules available on this module 

        Returns:
            A list of objects derived from FanBase representing all fan
            modules available on this module 
        """
        return self._fan_list

    def get_fan(self, index):
        """
        Retrieves fan module represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the fan module to
            retrieve

        Returns:
            An object dervied from FanBase representing the specified fan
            module
        """
        fan = None

        try:
            fan = self._fan_list[index]
        except IndexError:
            sys.stderr.write("Fan index {} out of range (0-{})\n".format(
                             index, len(self._fan_list)-1))

        return fan

    ##############################################
    # PSU module methods
    ##############################################

    def get_num_psus(self):
        """
        Retrieves the number of power supply units available on this module 

        Returns:
            An integer, the number of power supply units available on this
            module 
        """
        return len(self._psu_list)

    def get_all_psus(self):
        """
        Retrieves all power supply units available on this module 

        Returns:
            A list of objects derived from PsuBase representing all power
            supply units available on this module 
        """
        return self._psu_list

    def get_psu(self, index):
        """
        Retrieves power supply unit represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the power supply unit to
            retrieve

        Returns:
            An object dervied from PsuBase representing the specified power
            supply unit
        """
        psu = None

        try:
            psu = self._psu_list[index]
        except IndexError:
            sys.stderr.write("PSU index {} out of range (0-{})\n".format(
                             index, len(self._psu_list)-1))

        return psu

    ##############################################
    # THERMAL methods
    ##############################################

    def get_num_thermals(self):
        """
        Retrieves the number of thermals available on this module 

        Returns:
            An integer, the number of thermals available on this module 
        """
        return len(self._thermal_list)

    def get_all_thermals(self):
        """
        Retrieves all thermals available on this module 

        Returns:
            A list of objects derived from ThermalBase representing all thermals
            available on this module 
        """
        return self._thermal_list

    def get_thermal(self, index):
        """
        Retrieves thermal unit represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the thermal to
            retrieve

        Returns:
            An object dervied from ThermalBase representing the specified thermal
        """
        thermal = None

        try:
            thermal = self._thermal_list[index]
        except IndexError:
            sys.stderr.write("THERMAL index {} out of range (0-{})\n".format(
                             index, len(self._thermal_list)-1))

        return thermal

    ##############################################
    # SFP methods
    ##############################################

    def get_num_sfps(self):
        """
        Retrieves the number of sfps available on this module 

        Returns:
            An integer, the number of sfps available on this module 
        """
        return len(self._sfp_list)

    def get_all_sfps(self):
        """
        Retrieves all sfps available on this module 

        Returns:
            A list of objects derived from PsuBase representing all sfps 
            available on this module 
        """
        return self._sfp_list

    def get_sfp(self, index):
        """
        Retrieves sfp represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the sfp to retrieve

        Returns:
            An object dervied from SfpBase representing the specified sfp
        """
        sfp = None

        try:
            sfp = self._sfp_list[index]
        except IndexError:
            sys.stderr.write("SFP index {} out of range (0-{})\n".format(
                             index, len(self._sfp_list)-1))

        return sfp

    def get_change_event(self, timeout=0):
        """
        Returns a nested dictionary containing all devices which have
        experienced a change in this module

        Args:
            timeout: Timeout in milliseconds (optional). If timeout == 0,
                this method will block until a change is detected.

        Returns:
            (bool, dict):
                - True if call successful, False if not;
                - A nested dictionary where key is a device type,
                  value is a dictionary with key:value pairs in the format of
                  {'device_id':'device_event'}, 
                  where device_id is the device ID for this device and
                        device_event,
                             status='1' represents device inserted,
                             status='0' represents device removed.
                  Ex. {'fan':{'0':'0', '2':'1'}, 'sfp':{'11':'0'}}
                      indicates that fan 0 has been removed, fan 2
                      has been inserted and sfp 11 has been removed.
        """
        raise NotImplementedError

