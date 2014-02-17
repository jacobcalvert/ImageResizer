###########################################
# File:         ImageResizer.py
# Rev:          1.0
# Usage:        ''
# Dependencies: Image, os, sys, time
###########################################
import Image
import os
import sys
import time


EXTS = [".jpg", ".png", ".gif", ".tiff"]
TESTING = 0

def main():
    if len(sys.argv) == 4:
        source_folder = sys.argv[1]
        destination_folder = sys.argv[2]
        scale = float(sys.argv[3])
        if not os.path.exists(source_folder):
            print "ERROR: Source not found."
            return
        if not os.path.exists(destination_folder):
            print "Warning: Destination folder not found, creating it."
            os.makedirs(destination_folder)
        work_loop(source_folder, destination_folder, scale)
    else:
        usage()


def usage():
    print "ImageResizer.py src_dir dest_dir scale"
    print "EX: 'ImageResizer.py ./in/ ./out/ 0.6' would resize all images in 'in' down to 60% and put them in 'out'"


def scan_dir(src_dir):
    files = os.listdir(src_dir)
    for f in files:
        for ext in EXTS:
            if not f.lower().endswith(ext):
                files.remove(f)
    return files


def work_loop(source, destination, scale):
    files = scan_dir(source)
    t0 = time.time()
    for f in files:
        src = source+"/"+f
        dst = destination+"/" + f

        resize(src, dst, scale)


def get_source_folder():
    pass # TODO: add a tK gui folder browser


def get_destination_folder():
    pass # TODO: add a tK gui folder browser


def resize(src, dest, scale=0.5):
    orig = Image.open(src)

    w = orig.size[0]*scale
    h = orig.size[1]*scale

    new_img = orig.resize((w, h), Image.ANTIALIAS)

    new_img.save(dest)


def ftime(t):
    m, s = 0, 0
    if t > 59:
        m = t/60
        s = t - m*60
        return "%dm%ds" % (m, s)
    else:
        return "0m%ds" % (t)


def info_callback(t0, i, t, fn):
    delta_t = int(time.time() - t0)
    os.system("clear")  # TODO: check for WIN32 or Linux, should be either 'cls' or clear
    pct = (i/float(t))*100
    print "Job Info"
    print "     %-30s %s" % ("Current File: ", fn)
    print "     %-30s %.2f%%" % ("Percent Complete: ", pct)
    print "     %-30s %s" % ("Elapsed Time: ", ftime(delta_t))
    print "     %-30s %s" % ("Estimated time to completion: ", "Not implemented")  # TODO: take avg of each file, estimate ETA


def tests():
    if test_ftime():
        print "ftime() passed."
    print "------------------VISUAL VERIFICATION---------------------------"
    info_callback(time.time() - 100, 2, 125, "test-file.ext")


def test_ftime():
    if ftime(100) == "1m40s":
        return True

if TESTING == 1:
    tests()
else:
    main()