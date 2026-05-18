import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load dataset

df = pd.read_csv("retail_store_inventory.csv")

# Convert date

df['Date'] = pd.to_datetime(df['Date'])

# Feature engineering

df['Month'] = df['Date'].dt.month

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

# Train test split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train

model.fit(X_train, y_train)

# Save model

joblib.dump(model, 'forecast_model.pkl')

print("Model trained and saved successfully!")