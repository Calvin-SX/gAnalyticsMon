import pandas as pd

def sort_logs(file):
    data = pd.read_csv(file,usecols = ["CLIENT"])


    def filter_colons(ip):
        return ip[:ip.index(":")]

    set1 = set()

    for ip in data["CLIENT"]:
        set1.add(filter_colons(ip))
    
    list1 = list(set1)
 
    return list1

if __name__ == "__main__":
    data = sort_logs("bcec-logs-2024-06-08T13_14_25.csv")
    print(data)