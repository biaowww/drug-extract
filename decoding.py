# -*- coding: utf-8 -*-

import csv 

def main():
    with open('item.csv',"r") as csvfile:
            itemreader = csv.reader(csvfile)
            for row in itemreader:
                print ', '.join([i.decode('utf-8', errors='ignore').encode('utf-8', errors='ignore') for i in row])

if __name__ == '__main__':
    main()