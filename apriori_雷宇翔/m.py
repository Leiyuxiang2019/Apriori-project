def preprocess(filename1,filename2):
   f1=open(filename2,'w')
   with open(filename1, 'r')as f:
      for line in f:
       line=line.replace('"', '')
       line=line.replace('{', '')
       line=line.replace('}', '')
       words = line.strip().split(',')
       for i in range(len(words)-2):
             f1.write(words[i+1]+',')
       f1.write(words[-1])
       f1.write("\n")
       print(words)
   f.close()

preprocess("Groceries.csv", "after.csv")