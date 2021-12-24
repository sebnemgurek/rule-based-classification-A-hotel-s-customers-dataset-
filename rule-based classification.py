
#importing libraries
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

#reading data
df_ = pd.read_excel("hotel_customer/HotelCustomersDataset.xlsx")
df = df_.copy()
df.head()

#general information about the dataset
df.shape
df.info()
df.columns


#Descriptive statistics of the dataset
df.describe().T


#Sum of missing observations in the data set
df.isnull().sum()


#removing missing observations from the dataset
df.dropna(inplace=True)
df.isnull().sum()


#Customers make two kinds of expenses: accommodation expenses and other expenses.
#Total amount customers spend at the hotel

df["Total_revenue"]=df["LodgingRevenue"]+df["OtherRevenue"]
df=df[df["Total_revenue"]>0]


#Unique number of customers
#DocIDHash: ID document number provided by the customer at check-in (passport number, national ID card number or other)
#NameHash:Customer's name
#When we looked at the unique values of both, I saw that they were not the same.
#Maybe there are two different people with the same name and surname.
#I continued to work by choosing DocIDHash.

df["DocIDHash"].nunique()  #ikisi farklı  76760
df["NameHash"].nunique()  #77375


#Reservation frequencies by country
#Information on how many people from which country stayed at the hotel

df["Nationality"].value_counts().sort_values(ascending=False).head()


#We grouped customers by country and found out how much these customers with similar characteristics (from the same country) spent on average.

df.groupby(['Nationality'])['Total_revenue'].agg('mean').head(10)


#Segment customers by their total spend

df["Segment"]=pd.qcut(df['Total_revenue'], 4, labels=['D','C','B','A'])
df[["Segment","Total_revenue"]].groupby("Segment").agg(["mean","min","max","sum"])


#Average of total revenues in Nationality' and 'DistributionChannel' breakdown
#We grouped customers by country and distribution channel used to book the hotel.
#We found out how much these similar customers spend on average at the hotel.

agg_df =pd.DataFrame(df.groupby(['Nationality','DistributionChannel'])['Total_revenue'].agg('mean')).round(2).sort_values("Total_revenue")
agg_df.head(20)
agg_df=agg_df.reset_index()
agg_df.head()


#Identifying new level-based customers (personas)
#We created a new persona according to the country and distribution channel information from the demographic information in the data set.

agg_df['customers_level_based'] = [str(row[0]).upper()+'_'+str(row[1]).upper() for row in agg_df.values]
agg_df = agg_df[["customers_level_based","Total_revenue"]].groupby("customers_level_based").agg("mean").round(2)
agg_df=agg_df.reset_index()
agg_df.head()


#Categorize new customers by segment and predict how much revenue they can generate
#For example: We found the information about how much a person whose country is BRAZIL and who makes a hotel reservation on average spends at the hotel.

new_user='BRA_DIRECT'
agg_df[agg_df["customers_level_based"] == new_user]