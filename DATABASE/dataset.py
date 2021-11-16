import pandas as pd
import time


df = pd.read_excel ('DBPrueba.xlsx', sheet_name='data')
df.sensor_id = df.sensor_id.astype(int)
df.data = df.data.astype(str)
print (df.dtypes)


new_df= pd.concat([pd.Series(row['sensor_id'], row['data'].split(", ["))              
                 for _, row in df.iterrows()], names= ['data','sensor_id'])


print(new_df)
new_df.to_excel("output.xlsx")
#df2 = pd.DataFrame(df['data'].values.tolist(), ).stack().reset_index(level=0)

#print(df2)

#df1[['timestamp','value']]= pd.DataFrame(df1.data.toList(), index=df1.sensor_id)
#for index, row in df.iterrows():
#    new_row = row['data'].split()



#new_df= pd.concat([pd.Series(row['sensor_id'], row['data'].split("],["))              
                #   for _, row in df.iterrows()]).reset_index()
#print(new_df)






#df['data'] = df['data'].map(list)




#print (df_c.dtypes)






