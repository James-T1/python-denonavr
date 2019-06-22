#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module provides state information and some control of an
`Denon AVR 2112CI or AVR-X3400H` device over a network connection."""
#   2112ci may need to change dynamic volume code to old commented out code

import argparse
import logging
import telnetlib

import yaml
from flask import Flask, jsonify

# Setup for your Denon's IP address.  Recommend to set a static DHCP address for it in your router.
CONFIG = {
    "host": "192.168.1.133",
    "port": "23",
    "timeout": 5
}

# Don't let the user hit us multiple times before a command has completed
IN_PROGRESS = False
DYNEQ_LAST_SETTING = -99
LAST_TOGGLED_UP = True
VOLUME_PREV_LEVEL = -99

APP = Flask(__name__)

def _is_valid_input_source(source):
    """Only allow special sources.

    :param (str) source: name of source
    :return:
    """
    return source in ["DVD", "BD", "GAME", "SAT/CBL"]


def _convert_input_source(source):
    """Convert input source to proper denon conform name.

    :param source: name of the source
    :return: source name adapted to protocol
    """

    source = source.upper()
    if "SATCBL" in source:
        source = "SAT/CBL"
    return source


def execute(command, config):
    """Execute telnet commands on DENON host.

    :param (str) command: see public protocol
    :param (dict) config: device config

    :return: result from avr telnet connection.
    """
    tn_con = telnetlib.Telnet(config["host"], config["port"], config["timeout"])

    try:
        tn_con.write(("%s\r" % command).encode("ascii"))
        read = str(tn_con.read_until("\r".encode('ascii')))
        read = read.replace("b'", "").replace("\\r'", "")
        return read

    except OSError:
        logging.exception("Exception occurred during writing of telnet")
        return "ERROR"
    finally:
        tn_con.close()

@APP.route('/power/state', methods=['GET'])
def get_power_state():
    """Get current power state.

    :return: current power state PWON/PWStandby
    """
    return jsonify(power=execute("PW?", CONFIG))


@APP.route('/power/turnon', methods=['GET'])
def turn_on():
    """Turn on System.

    :return: success
    """
    if execute("PW?", CONFIG) == "PWON":
        return jsonify(power="PWON")
    return jsonify(power=execute("PWON", CONFIG))


@APP.route('/power/turnoff', methods=['GET'])
def turn_off():
    """Turn off System.

    :return: success
    """
    if execute("PW?", CONFIG) == "PWSTANDBY":
        return jsonify(power="PWSTANDBY")
    return jsonify(power=execute("PWSTANDBY", CONFIG))


@APP.route('/input/state', methods=['GET'])
def get_input_state():
    """ Get current Input Source.

    :return: success
    """
    return jsonify(power=execute("SI?", CONFIG))


@APP.route('/input/switch/<source_id>', methods=['GET'])
def switch_input_source(source_id):
    """Set new Input Source.

    :param source_id:
    :return: success
    """
    success = False
    source = _convert_input_source(source_id)
    current_source = execute("SI?", CONFIG).replace("SI", "")
    print("Requested Source: " + source + " Current SRC: " + current_source)

    if source in current_source:
        print("Not executing src change")
        success = True
    elif not _is_valid_input_source(source):
        success = False
    else:
        execute("SI" + source, CONFIG)
        success = True

    return jsonify(succes=success)


@APP.route('/volume/level', methods=['GET'])
def get_volume_level():
    """Get the volume level on volume/level.

    :return: Get current volume level
    """
    return jsonify(level=execute("MV?", CONFIG).replace("MV", ""))


@APP.route('/volume/set/<int:level_id>', methods=['GET'])
def set_volume_level(level_id):
    """Set Volume level on /volume/set/*.

    :param level_id: db level in the range of 0-60DB
    :return: success
    """
    success = False
    if 0 <= level_id <= 60:
        execute("MV%02d" % level_id, CONFIG)
        success = True
    return jsonify(success=success)

    
# James add 
    
# Toggle volume up/down by 5dB for shows that like to jump all over the place in volume

@APP.route('/volume/toggle', methods=['GET'])
def volume_toggle():
    """Set Volume level on /volume/set/*.

    :param level_id: toggle volume
    :return: success
    """
    #+15.5dB = 955
    #+15dB = 95
    #  0dB = 80
    #-15dB = 65
    #-40dB = 40
    #-40.5dB = 395
    #So... if it's >100, then divide by 10.
    success = False
    volume_cur_level = execute("MV?", CONFIG).replace("MV", "")
    if volume_cur_level > 100:
        volume_cur_level = volume_cur_level / 10.0
    
    print(volume_cur_level)
    # if VOLUME_PREV_LEVEL != volume_cur_level:
        # LAST_TOGGLED_UP = True
    # if LAST_TOGGLED_UP:
        # volume_new_level = volume_cur_level - 5
        # LAST_TOGGLED_UP = False
    # else:
        # volume_new_level = volume_cur_level + 5
        # LAST_TOGGLED_UP = True

    # # Truncate down to 2 digits by converting to int
    # volume_new_level = int(volume_new_level)
    # execute("MV%02d" % volume_new_level, CONFIG)
    success = True
    #VOLUME_PREV_LEVEL = volume_new_level
    return jsonify(success=success)


@APP.route('/volume/up3', methods=['GET'])
def volume_up3():
    """Set Volume level on /volume/set/*.

    :param level_id: toggle volume
    :return: success
    """
    #+15.5dB = 955
    #+15dB = 95
    #  0dB = 80
    #-15dB = 65
    #-40dB = 40
    #-40.5dB = 395
    #So... if it's >100, then divide by 10.
    success = False
    volume_cur_level = int(execute("MV?", CONFIG).replace("MV", ""))
    if volume_cur_level > 100:
        volume_cur_level = volume_cur_level / 10.0
    print(volume_cur_level)
    volume_new_level = volume_cur_level + 3
    # Truncate down to 2 digits by converting to int
    volume_new_level = int(volume_new_level)
    execute("MV%02d" % volume_new_level, CONFIG)
    success = True
    #VOLUME_PREV_LEVEL = volume_new_level
    return jsonify(success=success)

@APP.route('/volume/down3', methods=['GET'])
def volume_down3():
    """Set Volume level on /volume/set/*.

    :param level_id: toggle volume
    :return: success
    """
    #+15.5dB = 955
    #+15dB = 95
    #  0dB = 80
    #-15dB = 65
    #-40dB = 40
    #-40.5dB = 395
    #So... if it's >100, then divide by 10.
    success = False
    volume_cur_level = int(execute("MV?", CONFIG).replace("MV", ""))
    if volume_cur_level > 100:
        volume_cur_level = volume_cur_level / 10.0
    print(volume_cur_level)
    volume_new_level = volume_cur_level - 3
    # Truncate down to 2 digits by converting to int
    volume_new_level = int(volume_new_level)
    execute("MV%02d" % volume_new_level, CONFIG)
    success = True
    #VOLUME_PREV_LEVEL = volume_new_level
    return jsonify(success=success)
    
@APP.route('/ps/toggle_reflev', methods=['GET'])
def toggle_reflev():
    """Toggle Audyssey DynEq and Reflev.
    :return: success
    """
    success = False
    global IN_PROGRESS
    if IN_PROGRESS:
        return jsonify(succes=success)
        print("Ignoring successive request...")
    else:
        IN_PROGRESS = True
    
    print("Requested DynEQ Reference Level toggle...")

    #dyneq_status = execute("PSDYNEQ ?", CONFIG)
    #reflev_setting = execute("PSREFLEV ?", CONFIG)
    #if dyneq_status == "PSDYNEQ OFF":
    #    execute("PSDYNEQ ON", CONFIG)
    #    execute("PSREFLEV 0", CONFIG)
    #elif reflev_setting == "PSREFLEV 0":
    #    execute("PSREFLEV 5", CONFIG)
    #elif reflev_setting == "PSREFLEV 5":
    #    execute("PSREFLEV 10", CONFIG)
    #elif reflev_setting == "PSREFLEV 10":
    #    execute("PSREFLEV 15", CONFIG)
    #elif reflev_setting == "PSREFLEV 15":
    #    execute("PSDYNEQ OFF", CONFIG)
    global DYNEQ_LAST_SETTING
    # Check to see if we're using default setting.  If so find out where we are first.
    if DYNEQ_LAST_SETTING == -99:
        print("  Updating previous values from Denon amp...")
        dyneq_status = execute("PSDYNEQ ?", CONFIG)
        reflev_setting = execute("PSREFLEV ?", CONFIG)
        if dyneq_status == "PSDYNEQ OFF":
            DYNEQ_LAST_SETTING = -1
        elif reflev_setting == "PSREFLEV 0":
            DYNEQ_LAST_SETTING = 0
        elif reflev_setting == "PSREFLEV 5":
            DYNEQ_LAST_SETTING = 5
        elif reflev_setting == "PSREFLEV 10":
            DYNEQ_LAST_SETTING = 10
        elif reflev_setting == "PSREFLEV 15":
            DYNEQ_LAST_SETTING = 15
    # Toggle the dyneq/reference level settings
    print("  Performing the requested toggle based on current state:  {}".format(DYNEQ_LAST_SETTING))
    if DYNEQ_LAST_SETTING == -1:
        # Must turn DynEq on first or Denon will hang when you try to change the reference level.
        execute("PSDYNEQ ON", CONFIG)
        execute("PSREFLEV 0", CONFIG)
        DYNEQ_LAST_SETTING = 0
    elif DYNEQ_LAST_SETTING == 0:
        execute("PSREFLEV 5", CONFIG)
        DYNEQ_LAST_SETTING = 5
    elif DYNEQ_LAST_SETTING == 5:
        execute("PSREFLEV 10", CONFIG)
        DYNEQ_LAST_SETTING = 10
    elif DYNEQ_LAST_SETTING == 10:
        execute("PSREFLEV 15", CONFIG)
        DYNEQ_LAST_SETTING = 15
    elif DYNEQ_LAST_SETTING == 15:
        execute("PSDYNEQ OFF", CONFIG)
        DYNEQ_LAST_SETTING = -1
    success = True
    IN_PROGRESS = False
    print("  Completed DynEQ Reference Level toggle request.")
    return jsonify(succes=success)

@APP.route('/ps/toggle_dynvolume', methods=['GET'])
def toggle_dynvolume():
    """Toggle Audyssey Dynamic Volume
    :return: success
    """
    success = False
    print("Requested Dynamic Volume toggle...")

    dynvol_setting = execute("PSDYNVOL ?", CONFIG)
    if dynvol_setting == "PSDYNVOL OFF":
        execute("PSDYNVOL LIT", CONFIG)
        # 2112ci = NGT   (Midnight)
        # x3500 = HEV    (High/Evening?)
    elif dynvol_setting == "PSDYNVOL LIT":
        execute("PSDYNVOL MED", CONFIG)
        # 2112ci = EVE    (Evening)
        # x3500 = MED    (Medium)
    elif dynvol_setting == "PSDYNVOL MED":
        execute("PSDYNVOL HEV", CONFIG)
        # 2112ci = DAY   (Day)
        # X3500 = LIT   (Lite)
    elif dynvol_setting == "PSDYNVOL HEV":
        execute("PSDYNVOL OFF", CONFIG)
    success = True
    print("  Completed Dynamic Volume toggle request.")
    return jsonify(succes=success)

# Future ideas:
#   Toggle MultEQ setting
#   Toggle bass level or subwoofer level
    
def _read_config(config_file_path):
    """ Parse Config File from yaml file. """
    global CONFIG
    config_file = open(config_file_path, 'r')
    config = yaml.load(config_file)
    config_file.close()
    CONFIG = config["denon"]

def main():
    """ Set up the server."""
    parser = argparse.ArgumentParser(description='AVR Telnet Server')
    parser.add_argument('-p', '--port', type=int,
                        help='listen port', default=5557)
    parser.add_argument('-c', '--config', type=str, help='config')
    args = parser.parse_args()

    if args.config:
        _read_config(args.config)

    APP.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
