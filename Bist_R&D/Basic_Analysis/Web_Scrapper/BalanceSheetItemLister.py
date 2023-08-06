import BalanceSheet

bilanco_date = BalanceSheet.get_finance_data_dates("ODAS")[0].split("/")
bilanco_df = BalanceSheet.get_financal_tables("ODAS", bilanco_date[0], bilanco_date[1])

for i,row in bilanco_df.iterrows():
    print(i+ " " +row.ItemCode)