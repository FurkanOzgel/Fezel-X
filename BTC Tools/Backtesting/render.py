import pandas as pd

df = pd.read_csv("Rendered_Data_Daily.csv")
df.set_index("Index", inplace=True)

df.insert(4,"Percentage",[ x[1].Future*100/x[1].now - 100 
                          for x in df.iterrows() ] ,True )

df.to_csv("Rendered_Data_Daily.csv")