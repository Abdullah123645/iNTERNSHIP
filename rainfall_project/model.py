import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Load dataset
df = pd.read_csv("rainfall.csv")

df['rainfall'] = df['rainfall'].map({'yes':1,'no':0})

# Drop correlated features
df = df.drop(['max_temp','min_temp'], axis=1)

# Features & Target
X = df[['pressure','humidity','dew_point','cloud',
        'sunshine','wind_direction','wind_speed']] 
# Target
y = df['rainfall']


# Split
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42)


# Train SVC Model
model = SVC()
model.fit(X_train, y_train)

# Prediction Function
import pandas as pd

def predict_rain(input_data):
    columns = ['pressure','humidity','dew_point','cloud',
               'sunshine','wind_direction','wind_speed']

    input_df = pd.DataFrame([input_data], columns=columns)

    return model.predict(input_df)[0]