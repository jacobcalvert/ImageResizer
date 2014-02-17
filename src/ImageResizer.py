###########################################
# File:         ImageResizer.py
# Rev:          1.0
# Usage:        'ImageResizer.py src_dir dest_dir scale'
# Dependencies: Image, os, sys, time
###########################################
import Image
import os
import sys
import time


TESTING = 0

EXTS = [".jpg", ".png", ".gif", ".tiff", ".bmp"]
AVG = 0
AVG_FULL = []
PLATFORM = None
CLS_PARAMS = {"nt": "cls", "posix": "clear"}
CLS = None


def main():
    setup_params()
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
    new_files = []
    for f in files:
        for ext in EXTS:
            if f.lower().endswith(ext):
                new_files.append(f)
    return new_files


def work_loop(source, destination, scale):
    files = scan_dir(source)
    t0 = time.time()
    i = 1
    t = len(files)
    for f in files:
        src = source+"/"+f
        dst = destination+"/" + f
        info_callback(t0, i, t, f, AVG)
        i += 1
        resize(src, dst, scale)


def get_source_folder():
    pass # TODO: add a tK gui folder browser


def get_destination_folder():
    pass # TODO: add a tK gui folder browser


def resize(src, dest, scale=0.5):
    t0 = time.time()
    orig = Image.open(src)
    w = int(orig.size[0]*scale)
    h = int(orig.size[1]*scale)

    new_img = orig.resize((w, h), Image.ANTIALIAS)

    new_img.save(dest)
    calc_avg(t0, time.time())

def ftime(t):
    m, s = 0, 0
    if t > 59:
        m = t/60
        s = t - m*60
        return "%dm%ds" % (m, s)
    else:
        return "0m%ds" % (t)


def info_callback(t0, i, t, fn, avg):
    delta_t = int(time.time() - t0)
    os.system(CLS)
    pct = (i/float(t))*100
    print "Job Info"
    print "     %-30s %-20s (file %d of %d)" % ("Current File: ", fn, i, t)
    print "     %-30s %.2f%%" % ("Percent Complete: ", pct)
    print "     %-30s %s" % ("Elapsed Time: ", ftime(delta_t))
    print "     %-30s %s" % ("Estimated time to completion: ", time_to_completion(t-i))
    print "     %-30s %.2fs" % ("Average time per file: ", avg)


def time_to_completion(left):
    return ftime(int(AVG*left))


def calc_avg(t0, t1):
    global AVG, AVG_FULL
    AVG_FULL.append(t1-t0)
    AVG = sum(AVG_FULL)/float(len(AVG_FULL))


def setup_params():
    global PLATFORM, CLS, CLS_PARAMS
    PLATFORM = os.name
    CLS = CLS_PARAMS[PLATFORM]


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