import csv

with open("test.csv") as file:
  reader=csv.DictReader(file)
  for line in reader:
    print int(line["motion"])*int(line["sound"])
