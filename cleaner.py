
file = "/home/mubeen/Downloads/Instagram-Emails-Mastersheet-Name_email.csv"
with open(file, 'r') as f:
    L = f.readlines()

cleaned = []

count = 0
for i in L:
    l = i.strip("\n").split(",")
    temp = []
    count += 1
    
    for j in l:
        if len(j) > 2:
            temp.append(j)
    if len(temp)  >= 2:
        cleaned.append(temp)


with open(file, 'w') as f:
    for i in cleaned:
        f.writelines(",".join(i)+"\n")



