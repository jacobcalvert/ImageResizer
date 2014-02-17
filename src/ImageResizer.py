###########################################
# File:     ImageResizer.py
# Rev:      1.0
# Usage:    ''
#
###########################################
import Image
import os
import sys
import time

EXTS = [".jpg", ".png", ".gif", ".tiff"]

def main():
    if len(sys.argv) == 3:
        source_folder = sys.argv[1]
        destination_folder = sys.argv[2]
        work_loop(source_folder, destination_folder, 0.5)
    else:
        pass


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


def test():
    print ftime(100)
    info_callback(time.time() - 100, 2, 125, "test-file.ext")

test()