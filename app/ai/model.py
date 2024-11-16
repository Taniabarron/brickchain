import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Simulate or load data
data = pd.DataFrame({
    'property_type': ['house', 'apartment', 'land', 'house', 'land'],
    'valuation': [500000, 350000, 200000, 450000, 150000],
    'tokens': [10, 5, 20, 8, 15],
    'publish_price': [520000, 360000, 210000, 460000, 155000],
    'auction': [True, False, False, True, False],
    #'location_score': [8.5, 7.2, 5.8, 8.0, 4.9],
    #'days_on_market': [30, 45, 60, 25, 90],
    'final_price': [510000, 355000, 205000, 455000, 150000],
})

# Separate characteristics and target variable
X = data.drop(columns=['final_price'])
y = data['final_price']

# Divide into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Data preprocessing
# Identify categorical and numeric columns
categorical_features = ['property_type', 'auction']
numerical_features = ['valuation', 'tokens', 'publish_price']
#numerical_features = ['valuation', 'tokens', 'publish_price', 'location_score', 'days_on_market']

# Create transformer for preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),  
        ('cat', OneHotEncoder(), categorical_features) 
    ]
)

# Create pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor), 
    ('model', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Training the model
pipeline.fit(X_train, y_train)

# Making predictions
y_pred = pipeline.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("Predicciones:", y_pred)
print(f"Mean Squared Error: {mse}")
