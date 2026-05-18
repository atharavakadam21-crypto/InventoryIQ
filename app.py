import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load dataset
df = pd.read_csv("retail_store_inventory.csv")

# Convert date
df['Date'] = pd.to_datetime(df['Date'])

# Convert categorical columns
df = pd.get_dummies(df, columns=[
    'Category',
    'Region',
    'Weather Condition',
    'Seasonality'
])

# Features
X = df.drop(columns=[
    'Units Sold',
    'Date',
    'Store ID',
    'Product ID'
])

# Target
y = df['Units Sold']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=50,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Error
error = mean_absolute_error(y_test, predictions)

print("Mean Absolute Error:", round(error, 2))

# Graph
plt.figure(figsize=(12,6))

plt.plot(
    y_test.values[:100],
    label='Actual Sales'
)

plt.plot(
    predictions[:100],
    label='Predicted Sales'
)

plt.title("Actual vs Predicted Sales")

plt.xlabel("Data Points")
plt.ylabel("Units Sold")

plt.legend()

plt.grid(True)

plt.show()