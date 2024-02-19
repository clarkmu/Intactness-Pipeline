import intactness
import sys
# import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-e", "--email", help="Email to receive results")
parser.add_argument("-f", "--format", help="Format PDFs as 'circular' (default 'bar')")

args = parser.parse_args()

EMAIL = args.email

intactness().init()

# print("Email", args.email)