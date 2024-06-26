import pandas as pd

# It was assumed that there would only be one ip adress for each line
# As a result of this, this would be a limitation for the code


def sort_logs(file):
    data = pd.read_csv(file,usecols = ["CLIENT"])


    def filter_colons(ip):
        if ":" in ip:
            return ip[:ip.index(":")]
        else:
            return ip

    set1 = set()

    for ip in data["CLIENT"]:
        set1.add(filter_colons(ip))
    
    list1 = list(set1)
 
    return list1

if __name__ == "__main__":
    data = sort_logs("testdata/test.csv")
    print(data)