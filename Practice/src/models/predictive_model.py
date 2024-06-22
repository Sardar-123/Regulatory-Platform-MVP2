import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

class ImpactPredictor:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.trained = False

    def load_data(self, filepath):
        """
        Load historical impact data from a JSON file.
        """
        with open(filepath, 'r') as file:
            data = json.load(file)

        df = pd.DataFrame(data)
        return df

    def train_model(self, data):
        """
        Train the predictive model using historical impact data.
        """
        X = data.drop(columns='impact')
        y = data['impact']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model trained with accuracy: {accuracy}")

        self.trained = True

    def predict_impact(self, new_data):
        """
        Predict the impact of new changes using the trained model.
        """
        if not self.trained:
            raise Exception("Model is not trained. Train the model before making predictions.")

        prediction = self.model.predict(new_data)
        return prediction

# Example usage
if __name__ == '__main__':
    predictor = ImpactPredictor()
    historical_data = predictor.load_data('data/impacts/historical_impacts.json')
    predictor.train_model(historical_data)

    # Example new data for prediction
    new_data = pd.DataFrame([{
        'feature1': value1,
        'feature2': value2,
        # Add all relevant features here
    }])

    predicted_impact = predictor.predict_impact(new_data)
    print(f"Predicted impact: {predicted_impact}")
