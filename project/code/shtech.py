#!/usr/bin/env python3
from data_source import flightaware_crawler as crl

interval = 10
max_loop = 5
save = True
display = True
display_num = 5
filename = crl.kDefaultPath

if __name__ == "__main__":
    import sys
    import getopt
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hm:i:s:d:n",
            ["help", "maxloop=", "interval=", "saveto=", "display=", "nosave"])
    except getopt.GetoptError:
        print("Error: Invalid Syntax, enter shtech.py -h or shtech.py --help"
              "for more information")
    try:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(
                    "-i <time>, --interval=<time>\n  "
                    "set an interval to crawl the "
                    "website. The value would be set to 1 if the input time "
                    "is less than 1. Default is 10.\n\n"
                    "-s <filename>, --saveto=<filename>\n  "
                    "Give a file to save the data, it should be a json file."
                    "Omitt the option indicates that the data will"
                    " be stored in default file. (/tmp/data.json)\n"
                    "\n"
                    "-n, --nosave\n"
                    "Ask the program not to save the data. This will override"
                    " -s\n\n"
                    "-m <loops>, --maxloop=<loops>\n  "
                    "Give a number of loop times. If loops is less or equal"
                    " to 0, then the program will loop infinite times."
                    "Default the times of looping is 5.\n\n"
                    "-d <number>, --display=<number>\n  "
                    "Give a number of items to display. If the number is "
                    "less or equal to 0, then the data won't be diplayed. "
                    "Default is 5 items")
                sys.exit()
            if opt in ("-i", "--interval"):
                interval = max(float(arg), 1)
            if opt in ("-s", "--saveto"):
                filename = arg
            if opt in ("-m", "--maxloop"):
                max_loop = None if int(arg) <= 0 else int(arg)
            if opt in ("-d", "--display"):
                display_num = int(arg)
                if display_num <= 0:
                    display = False
            if opt in ("-n", "--nosave"):
                save = False

    except ValueError:
        print("Inalid input. <time>, <loops> and <number> should be integers.")
        sys.exit()

# 31.17940N, 121.59043E
kLatitude = 31.17940
kLongitude = 121.59043
shtech_crawler = crl.FlightAwareCrawler((kLatitude, kLongitude),
                                        (kLatitude + 1.5, kLongitude - 1.5))

shtech_crawler.spin(interval=interval,
                    max_loop=max_loop,
                    save=save,
                    filename=filename,
                    display=display,
                    display_num=display_num)
