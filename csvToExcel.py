import pandas as pd
df_new = pd.read_csv(r'C:\Users\Shamanth kumar HP\Desktop\WebD\testing\dataSheetsCSV\Byappanahalli\camera1.csv')  
GFG = pd.ExcelWriter(r'C:\Users\Shamanth kumar HP\Desktop\WebD\testing\dataSheetsCSV\Byappanahalli\camera1.xlsx')
df_new.to_excel(GFG, index = False)  
GFG.save()
print("csv to excel converted")