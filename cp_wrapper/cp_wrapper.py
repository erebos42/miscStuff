#!/usr/bin/python

#####
# cp_wrapper, cp wrapper that adds a progress bar to the cp command
#
# Copyright 2012, erebos42 (https://github.com/erebos42/miscScripts)
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of
# the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this software; if not, write to the Free
# Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA, or see the FSF site: http://www.fsf.org.
#####

# TODO:
# - parse flags dynamically

import os
import sys
import subprocess
import string
import time
from datetime import datetime
from datetime import timedelta

def main():
    flags = ""
    src = ""
    dest = ""

    # parse sys.argv[]
    if (len(sys.argv) == 3):
        src = sys.argv[1]
        dest = sys.argv[2]
    elif (len(sys.argv) == 4):
        flags = sys.argv[1]
        src = sys.argv[2]
        dest = sys.argv[3]
    else:
        print "usage:"
        print "python cp_wrapper -FLAGS src dest"
        print "Flags must be all without spaces between them..."

    command = "cp " + flags + " " + src + " " + dest + " &"
#    print command
    os.system(command)

    srcsize = os.stat(src)

    proc1 = subprocess.Popen(["ps -Af | grep -m1 \"" + command + "\" | awk '{print $2}'"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc1.communicate()
    # TODO: THIS IS NOT GOOD! WHY IS THE PID ALWAYS OFF BY ONE???
    pid = int(out) - 1
#    print "pid: " + str(pid)

    try:
        keepgoing = True
        # TODO: destsize should be initialized with an os.stat object with 0 bytes size. Quick Hack: use /dev/zero instead
        destsize = os.stat("/dev/zero")
        cptime = datetime.now()
        while (keepgoing):
            cmd = "ps -p " + string.strip(str(pid),"\n") + " | wc -l"
            proc2 = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
            (temp, err) = proc2.communicate()
            temp = int(temp)
            if (temp != 2):
                keepgoing = False

            # calc values and output infos
            destsizeold = destsize
            destsize = os.stat(dest)
            cptimeold = cptime
            cptime = datetime.now()

            # TODO: calc est. time
#            temp1 = srcsize.st_size + destsize.st_size
#            temp2 = destsize.st_size + destsizeold.st_size
#            temp3 = (cptime - cptimeold).total_seconds()
#            if (temp1 == 0):
#                temp1 = LONG_MIN
#            if (temp2 == 0):
#                temp2 = LONG_MIN
#            if (temp3 == 0):
#                temp3 = LONG_MIN
#            temp4 = (temp1 / temp2) * temp3            

            percent = (destsize.st_size * 100) / srcsize.st_size

            out = "["
            for x in range(0, (percent / 2)):
                out += "#"
            for x in range((percent / 2), 50):
                out += "-"

            out += "] "

            formattedpercent = "%03s" % (percent)
#            print out + str(formattedpercent) + " %  " + str(temp4)
            print out + str(formattedpercent) + " %  "

            # sleep
            time.sleep(0.25)
    except KeyboardInterrupt:
        os.system("kill " + str(pid))
        sys.exit(0)

#print "Start!"
main()
#print "Done!"
