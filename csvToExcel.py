import pandas as pd
df_new = pd.read_csv(r'C:\Users\Shamanth kumar HP\Desktop\WebD\FinalYearProject\csvFiles\URS_road\camera1.csv')  
GFG = pd.ExcelWriter(r'C:\Users\Shamanth kumar HP\Desktop\WebD\FinalYearProject\csvFiles\URS_road\camera1.xlsx')


df_new.to_excel(GFG, index = False)  
GFG.save()
#dd = pd.read_csv(r"C:\Users\Shamanth kumar HP\Desktop\real.csv")

print("csv to excel converted")