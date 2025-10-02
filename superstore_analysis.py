## 1. Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(
    style='whitegrid',
    rc={
        'figure.figsize': (12,6),
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12
    }
)
## 2. Load and prepare the data
# 2.1 Load dataset
df = pd.read_csv("Sample - Superstore.csv", encoding="cp1250")

# 2.2 Convert date columns
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"], errors="coerce")

# 2.3 Basic info
print(df.head(3))
print(df.info())
print(df.isnull().sum())
print("Number of duplicate Row IDs:", df['Row ID'].duplicated().sum())

# 2.4 Date range
print("Earliest order date:", df['Order Date'].min())
print("Latest order date:", df['Order Date'].max())

## 3. Exploratory Data Analysis

# 3.1 Monthly Sales
monthly_sales = df.set_index('Order Date')['Sales'].resample('ME').sum()

fig, ax = plt.subplots()
ax.plot(monthly_sales, marker='o')
ax.set_title('Monthly Sales')
ax.set_xlabel('Date')
ax.set_ylabel('Sales')
ax.grid(True)
plt.show()

# 3.2 Sales by Category
fig, ax = plt.subplots()
sns.barplot(x=df['Category'], y=df['Sales'], estimator=sum, ax=ax)
ax.set_title('Sales by Category')
ax.set_xlabel('Category')
ax.set_ylabel('Sales')
plt.show()

# 3.3 Sales by Sub-Category
top_subcat = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
sns.barplot(x=top_subcat.index, y=top_subcat.values, ax=ax)
ax.set_title('Sales by Sub-Category')
ax.set_xlabel('Sub-Category')
ax.set_ylabel('Sales')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
plt.show()

# 3.4 Profit by Category and Region

# 3.4.1 Profit by category
profit_by_category = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
profit_by_category.plot(kind='bar', color='green')
plt.title('Profit by Category')
plt.show()

# 3.4.2 Profit by region
profit_by_region = df.groupby('Region')['Profit'].sum()
profit_by_region.plot(kind='pie', autopct='%1.1f%%')
plt.title('Profit by Region')
plt.ylabel('')
plt.show()

# 4. Correlation Analysis
corr = df[['Sales','Profit','Quantity']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# 5. Deep-Dive Analyses

# 5.1 Discount Impact on Profit
discount_profit = df.groupby('Discount')['Profit'].mean()
plt.plot(discount_profit.index, discount_profit.values, marker='o')
plt.title("Average Profit vs Discount Level")
plt.xlabel("Discount")
plt.ylabel("Average Profit")
plt.show()

# 5.2 Sales by Day of Week
df['Order Day'] = df['Order Date'].dt.day_name()  ##not needed in .ipynb

order_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']  
fig_day, ax_day = plt.subplots()
sns.barplot(
    x='Order Day',
    y='Sales',
    data=df,
    estimator=sum,
    order=order_days,
    ax=ax_day,
    errorbar=None
)
ax_day.set_title('Sales by Day of the Week')
ax_day.set_xlabel('Day of the Week')
ax_day.set_ylabel('Sales')

plt.show()

# 5.3 Shipping Mode Analysis

shipping_sales = df.groupby('Ship Mode')['Sales'].sum()
shipping_profit = df.groupby('Ship Mode')['Profit'].sum()

fig, ax = plt.subplots()
shipping_sales.plot(kind='bar', color='lightgreen', ax=ax)
ax.set_ylabel("Sales")
ax.set_title("Sales by Shipping Mode")
plt.show()

fig, ax = plt.subplots()
shipping_profit.plot(kind='bar', color='orange', ax=ax)
ax.set_ylabel("Profit")
ax.set_title("Profit by Shipping Mode")
plt.show()

# 5.4 Top Customers by Profit

top_customers = df.groupby('Customer Name')['Profit'].sum().sort_values(ascending=False).head(10)
top_customers.plot(kind='barh', color='green')
plt.title("Top 10 Customers by Profit")
plt.xlabel("Profit")
plt.gca().invert_yaxis()
plt.show()

# 5.5 Underperforming Products
# 5.5.1 By sales value
sales_by_product = df.groupby('Product Name')['Sales'].sum()
lowest_sales = sales_by_product.nsmallest(10)
lowest_sales.plot(kind='barh', color='red')
plt.xlabel('Sales')
plt.title('10 Products with Lowest Sales (Value)')
plt.gca().invert_yaxis()
plt.show()

# 5.5.2 By quantity
sales_by_product_qty = df.groupby('Product Name')['Quantity'].sum()
lowest_qty = sales_by_product_qty.nsmallest(10)
lowest_qty.plot(kind='barh', color='red')
plt.xlabel('Quantity')
plt.title('10 Products with Lowest Sales (Quantity)')
plt.gca().invert_yaxis()
plt.show()


