import csv
import os

def appendData(csvPathName, headers, data_dict):
    exist = os.path.exists(csvPathName)
    with open(csvPathName, 'a+', newline='', encoding="utf-8") as f:
        try:
            writer = csv.DictWriter(f, headers)
            if not exist:
                writer.writeheader()

            if type(data_dict) == type([]):
                writer.writerows(data_dict)
            else:
                writer.writerow(data_dict)

        except Exception as e:
            print(e)
        finally:
            data_dict = []

def clearData(csvPathName):
    try:
        os.remove(csvPathName)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    appendData("a.csv", ["f1", "f2"], [{'f1':3, 'f2':5},{'f1':5, 'f2':3}])
    appendData("a.csv", ["f1", "f2"], {'f1':4, 'f2':4})
    clearData("b.csv")
    with open("wxinfo.csv", 'r+', newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print(type(reader))
        for line in reader:
            print("---", line["imgs"])