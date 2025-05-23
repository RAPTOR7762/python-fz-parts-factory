#!/usr/bin/env python3

import partsfactory_constants as constants
import getopt
import os
import os.path
import sys
import logging
from datetime import date
from PySide6.QtCore import QCryptographicHash, QUuid, QByteArray


def convert(s):

    # since str doesn't have .toLatin1() unlike Qstring (and PySide2 doesn't
    # have Qstring but uses str instead), use a function to do the conversion.
    # From https://stackoverflow.com/questions/51186075/
    # python-convert-this-utf8-string-to-latin1

    r = ''
    for c in s:
        try:
            c.encode('latin-1')
        except UnicodeEncodeError:
            c = unicodedata.normalize('NFKD', c).encode(
                'latin-1', 'ignore').decode('latin-1')
        r += c
    return r


def get_uuid():

    # Copied from TextUtils::getRandText() in Fritzing app in
    # src/utils/textutils.cpp and modified to run under PySide2

    uuid = QUuid.createUuid().toString()

    # since str doesn't have .toLatin1() unlike Qstring, use a function
    # to do the conversion.

    uuid = convert(uuid)

    # then create the uuid string and return it.
    # Conversion from QByteArray to string from:
    # https://stackoverflow.com/questions/57663191/
    # how-to-convert-a-qbytearray-to-a-python-string-in-pyside2

    uuid_out = str(QCryptographicHash.hash(
                  uuid.encode(), QCryptographicHash.Md4).toHex(), 'utf-8')

    return uuid_out


def write_file(filename, data):

    # Write data to filename.

    # At the moment ignore if the file exists and overwrite it.

    #    if os.path.exists(fzp_filename) :

    #        print ('Error: File {0:s} already exists.\n'.format(fzp_filename))

    #        exit(1)

    # breakpoint()

    try:

        file = open(filename, 'w')

    except os.error as e:

        print("\nError: Can not open file\n\n\'{0:s}\'\n\nto write {1:s}"
              " ({2:d})\n".format(e.filename, e.strerror, e.errno),
              file=sys.stderr)
        exit(1)

    for line in data:

        # add newline to pretty print the xml.

        file.write(line + "\n")

    try:

        file.close()

    except os.error as e:

        print("\nError: Can not open file\n\n\'{0:s}\'\n\nto write {1:s}"
              " ({2:d})\n".format(e.filename, e.strerror, e.errno),
              file=sys.stderr)
        exit(1)


def create_pin_xml(fzp, connector, pcb_type):

    # Create the xml for a single pin in fzp then return it.

    fzp.append("      <connector id=\"connector{0:d}\" type=\"male\""
               " name=\"Pin {1:d}\">".format(connector, connector + 1))

    fzp.append("        <description>Pin {0:d}</description>".format
               (connector + 1))

    fzp.append("        <views>")

    fzp.append("          <breadboardView>")

    fzp.append("            <p layer=\"breadboard\" svgId=\"connector{0:d}"
               "pin\"/>".format(connector))

    fzp.append("          </breadboardView>")

    fzp.append("          <schematicView>")

    fzp.append("            <p layer=\"schematic\" svgId=\"connector{0:d}pin\""
               " terminalId=\"connector{0:d}terminal\"/>".format(connector))

    fzp.append("          </schematicView>")

    fzp.append("          <pcbView>")

    if pcb_type == constants.SMD:

        # end up with '       <p svgId="connector0pad layer="copper1"/>
        # (where 0 is the value of connector) in the xml.

        fzp.append("            <p layer=\"copper1\" svgId=\""
                   "connector{0:d}pad\"/>".format(connector))

    else:

        # end up with '       <p svgId="connector0pin layer="copper0"/>
        #             '       <p svgId="connector0pin layer="copper1"/>
        # (where 0 is the value of connector) in the xml.

        fzp.append("            <p layer=\"copper0\" svgId=\""
                   "connector{0:d}pin\"/>".format(connector))

        fzp.append("            <p layer=\"copper1\" svgId=\""
                   "connector{0:d}pin\"/>".format(connector))

    fzp.append("          </pcbView>")

    fzp.append("        </views>")

    fzp.append("      </connector>")

    return (fzp)


def create_fzp(part_type, rows, columns, pitch, pcb_type, pin_order, pad_type,
               color, version):

    # Create the fzpxml file for the part.

    uuid = get_uuid()

    # Create the fzp file name from the parameters

    if part_type == "male-header":

        label = "J"

        family = "Generic header"

        form = "(male)"

        if rows == 0 or columns == 0:

            # If either rows or columns is 0 flag an error.

            print("Error: rows and columns must have a value > 0",
                  file=sys.stderr)

            exit(1)

        if columns == 1:

            # If rows is 1 overide PinOrder to row as there are no columns

            pin_order = "row"

        if pcb_type == constants.SMD:

            moduleid = ('Generic-male-header-'
                        + str(rows)
                        + 'pins-'
                        + str(columns)
                        + 'rows-'
                        + str(pitch)
                        + "-pitch-smd-pinorder-"
                        + pin_order
                        + "-"
                        + pad_type
                        + "-"
                        + color
                        + "_"
                        + uuid
                        + "_"
                        + str(version))

            title = ('Generic male header SMD - '
                     + str(rows)
                     + ' pins '
                     + str(columns)
                     + 'columns '
                     + str(pitch)
                     + " pitch smd pin order "
                     + pin_order
                     + " "
                     + pad_type
                     + " "
                     + color)
            package = "SMD"

        elif pcb_type == constants.THT:

            moduleid = ('Generic-male-header-'
                        + str(rows)
                        + 'pins-'
                        + str(columns)
                        + 'columns-'
                        + str(pitch)
                        + "-pitch-tht-pinorder-"
                        + pin_order
                        + "-"
                        + pad_type
                        + "-"
                        + color
                        + "_"
                        + uuid
                        + "_"
                        + str(version))

            title = ('Generic male header - '
                     + str(rows)
                     + ' pins '
                     + str(columns)
                     + 'rows '
                     + str(pitch)
                     + " pitch tht pin order "
                     + pin_order
                     + " "
                     + pad_type
                     + " "
                     + color)

            package = "THT"

        else:

            return "1 NotImplmented yet"

    else:

        return "2 NotImplmented yet"

    fzp = []
    fzp.append("<?xml version='1.0' encoding='UTF-8'?>")
    fzp.append(
        "<module  moduleId=\"{0:s}\" fritzingVersion=\"1.0.3\">".format(
                                                                 moduleid))
    fzp.append("  <version>1</version>")
    fzp.append("  <author>Python Part-o-matic</author>")
    fzp.append("  <title>{0:s}</title>".format(title))
    fzp.append("  <label>{0:s}</label>".format(label))

    now = date.today()
    today = now.strftime("%a %b %d %Y")

    fzp.append("  <date>{0:s}</date>".format(today))
    fzp.append("  <tags/>")
    fzp.append("  <properties>")
    fzp.append(
        "  <property name=\"family\">{0:s}</property>".format(family))
    fzp.append(
        "    <property name=\"PartType\">{0:s}</property>".format(part_type))
    fzp.append(
        "    <property name=\"Rows\">{0:d}</property>".format(rows))
    fzp.append(
        "    <property name=\"Columns\">{0:d}</property>".format(columns))
    fzp.append(
        "    <property name=\"Pitch\">{0:f}</property>".format(pitch))
    fzp.append(
        "    <property name=\"Pcbtype\">{0:s}</property>".format(pcb_type))
    fzp.append(
        "    <property name=\"Pinorder\">{0:s}</property>".format(pin_order))
    fzp.append(
        "    <property name=\"Padtype\">{0:s}</property>".format(pad_type))
    fzp.append(
        "    <property name=\"color\">{0:s}</property>".format(color))
    fzp.append(
        "    <property name=\"Form\">{0:s}</property>".format(form))
    fzp.append(
        "    <property name=\"version\">{0:d}</property>".format(version))
    fzp.append(
        "    <property name=\"package\">{0:s}</property>".format(package))
    fzp.append("    <property name=\"mn\"></property>")
    fzp.append("    <property name=\"layer\"></property>")
    fzp.append("    <property name=\"part number\"></property>")
    fzp.append("    <property name=\"mpn\"></property>")
    fzp.append("    <property name=\"variant\">variant 1</property>")
    fzp.append("  </properties>")
    fzp.append("  <description>{0:s}</description>".format(title))
    fzp.append("  <views>")
    fzp.append("    <iconView>")
#    fzp.append(
#        "      <layers image=\"breadboard/{0:s}.breadboard.svg\">".format(
#                                                                    moduleid))
#
# For testing use a fixed file test_breadboard.svg
    fzp.append("      <layers image=\"breadboard/test_breadboard.svg\">")
    fzp.append("        <layer layerId=\"icon\"/>")
    fzp.append("      </layers>")
    fzp.append("    </iconView>")
    fzp.append("    <breadboardView>")
#    fzp.append(
#        "      <layers image=\"breadboard/{0:s}.breadboard.svg\">".format(
#                                                                    moduleid))
#
# For testing use a fixed file test_breadboard.svg
    fzp.append("      <layers image=\"breadboard/test_breadboard.svg\">")
    fzp.append("        <layer layerId=\"breadboard\"/>")
    fzp.append("      </layers>")
    fzp.append("    </breadboardView>")
    fzp.append("    <schematicView>")
#    fzp.append(
#        "      <layers image=\"schematic/{0:s}.schematic.svg\">".format(
#                                                                    moduleid))
#
# For testing use a fixed file test_schematic.svg
    fzp.append("      <layers image=\"schematic/test_schematic.svg\">")
    fzp.append("        <layer layerId=\"schematic\"/>")
    fzp.append("      </layers>")
    fzp.append("    </schematicView>")
    fzp.append("    <pcbView>")
#    fzp.append("      <layers image=\"pcb/{0:s}.pcb.svg\">".format(
#                                                                moduleid))
#
# For testing use a fixed file test_pcb.svg
    fzp.append("      <layers image=\"pcb/test_pcb.svg\">")
    fzp.append("        <layer layerId=\"silkscreen\"/>")

    if package == "THT":

        # No copper0 layer for SMD parts.

        fzp.append("        <layer layerId=\"copper0\"/>")

    fzp.append("        <layer layerId=\"copper1\"/>")
    fzp.append("       </layers>")
    fzp.append("     </pcbView>")
    fzp.append("  </views>")
    fzp.append("  <connectors>")

    connector = 0

    for column in range(0, columns):

        for row in range(0, rows):

            fzp = create_pin_xml(fzp, connector, pcb_type)
            connector += 1

    fzp.append("  </connectors>")

    fzp.append("</module>")

    fzp_filename = 'part.test_fzp.fzp'

    # breakpoint()

    write_file(fzp_filename, fzp)

    return moduleid


def s_x(parm, row, pitch, stroke_width=0):

    # scale and move (if needed) this pin in x. Round the result to
    # 2 digit after the decimal to avoid 35.40000001. Drawing units
    # are 1/1000th of an inch and that is fine for our purposes.

# *** remove me later ***
    print("s_x parm {0:f} row {1:d} pitch {2:f}".format(parm, row, pitch))

    # otherwise do both move and scale. First calculate the offset of
    # the pitch converted to 1/1000 of an inch times the row - 1 (because
    # the row needs to start at 0 not 1 which it does now.)

#    offset = float(pitch) * float(constants.PITCH_TO_THOU) * float(row - 1)
    offset = pitch * constants.PITCH_IN_THOU * (row - 1)

# *** remove me later ***
    print("s_x offset {0:f}".format(offset))

    # Than add the parameter multiplied by the pitch in 1/1000 of an inch
    # and add it to the offset to create the parameter to return. 

    scaled_param = round((parm * pitch) + offset + stroke_width, 4)

# *** remove me later ***
    print("s_x row {0:d}: return {1:s}".format(row, str(scaled_param)))

    return str(scaled_param)


def s_y(parm, column, pitch):

    # scale and move (if needed) this pin in y. Round the result to
    # 2 digits after the decimal to avoid 35.40000001. Drawing units
    # are 1/1000th of an inch and that is fine for our purposes.

# *** remove me later ***
    print("s_y parm {0:f} column {1:d} pitch {2:f}".format(parm, column, pitch))

    # otherwise do both move and scale. First calculate the offset of
    # the pitch converted to 1/1000 of an inch times the row. Need to 
    # subract 1 from the column to start at position 0 rather than 1.

    offset = pitch * constants.PITCH_IN_THOU * (column - 1)

    # Than add the parameter multiplied by the pitch in 1/1000 of an inch
    # and add it to the offset to create the parameter to return. 

    scaled_param = round((parm * pitch) + offset, 4)

# *** remove me later ***
    print("s_y column {0:d}: return {1:s}".format(column, str(scaled_param)))

    return str(scaled_param)


def s_r_y(parm, columns, column, pitch):

    # scale and move (if needed) this pin in y, but in the reverse direction
    # i.e. s_y above increases the columns in y, this function decreases
    # the columns in y so we can start pin0 at the bottom of an svg and have
    # the next column be above (rather than below) the lower column. This is
    # needed for correct alignment in breadboard and pcb (but not schematic
    # which uses s_y()!)

    # This will change the sequence 1, 2, 3, 4 in column to the sequence
    # 4, 3, 2, 1 which will place the item where we want it in the svg.

    local_column = columns - column

    # otherwise do both move and scale. First calculate the offset of the
    # pitch converted to 1/1000 of an inch times the column.

    offset = pitch * constants.PITCH_IN_THOU * local_column

    # Than add the parameter multiplied by the pitch in 1/1000 of an inch 
    # and add it to the offset to create the parameter to return (so the 
    # parameter only gets scaled and added once rather than for every
    # column!). 

    scaled_param = round((parm * pitch) + offset, 4)

# *** remove me later ***
    print("s_r_y column {0:d}: return {1:s}".format(local_column, str(scaled_param)))

    return str(scaled_param)


def male_outline(svg, connector, columns, row, column, pitch, color):

    # Generate an outline path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

    svg.append("    <path")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"outline" + str(connector) + "\"")

    # Then create the path, moving and scaling the coordinates as
    # we go. The first y needs to use s_r_y() to correctly align the
    # absolute start value, after that the moves are relative and don't need
    # that translation.

#*** remove me later ***
#    print("Start outline row {0:d}".format(row))

    svg.append("      d=\""
               + "M " + s_x(0, row, pitch) + ","
               + s_r_y(3.83, columns, column, pitch)
               + " l " + s_x(3.83, constants.SCALE_ONLY, pitch)
               + "," + s_y(-3.83, constants.SCALE_ONLY, pitch)
               + " h " + s_x(12.1, constants.SCALE_ONLY, pitch) + " l "
               + s_x(3.83, constants.SCALE_ONLY, pitch)
               + "," + s_y(3.83, constants.SCALE_ONLY, pitch) + " v " 
               + s_x(0, constants.SCALE_ONLY, pitch) + "," 
               + s_y(12.1, constants.SCALE_ONLY, pitch) + " l " 
               + s_x(-3.83, constants.SCALE_ONLY, pitch) + "," 
               + s_y(3.83, constants.SCALE_ONLY, pitch) + " h " 
               + s_y(-12.1, constants.SCALE_ONLY, pitch) + " l " 
               + s_x(-3.83, constants.SCALE_ONLY, pitch) + "," 
               + s_y(-3.83, constants.SCALE_ONLY, pitch) + " z\"")

    # Set the approriate color for the pin.

    svg.append("      fill=\"" + color + "\"")

    svg.append("      stroke-width=\"0\"")

    svg.append("    />")

    return svg


def male_pinleft(svg, connector, columns, row, column, pitch):

    # Generate a pinleft path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

#*** remove me later ***
#    print("Start pinleft row {0:d}".format(row))

    svg.append("    <path")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"pinleft" + str(connector) + "\"")

    # Then create the path, moving and scaling the coordinates as
    # we go. Use s_r_y() for the y start coord after that is
    # relative and doesn't need that translation.

    svg.append("      d=\""
               + "M " + s_x(6, row, pitch) + ","
               + s_r_y(6, columns, column, pitch)
               + " l " + s_x(2, constants.SCALE_ONLY, pitch) + ","
               + s_y(2, constants.SCALE_ONLY, pitch)
               + " v " + s_x(4, constants.SCALE_ONLY, pitch)
               + " l " + s_x(-2, constants.SCALE_ONLY, pitch) + ","
               + s_y(2, constants.SCALE_ONLY, pitch) + " z\"")

    # Set the approriate color for the pin.

    svg.append("      fill=\"#9a916c\"")

    svg.append("      stroke-width=\"0\"")

    svg.append("    />")

    return svg


def male_pintop(svg, connector, columns, row, column, pitch):

    # Generate a pintop path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

#*** remove me later ***
#    print("Start pintop row {0:d}".format(row))

    svg.append("    <path")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"pintop" + str(connector) + "\"")

    # Then create the path, moving and scaling the coordinates as
    # we go. Use s_r_y() for the absolute y start coord after that is
    # relative and doesn't need that translation.

    svg.append("      d=\""
               + "M " + s_x(6, row, pitch) + "," 
               + s_r_y(6, columns, column, pitch)
               + " h " + s_x(8, constants.SCALE_ONLY, pitch)
               + " l " + s_x(-2, constants.SCALE_ONLY, pitch) + "," 
               + s_y(2, constants.SCALE_ONLY, pitch) + " h " 
               + s_x(-4, constants.SCALE_ONLY, pitch) + " z\"")

    # Set the approriate color for the pin.

    svg.append("      fill=\"#b8af82\"")

    svg.append("      stroke-width=\"0\"")

    svg.append("    />")

    return svg


def male_pinright(svg, connector, columns, row, column, pitch):

    # Generate a pinright path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

#*** remove me later ***
#   print("Start pinright row {0:d}".format(row))

    svg.append("    <path")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"pinright" + str(connector) + "\"")

    # Then create the path, moving and scaling the coordinates as
    # we go. Use s_r_y() for the absolute y start coord after that is
    # relative and doesn't need that translation.

    svg.append("      d=\""
               + "M " + s_x(12, row, pitch) + ","
               + s_r_y(8, columns, column, pitch)
               + " l " + s_x(2, constants.SCALE_ONLY, pitch) + ","
               + s_y(-2, constants.SCALE_ONLY, pitch)
               + " v " + s_x(8, constants.SCALE_ONLY, pitch)
               + " l " + s_x(-2, constants.SCALE_ONLY, pitch) + "," 
               + s_y(-2, constants.SCALE_ONLY, pitch) + " z\"")

    # Set the approriate color for the pin.

    svg.append("      fill=\"#9a916c\"")

    svg.append("      stroke-width=\"0\"")

    svg.append("    />")

    return svg


def male_pinbottom(svg, connector, columns, row, column, pitch):

    # Generate a pinbottom path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

#*** remove me later ***
#    print("Start pinbottom row {0:d}".format(row))

    svg.append("    <path")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"pinbottom" + str(connector) + "\"")

    # Then create the path, moving and scaling the coordinates as
    # we go. Use s_r_y() for the absolute y start coord after that is
    # relative and doesn't need that translation.

    svg.append("      d=\""
               + "M " + s_x(6, row, pitch)
               + "," + s_r_y(14, columns, column, pitch)
               + " l " + s_x(2, constants.SCALE_ONLY, pitch) + ","
               + s_y(-2, constants.SCALE_ONLY, pitch)
               + " h " + s_x(4, constants.SCALE_ONLY, pitch)
               + " l " + s_x(2, constants.SCALE_ONLY, pitch) + "," 
               + s_y(2,  constants.SCALE_ONLY, pitch) + " z\"")

    # Set the approriate color for the pin.

    svg.append("      fill=\"#5e5b43\"")

    svg.append("      stroke-width=\"0\"")

    svg.append("    />")

    return svg


def male_pinconnector(connectors, connector, columns, row, column, pitch):

    # Generate a pinconnector rect and label it with the connector number.
    # followed by pin to make a Fritzing connector.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical. Note it returns connectors and the connectors (and only the
    # connectors) are returned in order in connectors. This is so the pins 
    # can be appended to the end of the connectors to be in the correct place
    # for use by other tools. Use s_r_y() for the absolute y start coord 
    # after that is relative and doesn't need that translation.

#*** remove me later ***
#   print("Start pinconnector row {0:d}".format(row))


    connectors.append("    <rect")

    # Create a label ending in the connector number followed by pin to
    # make a Fritzing pin which matches the definition in the .fzp file.

    connectors.append("      id=\"connector" + str(connector) + "pin" + "\"")
    connectors.append("      fill=\"#8c8663\"")
    connectors.append("      stroke-width=\"0\"")
    connectors.append("      x=\"" + s_x(8, row, pitch) + "\"")
    connectors.append("      width=\"" + s_x(4, constants.SCALE_ONLY, pitch)
                                       + "\"")
    connectors.append("      y=\"" + s_r_y(8, columns, column, pitch) + "\"")
    connectors.append("      height=\"" + s_x(4, constants.SCALE_ONLY, pitch)
                                        + "\"")
    connectors.append("    />")

    return connectors


def male_pin_no(svg, connector, row, column, pitch):

    # Create the pin number text for a schematic pin.

    svg.append("    <text")
    svg.append("      id=\"pintext" + str(connector) + "\"")
    svg.append("      fill=\"#555555\"")
    svg.append("      stroke-width=\"0\"")
    svg.append("      text-anchor=\"middle\"")
    svg.append("      font-family=\"'Droid Sans'\"")
    svg.append("      font-size=\"{0:s}\"".format(s_x(6.9,
                                           constants.SCALE_ONLY, pitch)))
    svg.append("      x=\"" + s_x(15.4, column, pitch) + "\"")
    svg.append("      y=\"" + s_y(6.9, row, pitch) + "\"" +
                                ">{0:s}</text>".format(str(connector)))
    return svg


def male_line1(svg, connector, row, column, pitch):

    # Create the upper half of a schematic arrow line.

    svg.append("    <line")
    svg.append("      id=\"pinline1-" + str(connector) + "\"")
    svg.append("      fill=\"none\"")
    svg.append("      stroke=\"#000000\"")
    svg.append("      stroke-width=\"{0:s}\"".format(s_x(1.9685,
                                              constants.SCALE_ONLY, pitch)))
    svg.append("      stroke-linecap=\"round\"")
    svg.append("      x1=\"" + s_x(38.36, column, pitch) + "\"")
    svg.append("      x2=\"" + s_x(27.36, column, pitch) + "\"")
    svg.append("      y1=\"" + s_y(9.8, row, pitch) + "\"")
    svg.append("      y2=\"" + s_y(4.299, row, pitch) + "\"")
    svg.append("    />")

    return svg


def male_line2(svg, connector, row, column, pitch):

    # Create the staight middle of a schematic arrow line.

    svg.append("    <line")
    svg.append("      id=\"pinline2-" + str(connector) + "\"")
    svg.append("      fill=\"none\"")
    svg.append("      stroke=\"#000000\"")
    svg.append("      stroke-width=\"{0:s}\"".format(s_x(1.9685,
                                                 constants.SCALE_ONLY, pitch)))
    svg.append("      stroke-linecap=\"round\"")
    svg.append("      x1=\"" + s_x(38.385, column, pitch) + "\"")
    svg.append("      x2=\"" + s_x(20.699, column, pitch) + "\"")
    svg.append("      y1=\"" + s_y(9.8425, row, pitch) + "\"")
    svg.append("      y2=\"" + s_y(9.8425, row, pitch) + "\"")
    svg.append("    />")

    return svg


def male_line3(svg, connector, row, column, pitch):

    # Create the lower half of a schematic arrow line.

    svg.append("    <line")
    svg.append("      id=\"pinline3-" + str(connector) + "\"")
    svg.append("      fill=\"none\"")
    svg.append("      stroke=\"#000000\"")
    svg.append("      stroke-width=\"{0:s}\"".format(s_x(1.9685,
                                              constants.SCALE_ONLY, pitch)))
    svg.append("      stroke-linecap=\"round\"")
    svg.append("      x1=\"" + s_x(38.36, column, pitch) + "\"")
    svg.append("      x2=\"" + s_x(27.36, column, pitch) + "\"")
    svg.append("      y1=\"" + s_y(9.799, row, pitch) + "\"")
    svg.append("      y2=\"" + s_y(15, row, pitch) + "\"")
    svg.append("    />")

    return svg


def male_pin(connectors, connector, row, column, pitch):

    # Create the schematic pin line.

    stroke_width = s_x(1.9685, constants.SCALE_ONLY, pitch)

    connectors.append("    <line")
    connectors.append("      id=\"connector" + str(connector) + "pin\"")
    connectors.append("      fill=\"none\"")
    connectors.append("      stroke=\"#555555\"")
    connectors.append("      stroke-width=\"{0:s}\"".format(stroke_width))
    connectors.append("      stroke-linecap=\"round\"")
    connectors.append("      x1=\"" + s_x(1, column, pitch) + "\"")
    connectors.append("      x2=\"" + s_x(21.7, column, pitch) + "\"")
    connectors.append("      y1=\"" + s_y(9.85, row, pitch) + "\"")
    connectors.append("      y2=\"" + s_y(9.85, row, pitch) + "\"")
    connectors.append("     />")

    return connectors


def male_terminal(connectors, connector, row, column, pitch):

    # Create the schematic terminal rectangle.

    connectors.append("    <rect")
    connectors.append("      id=\"connector" + str(connector) + "terminal\"")
    connectors.append("      fill=\"#555555\"")
    connectors.append("      stroke=\"none\"")
    connectors.append("      stroke-width=\"{0:s}\"".format(s_x(0,
                                                 constants.SCALE_ONLY, pitch)))
    connectors.append("      x=\"" + s_x(0.3, column, pitch) + "\"")
    connectors.append("      y=\"" + s_y(9.74, row, pitch) + "\"")
    connectors.append("      height=\"1\"")
    connectors.append("      width=\"1\"")
    connectors.append("    />")

    return connectors


def create_male_breadboard_pin(svg, connectors, connector, columns, row,
                               column, pitch, color):

    # Create a male breadboard pin.

    svg = male_outline(svg, connector, columns, row, column, pitch, color)
    svg = male_pinleft(svg, connector, columns, row, column, pitch)
    svg = male_pintop(svg, connector, columns, row, column, pitch)
    svg = male_pinright(svg, connector, columns, row, column, pitch)
    svg = male_pinbottom(svg, connector, columns, row, column, pitch)
    connectors = male_pinconnector(connectors, connector, columns, row,
                                   column, pitch)
    return svg, connectors

    # Start of female breadboard pin code.

def female_outline(svg, connector, columns, row, column, pitch, color):

    # Generate an outline path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

#*** remove me later ***
    print("Start outline row {0:d} column {1:d}".format(row, column))


    svg.append("    <rect")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"outline" + str(connector) + "\"")

    # Then create the rectangle, moving and scaling the coordinates as
    # we go.

    # Set the approriate color for the pin.

    svg.append("      fill=\"#404040\"")

    svg.append("      stroke=\"none\"")

    svg.append("      stroke-width=\"0\"")

    # Hard code the row to 0 to keep the pin only moving horizontally.

    svg.append("      x=\"" + s_x(-1, row, pitch) + "\"")

    svg.append("      y=\"" + s_r_y(-1, columns, column, pitch) + "\"")

    svg.append("      height=\"" + s_y(20.68, 
                                        constants.SCALE_ONLY, pitch) + "\"")

    svg.append("      width=\"" + s_x(20.68, 
                                        constants.SCALE_ONLY, pitch) + "\"")

    svg.append("    />")

    return svg


def female_pinleft(svg, connector, columns, row, column, pitch):

    # Generate a pinleft path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

    svg.append("    <path")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"pinleft" + str(connector) + "\"")

    # Then create the path, moving and scaling the coordinates as
    # we go. Use s_r_y() for the absolute y start coord after that is
    # relative and doesn't need that translation.

    svg.append("      d=\""
               + "m " + s_x(6, row, pitch) + "," + s_r_y(6, columns, column,
                                                         pitch)
               + " v " + s_x(7.6, constants.SCALE_ONLY, pitch)
               + " l " + s_x(-2.8, constants.SCALE_ONLY, pitch) +
                             "," + s_y(2.8, constants.SCALE_ONLY, pitch)
               + " v " + s_y(-13.2, constants.SCALE_ONLY , pitch)
               + " z\"")

    # Set the approriate color for the pin.

    svg.append("      fill=\"#373737\"")

    svg.append("      stroke-width=\"0\"")

    svg.append("    />")

    return svg


def female_pintop(svg, connector, columns, row, column, pitch):

    # Generate a pintop path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

    svg.append("    <path")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"pintop" + str(connector) + "\"")

    # Then create the path, moving and scaling the coordinates as
    # we go. Use s_r_y() for the absolute y start coord after that is
    # relative and doesn't need that translation.

    svg.append("      d=\""
               + "m " + s_x(3.24, row, pitch) + "," + s_r_y(3.24, columns,
                                                             column, pitch)
               + " h " + s_x(13.2, constants.SCALE_ONLY, pitch)
               + " l " + s_x(-2.8, constants.SCALE_ONLY, pitch)
               + "," + s_y(2.8, constants.SCALE_ONLY, pitch)
               + " h " + s_x(-7.6, constants.SCALE_ONLY, pitch)
               + " z\"")

    # Set the approriate color for the pin.

    svg.append("      fill=\"#2a2a2a\"")

    svg.append("      stroke-width=\"0\"")

    svg.append("    />")

    return svg


def female_pinright(svg, connector, columns, row, column, pitch):

    # Generate a pinright path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

    svg.append("    <path")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"pinright" + str(connector) + "\"")

    # Then create the path, moving and scaling the coordinates as
    # we go. Use s_r_y() for the absolute y start coord after that is
    # relative and doesn't need that translation.

    svg.append("      d=\""
               + "m " + s_x(13.65, row, pitch) + "," + s_r_y(6, columns, 
                                                             column, pitch)
               + " " + s_x(2.8, constants.SCALE_ONLY, pitch)
               + "," + s_y(-2.8, constants.SCALE_ONLY, pitch)
               + " v " + s_x(13.2, constants.SCALE_ONLY, pitch)
               + " l " + s_x(-2.8, constants.SCALE_ONLY, pitch)
               + "," + s_y(-2.8, constants.SCALE_ONLY, pitch)
               + " z\"")

    # Set the approriate color for the pin.

    svg.append("      fill=\"#474747\"")

    svg.append("      stroke-width=\"0\"")

    svg.append("    />")

    return svg


def female_pinbottom(svg, connector, columns, row, column, pitch):

    # Generate a pinbottom path and label it with the connector number.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical.

    svg.append("    <path")

    # Create a label ending in the connector number to be unique.

    svg.append("      id=\"pinbottom" + str(connector) + "\"")

    # Then create the path, moving and scaling the coordinates as
    # we go. Use s_r_y() for the absolute y start coord after that is
    # relative and doesn't need that translation.

    svg.append("      d=\""
               + "m " + s_x(6, row, pitch) + "," + s_r_y(13.65, columns, 
                                                         column, pitch)
               + " h " + s_y(7, constants.SCALE_ONLY, pitch)
               + " l " + s_x(2.8, constants.SCALE_ONLY, pitch)
               + "," + s_y(2.8,  constants.SCALE_ONLY, pitch)
               + " h " + s_y(-13.2, constants.SCALE_ONLY, pitch)
               + " z\"")

    # Set the approriate color for the pin.

    svg.append("      fill=\"#595959\"")

    svg.append("      stroke-width=\"0\"")

    svg.append("    />")

    return svg


def female_pinconnector(connectors, connector, columns, row, column, pitch):

    # Generate a pinconnector rect and label it with the connector number.
    # followed by pin to make a Fritzing connector.
    # Adjust the staring position in x and y and the scale to position
    # and size it correctly. Assumes row is horizontal and column is
    # vertical. Note it returns connectors and the connectors (and only the
    # connectors) are returned in order in connectors. This is so the pins 
    # can be appended to the end of the connectors to be in the correct place
    # for use by other tools.

    connectors.append("    <rect")

    # Create a label ending in the connector number followed by pin to
    # make a Fritzing pin which matches the definition in the .fzp file.

    connectors.append("      id=\"connector" + str(connector) + "pin" + "\"")
    connectors.append("      fill=\"#000000\"")
    connectors.append("      stroke-width=\"0\"")
    connectors.append("      x=\"" + s_x(6, row, pitch) + "\"")
    connectors.append("      width=\"" + s_x(7.6, constants.SCALE_ONLY, pitch)
                       + "\"")
    connectors.append("      y=\"" + s_r_y(6, columns, column, pitch) + "\"")
    connectors.append("      height=\"" + s_y(7.6, constants.SCALE_ONLY, pitch)
                       + "\"")
    connectors.append("    />")

    return connectors



def create_female_breadboard_pin(svg, connectors, connector, columns, row,
                               column, pitch, color):

    # Create a female breadboard pin.

    svg = female_outline(svg, connector, columns, row, column, pitch, color)
    svg = female_pinleft(svg, connector, columns, row, column, pitch)
    svg = female_pintop(svg, connector, columns, row, column, pitch)
    svg = female_pinright(svg, connector, columns, row, column, pitch)
    svg = female_pinbottom(svg, connector, columns, row, column, pitch)
    connectors = female_pinconnector(connectors, connector, columns, row,
                                   column, pitch)
    return svg, connectors



def create_male_schematic_pin(svg, connectors, connector, row, column, pitch):

    # Create a male schematic breadboard pin,

# *** remove me later ***
#   print("sch pin_no con {0:d} row {1:d} column {2:d} pitch {3:f}".format(connector, row, column, pitch))

    svg = male_pin_no(svg, connector, row, column, pitch)

# *** remove me later ***
#   print("sch male_line1 con {0:d} row {1:d} column {2:d} pitch {3:f}".format(connector, row, column, pitch))

    svg = male_line1(svg, connector, row, column, pitch)

# *** remove me later ***
#   print("sch male_line2 con {0:d} row {1:d} column {2:d} pitch {3:f}".format(connector, row, column, pitch))

    svg = male_line2(svg, connector, row, column, pitch)

# *** remove me later ***
#   print("sch male_line3 con {0:d} row {1:d} column {2:d} pitch {3:f}".format(connector, row, column, pitch))

    svg = male_line3(svg, connector, row, column, pitch)

# *** remove me later ***
#   print("sch male_pin con {0:d} row {1:d} column {2:d} pitch {3:f}".format(connector, row, column, pitch))

    connectors = male_pin(connectors, connector, row, column, pitch)

# *** remove me later ***
#   print("sch male_terminal con {0:d} row {1:d} column {2:d} pitch {3:f}".format(connector, row, column, pitch))

    connectors = male_terminal(connectors, connector, row, column, pitch)
    return svg, connectors


def create_pcb_pin(svg, connectors, connector, columns, row, column, pitch,
                   pcb_type, pad_type):

    if pcb_type == constants.SMD:

        # There is only copper1 so set indent to a single blank.

        if pad_type != constants.RECTANGLE:

            print("Error: SMD pad type must be RECTANGLE!", file=sys.stderr)

    elif pcb_type == constants.THT:

        # There are both copper1 and copper0 so set indent to a 3 blanks.

        indent = "   "

        if pad_type == constants.RECTANGLE:

            print("Error: RECTANGLE not valid in THT!", file=sys.stderr)

    else:

        # Otherwise this is an error.

        print("Error: Unknown pcb_type", file=sys.stderr)

        exit(1)

    # Create a pcb pin

    if pcb_type == constants.THT:

        if pad_type == constants.CIRCLE:

            connectors.append("     <circle")

            # For THT label is "pin"

            connectors.append("       id=\"connector{0:d}pin\"".format(
                                                            connector))
            connectors.append("       fill=\"none\"")
            connectors.append("       stroke=\"#ffbf00\"")

            # Scale the default radius value (hard code a row of 0 to trigger
            # only a scale).

            connectors.append("       r=\""
                             + s_x(5.70866, constants.SCALE_ONLY, pitch) + "\"")

            # Scale the default stroke-width value (hard code a row of 0 to
            # trigger only a scale).

            connectors.append("       stroke-width=\""
                              + s_x(3.937, constants.SCALE_ONLY, pitch) + "\"")


#            if pitch < constants.PITCH_2MM:

            # Scale the default x coord value and potentially move it
            # according to its row value.

            connectors.append("       cx=\"" + s_x(10.23,
                                            row, pitch) + "\"")

            # Scale the default y coord value and potentially move it 
            # according to its column value adjusted for column based pin
            # numbering. Use s_r_y() to get pin0 on the bottom where it 
            # should be. 

            connectors.append("       cy=\"" + s_r_y(12.89,
                                            columns, column, pitch) + "\"")
#            else:

                # At pitch values > 2mm adjust the default coord to account
                # for the stroke-width changing to 10 (fixed).
                # Scale the default x coord value and potentially move it
                # according to its row value.

#            connectors.append("       cx=\"" + s_x(10.3366968503937,
#                                             row, pitch) + "\"")

            # Scale the default y coord value and potentially move it 
            # according to its column value adjusted for column based pin
            # numbering. Use s_r_y() to get pin0 on the bottom where it 
            # should be. 

#            connectors.append("       cy=\"" + s_r_y(10.3366968503937,
#                                            columns, column, pitch) + "\"")

            # Then close the circle.

            connectors.append("     />")

        elif pad_type == constants.OBLONG:

#*** remove me later ***
#            print("pcb oblong: columns {0:d} column {1:d} {2:d}".format(columns, column, row))

            if columns == 1:

#*** remove me later ***
#                print("pcb oblong: columns == 1")

                # For a single column use the 
                # svg.pcb.oblong_single-pin-0.5mm_pcb.svg reference file.
                # First we need to emit the path (using svg.append() rather
                # connectors.append() to get it in the correct place) and then 
                # the cirle for the connector using connectors.append().

                svg.append("    <path")
                svg.append("      stroke-width=\"0\"")
                svg.append("      stroke=\"none\"")
                svg.append("      fill=\"#ffbf00\"")
                svg.append("      d=\""
                           + "m " + s_x(16.3, row, pitch) + ","
                           + s_y(8.8, column, pitch)
                           + " c "
                           + s_x(0, constants.SCALE_ONLY, pitch)
                           + "," + s_y(2.7, constants.SCALE_ONLY, pitch) + " "
                           + s_x(0, constants.SCALE_ONLY, pitch) + ","
                           + s_y(7.2, constants.SCALE_ONLY, pitch) + " "
                           + s_x(0, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(10, constants.SCALE_ONLY, pitch) + " "
                           + s_x(0, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(3.9, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-2.6, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(5.4, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-5.3, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(5.5, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-2.6, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(0, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-5.3, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-1.5, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-5.3, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-5.5, constants.SCALE_ONLY, pitch) + " "
                           + "v " + s_y(-10.28, constants.SCALE_ONLY, pitch)
                           + " c " + s_x(0, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-3.1, constants.SCALE_ONLY, pitch) + " "
                           + s_x(2.6, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-4.8, constants.SCALE_ONLY, pitch) + " "
                           + s_x(5.2, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-4.8, constants.SCALE_ONLY, pitch) + " "
                           + s_x(2.7, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(0, constants.SCALE_ONLY, pitch) + " "
                           + s_x(5.3, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(1.5, constants.SCALE_ONLY, pitch) + " "
                           + s_x(5.4, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(4.9, constants.SCALE_ONLY, pitch) + " z\"")
                svg.append("    />")

                connectors.append("     <circle")

                # For THT label is "pin"

                connectors.append("       id=\"connector{0:d}pin\"".format(
                                                            connector))
                connectors.append("       fill=\"#ffffff\"")
                connectors.append("       stroke=\"#ffbf00\"")

                # Scale the default radius value (hard code a row of 0 to
                # trigger only a scale).

                connectors.append("       r=\"" 
                                + s_x(4.2, constants.SCALE_ONLY, pitch) + "\"")

                # Scale the default stroke-width value (hard code a row of 0 
                # to trigger only a scale).

                connectors.append("       stroke-width=\""
                           + s_x(0.9, constants.SCALE_ONLY, pitch) + "\"")

                # Scale the default x coord value and potentially move it
                # according to its row value.

                connectors.append("       cx=\"" + s_x(11, row, pitch) + "\"")

                # Scale the default y coord value and potentially move it 
                # according to its column value adjusted for column based pin
                # numbering. Use s_r_y() to get pin0 on the bottom where it 
                # should be. 

                connectors.append("       cy=\"" + s_r_y(14, columns, column, 
                                                pitch) + "\"")

                # Then close the circle.

                connectors.append("     />")

            elif column == 1:

#*** remove me later ***
#                print("pcb oblong: column == 1")

                # For a column 1 use the 
                # svg.pcb.oblong_bottom-pin-0.5mm_pcb.svg reference file.
                # First we need to emit the path (using svg.append() rather
                # connectors.append() to get it in the correct place) and then 
                # the cirle for the connector using connectors.append().

                svg.append("    <path")
                svg.append("      stroke-width=\"0\"")
                svg.append("      stroke=\"none\"")
                svg.append("      fill=\"#ffbf00\"")
                svg.append("      d=\""
                           + "m " + s_x(11, row, pitch) + ","
                           + s_r_y(7.5, columns, column, pitch)
                           + " c "
                           + s_x(3.2, constants.SCALE_ONLY, pitch) + ","
                           + s_y(0, constants.SCALE_ONLY, pitch) + " "
                           + s_x(5.9, constants.SCALE_ONLY, pitch) + ","
                           + s_y(2.6, constants.SCALE_ONLY, pitch) + " "
                           + s_x(5.9, constants.SCALE_ONLY, pitch) + ","
                           + s_y(4.9, constants.SCALE_ONLY, pitch) + " "
                           + " v " + s_x(8.3, constants.SCALE_ONLY, pitch)
                           + " c "
                           + s_x(0, constants.SCALE_ONLY, pitch) + ","
                           + s_y(2.3, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-2.6, constants.SCALE_ONLY, pitch) + ","
                           + s_y(4.1, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-5.9, constants.SCALE_ONLY, pitch) + ","
                           + s_y(4.1, constants.SCALE_ONLY, pitch) + " v " 
                           + s_x(0, constants.SCALE_ONLY, pitch) + " c "
                           + s_x(-3.2, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(0, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-5.9, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-1.8, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-5.9, constants.SCALE_ONLY, pitch) + ","
                           + s_y(-4.1, constants.SCALE_ONLY, pitch) + " v " 
                           + s_x(-8.4, constants.SCALE_ONLY, pitch) + " c "
                           + s_x(0, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-2.2, constants.SCALE_ONLY, pitch) + " "
                           + s_x(2.7, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-4.8, constants.SCALE_ONLY, pitch) + " "
                           + s_x(5.9, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-4.8, constants.SCALE_ONLY, pitch) + " z\"")
                svg.append("    />")

                connectors.append("     <circle")

                # For THT label is "pin"

                connectors.append("       id=\"connector{0:d}pin\"".format(
                                                            connector))
                connectors.append("       fill=\"#ffffff\"")
                connectors.append("       stroke=\"#ffbf00\"")

                # Scale the default radius value (hard code a row of 0 to
                # trigger only a scale).

                connectors.append("       r=\"" + s_x(4.2,
                                         constants.SCALE_ONLY , pitch) + "\"")

                # Scale the default stroke-width value (hard code a row of 0 
                # to trigger only a scale).

                connectors.append("       stroke-width=\"" + s_x(0.9, 
                                         constants.SCALE_ONLY, pitch) + "\"")

                # Scale the default x coord value and potentially move it
                # according to its row value.

                connectors.append("       cx=\"" + s_x(11, row, pitch) + "\"")

                # Scale the default y coord value and potentially move it 
                # according to its column value adjusted for column based pin
                # numbering. Use s_r_y() to get pin0 on the bottom where it 
                # should be. 

                connectors.append("       cy=\"" + s_r_y(14, columns, column, 
                                                pitch) + "\"")

                # Then close the circle.

                connectors.append("     />")

            elif column > 1 and column < columns:

#*** remove me later ***
#                print("pcb oblong: column > 1 column < columns")

                # This is a middle columns so use
                # svg.pcb.oblong-middle-circle_single-pin-0.5mm_pcb.svg
                # for the pin.

                connectors.append("     <circle")

                # For THT label is "pin"

                connectors.append("       id=\"connector{0:d}pin\"".format(
                                                            connector))
                connectors.append("       fill=\"#ffffff\"")
                connectors.append("       stroke=\"#ffbf00\"")

                # Scale the default radius value (hard code a row of 0 to
                # trigger only a scale).

                connectors.append("       r=\"" + s_x(4.75, 
                                          constants.SCALE_ONLY, pitch) + "\"")

                # Scale the default stroke-width value (hard code a row of 0 
                # to trigger only a scale).

                connectors.append("       stroke-width=\"" + s_x(2, 
                                          constants.SCALE_ONLY, pitch) + "\"")

                # Scale the default x coord value and potentially move it
                # according to its row value.

                connectors.append("       cx=\"" + s_x(11, row, pitch) + "\"")

                # Scale the default y coord value and potentially move it 
                # according to its column value adjusted for column based pin
                # numbering. Use s_r_y() to get pin0 on the bottom where it 
                # should be. 

                connectors.append("       cy=\"" + s_r_y(14, columns, column, 
                                                pitch) + "\"")

                # Then close the circle.

                connectors.append("     />")

            elif column == columns:

#*** remove me later ***
#                print("pcb oblong: column == columns")

                # We are on the top row so use the
                # svg.pcb.oblong_top-pin-0.5mm_pcb.svg reference file.
                # First we need to emit the path (using svg.append() rather
                # connectors.append() to get it in the correct place) and then 
                # the cirle for the connector using connectors.append().

                svg.append("    <path")
                svg.append("      stroke-width=\"0\"")
                svg.append("      stroke=\"none\"")
                svg.append("      fill=\"#ffbf00\"")
                svg.append("      d=\""
                           + "m "
                           + s_x(11, row, pitch) + ","
                           + s_r_y(3.7, columns, column, pitch) + " c "
                           + s_x(3.2, constants.SCALE_ONLY, pitch) + ","
                           + s_y(0, constants.SCALE_ONLY, pitch) + " "
                           + s_x(5.9, constants.SCALE_ONLY, pitch) + ","
                           + s_y(2.6, constants.SCALE_ONLY, pitch) + " "
                           + s_x(5.9, constants.SCALE_ONLY, pitch) + ","
                           + s_y(4.9, constants.SCALE_ONLY, pitch) + " v "
                           + s_x(8.3, constants.SCALE_ONLY, pitch) + " c "
                           + s_x(0, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(2.3, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-2.6, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(4.1, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-5.9, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(4.1, constants.SCALE_ONLY, pitch) + " v " 
                           + s_x(0, constants.SCALE_ONLY, pitch) + " c "
                           + s_x(-3.2, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(0, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-5.9, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-1.8, constants.SCALE_ONLY, pitch) + " "
                           + s_x(-5.9, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-4.1, constants.SCALE_ONLY, pitch) + " v " 
                           + s_x(-8.4, constants.SCALE_ONLY, pitch) + " c "
                           + s_x(0, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-2.2, constants.SCALE_ONLY, pitch) + " "
                           + s_x(2.7, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-4.8, constants.SCALE_ONLY, pitch) + " "
                           + s_x(5.86, constants.SCALE_ONLY, pitch) + "," 
                           + s_y(-4.8, constants.SCALE_ONLY, pitch) + " z\"")
                svg.append("    />")

                connectors.append("     <circle")

                # For THT label is "pin"

                connectors.append("       id=\"connector{0:d}pin\"".format(
                                                            connector))
                connectors.append("       fill=\"#ffffff\"")
                connectors.append("       stroke=\"#ffbf00\"")

                # Scale the default radius value (hard code a row of 0 to
                # trigger only a scale).

                connectors.append("       r=\"" + s_x(4.2,
                                         constants.SCALE_ONLY, pitch) + "\"")

                # Scale the default stroke-width value (hard code a row of 0 
                # to trigger only a scale).

                connectors.append("       stroke-width=\"" + s_x(0.9, 
                                         constants.SCALE_ONLY, pitch) + "\"")

                # Scale the default x coord value and potentially move it
                # according to its row value.

                connectors.append("       cx=\"" + s_x(11, row, pitch) + "\"")

                # Scale the default y coord value and potentially move it 
                # according to its column value adjusted for column based pin
                # numbering. Use s_r_y() to get pin0 on the bottom where it 
                # should be. 

                connectors.append("       cy=\"" + s_r_y(14, columns, column, 
                                                pitch) + "\"")

                # Then close the circle.

                connectors.append("     />")

    else:

        print("pad type {0:d} Not implemented yet".format(pad_type),
               file=sys.stderr)

        exit(1)

    return svg, connectors


def create_pin(svg, connectors, connector, svg_type, part_type, columns, row,
               column, pitch, color, pcb_type, pad_type):

    # Create a single pin, positioning it correctly in x and y and
    # adjusting its scale according to pitch. Note the connectors are
    # returned in connector order in list connectors so they can be
    # appended to the end of the svg for use by other tools.

    if (svg_type == constants.BREADBOARD and
        part_type == constants.MALE_HEADER):

        # Create a breadboard male header pin

        svg, connectors = create_male_breadboard_pin(svg, connectors,
                                                     connector, columns, row,
                                                     column, pitch, color)
        return svg, connectors

    elif (svg_type == constants.BREADBOARD and
          part_type == constants.FEMALE_HEADER):

        # Create a breadboard female header pin

        svg, connectors = create_female_breadboard_pin(svg, connectors,
                                                     connector, columns, row,
                                                     column, pitch, color)
        return svg, connectors

    elif (svg_type == constants.SCHEMATIC and
          part_type == constants.MALE_HEADER):

        # Create a schematic male header pin. The row number is increased
        # by the value of offset to space different rows of the connector
        # in schematic.

        #       breakpoint()

        svg, connectors = create_male_schematic_pin(svg, connectors,
                                                    connector, row, column, 
                                                    pitch)
        return svg, connectors

#   not yet implemented.

#    elif (svg_type == constants.SCHEMATIC and
#          part_type == constants.FEMALE_HEADER):

        # Create a schematic male header pin. The row number is increased
        # by the value of offset to space different rows of the connector
        # in schematic.

        #       breakpoint()

#        svg, connectors = create_female_schematic_pin(svg, connectors,
#                                                    connector, row + offset,
#                                                    column, pitch)
#        return svg, connectors

    elif (svg_type == constants.PCB and
          part_type == constants.MALE_HEADER or 
          part_type == constants.FEMALE_HEADER):

        svg, connectors = create_pcb_pin(svg, connectors, connector, columns,
                                         row, column, pitch, pcb_type,
                                         pad_type)

        return svg, connectors

    else:

        print("svg_type {0:d} part type {1:s} Not implemented yet".format(
              svg_type, part_type), file=sys.stderr)

        exit(1)


def create_svg(svg_type, moduleid, part_type, rows, columns, pitch, pcb_type,
               pin_order, pad_type, color, ref_file, layerid):

    # Create the svg for a view.

    svg = []

    connectors = []

    svg.append("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>")

    svg.append("<svg")

    svg.append("  y=\"0in\"")

    svg.append("  x=\"0in\"")

    if svg_type == constants.SCHEMATIC:

        # Schematic only adds by row, so we need to ignore the column value
        # and set the columns to 0.2in because a pin is two columns wide and
        # the pitch is hardcoded to be 0.1in for schematic only.

        
        width = 0.2

#*** remove me later ***
#        print("\nSch: width {0:f} pitch {1:f}".format(width, pitch))

        # Then calculate the height allowing for 1 extra space per row
        #(via the (columns - 1) portion of the calculation) then convert the
        # resulting size (in 1/1000 of an inch) to inches by multiplying by
        # 1000 and rounding to 2 digits after the decimal.

        height = round((float(100) * (float(columns - 1) + (float(rows) *
                        float(columns))) / float(1000)), 2)

#*** remove me later ***
#        print("Sch: height {0:f}".format(height))

    elif svg_type == constants.PCB:

#        if pitch < constants.PITCH_2MM:

#        if True:

            
        # At pitches < 2mm scale the stroke-width to keep the silkscreen
        # size reasonable, at 2mm and greater set it to 10thou.
        # Use rectangle stroke-width as that is the height and width we are 
        # using!


        stroke_width = 1.968 * pitch / 1000.0

        print("pcb stroke_width = {0:f}".format(stroke_width))

        height = round(float(pitch) * float(columns) * float(0.024)
                                                  + stroke_width, 5)

#        height = float(pitch) * float(columns) * float(0.02046)

#       Try the height and width of 128x128 Doesn't work!

#        height = float(pitch) * float(columns) * float(0.01973330625)


        width = round(float(pitch) * float(rows) * float(0.0185)
                                               + stroke_width, 5)

#        width = float(pitch) * float(rows) * float(0.0198)

#       Try the height and width of 128x128 Doesn't work!

#        width = float(pitch) * float(rows) * float(0.0196911953125)

        print("pcb viewbox = {0:f} {1:f}".format(height, width))

#        else:

            # Above 2mm the stroke-width is always 10 so hard code that
            # (in inches so 10 thou is 0.01in.)

#            stroke_width = 0.01

#            height = round(float(pitch) * float(columns) * float(0.019685)
#                                 + stroke_width, 5)

#            width = round(float(pitch) * float(rows) * float(0.019685)
#                                 + stroke_width, 5)


#        print("pcb width = {0:f} rows {1:d}\npcb height = {2:f} columns {3:d}".format(width, rows, height, columns))

    else:

        # multiply the number of columns by the pitch then divide by 1000 t0
        # covert to inches of an element to get the correct height. Round the
        # result to 5digits after the decimal.

        height = round(float(pitch) * float(columns) * float(0.0198), 5)

        print("else height = {0:f} columns {1:d}".format(height, columns))

        # multiply the number of rows by the pitch (converted to inches)
        # of an element to get the correct width. Round the result to 5
        # digits after the  decimal.

        width = round(float(pitch) * float(rows) * float(0.0198), 5)

        print("else width = {0:f} rows {1:d}".format(width, rows))

    svg.append("  height=\"{0:f}in\"".format(height))

    svg.append("  width=\"{0:f}in\"".format(width))

    # viewbox needs to be 1000 x width and 1000 x height (assumes height
    # and width are in inches!) to make drawing units 1/1000in.

    svg.append("  viewBox=\"0 0 {0:f} {1:f}\"".format(
        round(width * float(1000), 5),
        round(height * float(1000), 5)))

    svg.append("  version=\"1.2\"")

    # Any svg id will do.

    svg.append("  id=\"svg21\"")

    svg.append("  xmlns=\"http://www.w3.org/2000/svg\"")

    svg.append("  xmlns:svg=\"http://www.w3.org/2000/svg\">")

    svg.append("  <defs")

    # Any defs id will do.

    svg.append("    id=\"defs25\"")

    svg.append("  />")

    svg.append("  <desc")

    svg.append("    id=\"desc2\">")

    # File name of the svg these parameters were copied from.

    svg.append('      <referenceFile>{0:s}</referenceFile>'.format(ref_file))

    svg.append("  </desc>")

    svg.append("  <g")

    # Add the layerId.

    # If this is pcb there are 2 or 3 layerIds depending on if the part is
    # THT (3 layerids) or SMD 2 layerids) so deal with that if this is pcb.

    if svg_type == constants.PCB:

        # First do the silkscreen which exists in either option and wants to
        # come first in the svg.

        svg.append("    id=\"silkscreen\">")

        if (part_type == constants.MALE_HEADER or
            part_type == constants.FEMALE_HEADER):

            # First calculate the size of the rectangle surrounding the pins
            # on the silkscreen and emit it. Save the value of the height
            # as the pin0marker needs it.

            svg.append("    <rect")

            svg.append("      id=\"rect\"")

            svg.append("      stroke=\"#000000\"")

            svg.append("      fill=\"none\"")

#            if pitch < constants.PITCH_2MM:

            if True:

                # calculate and save the scaled stroke-width/2 for later
                # adjustments.

                stroke_width = (float(s_x(1.968, constants.SCALE_ONLY, pitch))
                                     * 0.5)

                print("< 2mm: stroke-width {0:f}".format(stroke_width))

                # If the pitch is less than 2MM, scale the stroke-width.

                svg.append("      stroke-width=\"" + s_x(1.968,
                                  constants.SCALE_ONLY, pitch) + "\"") 

                print("< 2mm: stroke-width {0:s}".format(s_x(1.968, constants.SCALE_ONLY, pitch)))

                svg.append("      x=\"" + s_x(0.984, constants.SCALE_ONLY,
                                                         pitch) + "\"")

                print("< 2mm: x {0:s}".format(s_x(0.984, constants.SCALE_ONLY, pitch)))

                svg.append("      y=\"" + s_y(0.984, constants.SCALE_ONLY,
                                                         pitch) + "\"")

                print("< 2mm: y {0:s}".format(s_x(0.984, 
                                            constants.SCALE_ONLY, pitch)))

            else:

                # If the pitch is 2mm or larger set the stroke-width to 10.

                svg.append("      stroke-width=\"10\"")

                # Hard code the start x and y to 1/2 stroke-width (5 in this
                # case as stroke-width is 10.) 

                svg.append("      x=\"5\"")

                svg.append("      y=\"5\"")

            # Save the value of height as a float as it is needed to calculate
            # the position of the pin0marker later.

            height = float(s_y(23.9, columns, pitch))

            print("height: {0:f}".format(height))

            svg.append("      height=\"{0:f}\"".format(height))

            svg.append("      width=\"" + s_x(18.51, rows, pitch) + "\"")

            svg.append("    />")

            # Now do the pin0marker (which needs the height from the rectangle
            # above which is why it is in this order!) 

            # Emit the starting silkscreen pin1 marker as this only happens
            # for pin 1.

            svg.append("    <line")
            svg.append("      id=\"pin0marker\"")
            svg.append("      stroke=\"#000000\"")

            print("silk: pitch {0:f}".format(pitch))

#            if pitch < constants.PITCH_2MM:

            if True:

                # If the pitch is less than 2MM, scale the stroke-width. 
                # This is to adjust the size of silkscreen < 2mm to make
                # the lines a reasonable size at lower pitches. 

                # Then emit the scaled stroke-width value. 

                svg.append("      stroke-width=\"" + str(stroke_width) + "\"") 

                # Set x1 to be 5 (1/2 the stroke-width) to set the start of
                # the pin0marker.

                svg.append("      x2=\"{0:f}\"".format(stroke_width))

                # Scale the x2 value according to the pitch

# may need adjustment as I think a straight scale may be too large!

                svg.append("      x1=\"" + s_x(5.19,
                                  constants.SCALE_ONLY, pitch) + "\"")

                # This is column 1 so hard code that. Use s_r_y() to
                # correctly place the line in multiple column case.

                svg.append("      y2=\"" + s_r_y(20.66, columns, 
                                        constants.SCALE_ONLY, pitch) + "\"")

                # *** correct later! ***
                # Set y2 to be 1/2 stroke width (5 in this case as
                # stroke-width is 10) plus the height of the rectangle 
                # which was saved from the rectangle def above. 

                svg.append("      y1=\"{0:f}\"".format(height + stroke_width))

                svg.append("    />")

            # silkscreen is done so close the group.

            svg.append("  </g>")

        else:

            print("part type {0:d} Not implemented yet".format(pad_type),
                   file=sys.stderr)

            exit(1)

        if svg_type == constants.PCB and pcb_type == constants.THT:

            # Create a copper1 group with a child copper0 group for THT.

            svg.append("  <g")

            svg.append("    id=\"copper1\">")

            svg.append("    <g")

            svg.append("      id=\"copper0\">")

        elif svg_type == constants.PCB and pcb_type == constants.SMD:

            # If this is PCB and SMD only create group copper1.

            svg.append("  <g")

            svg.append("    id=\"copper1\">")

        else:

            # Neither of the above is an error.

            print("Unknown pcb pad type {0:d}\n".format(pcb_type),
                                                 file=sys.stderr)

            exit(1)

    else:

        svg.append("    id=\"{0:s}\">".format(layerid))

    # connectors start at 0.

    connector = 0

    offset = 0

    if svg_type == constants.SCHEMATIC:

        # For schematic there needs to be an offset to separate rows
        # (basically one space added to row for each new column to separate
        # the rows.) The column is always 1 so the pins are all in line
        # vertically.

        if pin_order == constants.ROW:

            # Pin numbers increase by row (as opposed to across columns!)
            # so the pin numbers go up by row, but add 1 to the offset for
            # each column to provide a 1 space break between columns.

            for column in range(1, columns + 1):

                for row in range(1, rows + 1):

                    # The column in this call is set to 1 so the pins all 
                    # accend in x. Here the pin numbers 
                    # increase by column (as opposed to across rows!) So 
                    # calculate the offset to be

                    # offset = (column - 1 * rows) + row + column - 1 
                    # (which provides the spaces between rows)

                    # This provides the offset value to apply to each pin
                    # to write it at the correct place, providing 1 extra
                    # space between sets of rows. Use offset as the row value.

                    offset = ((column - 1) * (rows)) + row  + column - 1

                    print("\nSch row: rows {0:d} row {1:d} column {2:d} offset {3:d} connector {4:d}".format(rows, row, column, offset, connector))

                    svg, connectors = create_pin(svg, connectors, connector,
                                                 svg_type, part_type, columns,
                                                 offset, 1, pitch,
                                                 color, pcb_type, pad_type)
                    connector += 1

        else:

            # Pin numbers increase by column (as opposed to across rows!)
            # so the pin numbers go up by row, but add 1 to the offset for
            # each row to provide a 1 space break between columns.


            for row in range(1, rows + 1):

                for column in range(1, columns + 1):

                    # The column in this call is set to 1 so the pins all
                    # accend in x. Here the pin numbers increase by column
                    # (as opposed to across rows!) So calculate the offset
                    # to be

                    # offset = (column - 1 * rows) + column - 1 + row
                    # (which provides the spaces between rows)

                    offset = ((column - 1) * (rows)) + column - 1 + row

# *** remove me later! ***
#                    print("\nSch col: columns {0:d} column {1:d} row {2:d} offset {3:d} connector {4:d}".format(columns, column, row, offset, connector))

                    svg, connectors = create_pin(svg, connectors, connector,
                                                 svg_type, part_type, columns,
                                                 offset, 1, pitch, color, 
                                                 pcb_type, pad_type)

                    connector += 1

    else:

        if pin_order == constants.ROW:

            # Pin numbers increase by row (as opposed to across columns!)
            # column starts at 1 so the first pin has no y offset, the
            # second column (if there is one) will increase in y by
            # pitch and scale.

            for column in range(1, columns + 1):

                # row starts at 0 so the first pin has no x offset, the
                # second pin (if there is one) will increase in x by pitch
                # and scale.

                for row in range(1, rows + 1):

                    svg, connectors = create_pin(svg, connectors, connector,
                                                 svg_type, part_type, columns,
                                                 row, column, pitch, color,
                                                 pcb_type, pad_type)
                    connector += 1

            # For each column increase the offset by 1 to produce a
            # 1 element gap between rows.

            offset += 1

        else:

            # Pin numbers increase by column (as opposed to across rows!)
            # row starts at 0 so the first pin has no y offset, the second
            # row (if there is one) will increase in y by pitch and scale.

            for row in range(1, rows + 1):

                # column starts at 0 so the first pin has no y offset, the
                # second pin (if there is one) will decrease in y by pitch
                # and scale.

                for column in range(1, columns + 1):

                    svg, connectors = create_pin(svg, connectors, connector,
                                                 svg_type, part_type, columns,
                                                 row, column, pitch, color,
                                                 pcb_type, pad_type)
                    connector += 1

                # For each column increase the offset by 1 to produce a
                # 1 element gap between rows only in schematic.

                offset += 1

    # Append the connectors to the svg just before closing the svg.

    for connector in (connectors):

        svg.append(connector)

    if svg_type == constants.PCB and pcb_type == constants.THT:

        # there is a copper0 group so terminate it.

        svg.append("    </g>")

    # Terminate the group.

    svg.append("  </g>")

    # Then the svg group.

    svg.append("</svg>")

    return svg


def main():

    # Configure the root logging instance, even though we won't be using it
    # (we will create loggers for each module) as this is said to be best
    # practice.

    logging.basicConfig(
        stream=sys.stderr,
        format=' %(levelname)s: %(filename)s line %(lineno)d \n   %(message)s',
               level=logging.DEBUG)

    # Create a child logger for this routine.

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)

    # set test parameters

    rows = 4

    columns = 4

    part_type = constants.MALE_HEADER

    pitch = constants.PITCH_0_5MM

#    pitch = constants.PITCH_1MM

#    pitch = constants.PITCH_1_27MM

#    pitch = constants.PITCH_2MM

#
#    pitch = constants.PITCH_0_1IN
#    pitch = constants.PITCH_0_11IN
#    pitch = constants.PITCH_0_12IN
#    pitch = constants.PITCH_0_13IN
#    pitch = constants.PITCH_0_14IN
#    pitch = constants.PITCH_0_15IN
#    pitch = constants.PITCH_0_16IN
#    pitch = constants.PITCH_0_17IN
#    pitch = constants.PITCH_0_18IN
#    pitch = constants.PITCH_0_19IN

#
#    pitch = constants.PITCH_0_156IN

#    pitch = constants.PITCH_0_2IN

#    pitch = constants.PITCH_1IN

    pcb_type = constants.THT

    pad_type = constants.CIRCLE

    pin_order = constants.COLUMN

#    pin_order = constants.ROW

    color = constants.BRN

    ref_file = constants.MALE_HEADER_BREADBOARD_REFERENCE_FILE

    moduleid = create_fzp(part_type, rows, columns, pitch, pcb_type,
                          pin_order, pad_type, color, 1)

    # Create the breadboard svg.

    svg_type = constants.BREADBOARD

    ref_file = constants.MALE_HEADER_BREADBOARD_REFERENCE_FILE

    layerid = constants.BREADBOARD

    svg = []

    svg = create_svg(svg_type, moduleid, part_type, rows, columns, pitch,
                     pcb_type, pin_order, pad_type, color, ref_file, layerid)

    breadboard_filename = 'svg.breadboard.test_breadboard.svg'

    # breakpoint()

    write_file(breadboard_filename, svg)

    svg_type = constants.SCHEMATIC

    ref_file = constants.MALE_HEADER_SCHEMATIC_REFERENCE_FILE

    layerid = constants.SCHEMATIC

    # Schematic is always pitch 0.1IN so set it expicitly.

    svg = []

    svg = create_svg(svg_type, moduleid, part_type, rows, columns,
                     constants.PITCH_0_1IN, pcb_type, pin_order, pad_type,
                     color, ref_file, layerid)

    schematic_filename = 'svg.schematic.test_schematic.svg'

    # breakpoint()

    write_file(schematic_filename, svg)

    svg_type = constants.PCB

    if pad_type == constants.CIRCLE:

        ref_file = constants.CIRCLE_PCB_REFERENCE_FILE

    elif pad_type == constants.OBLONG:

        ref_file = constants.OBLONG_PCB_REFERENCE_FILE

    else:

        print("Unknown pcb pad type\n", file=sys.stderr)

        exit(1)

    layerid = ""    # pcb has 3 layerIds not only 1!

    svg = []

    svg = create_svg(svg_type, moduleid, part_type, rows, columns, pitch,
                     pcb_type, pin_order, pad_type, color, ref_file, layerid)

    pcb_filename = 'svg.pcb.test_pcb.svg'

    # breakpoint()

    write_file(pcb_filename, svg)

    exit(0)


if __name__ == "__main__":
    main()
