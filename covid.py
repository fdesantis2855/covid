#!/usr/bin/env python
import csv 

def main():
   with open("3-10-2020.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        
                

if __name__ == "__main__":
    main()
