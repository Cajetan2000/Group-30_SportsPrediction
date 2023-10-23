# -*- coding: utf-8 -*-
"""Group 30_SportsPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qhyVdKOcsNA4MzniXvw9dhmVhrtwkQi9

# **This project is about building models that predict a player's overall rating given the player's profile.**

**Importing Libraries**
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from google.colab import drive
drive.mount('/content/drive')



"""**Reading the data used for training the model.**



"""

Training_Data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/players_21.csv')

"""**Reading the data used for testing the model.**"""

Testing_Data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/players_22.csv')

"""**Irrelivant attributes list**"""

Attributes_to_drop = ['sofifa_id', 'player_url', 'short_name', 'long_name', 'club_team_id', 'club_name', 'league_name', 'player_face_url', 'club_logo_url', 'club_flag_url', 'nation_logo_url', 'nation_flag_url', 'club_jersey_number', 'club_loaned_from', 'club_joined','club_contract_valid_until', 'nationality_id', 'nationality_name', 'nation_team_id', 'nation_jersey_number', 'preferred_foot', 'weak_foot', 'dob', 'height_cm', 'international_reputation', 'body_type', 'real_face', 'player_tags', 'player_traits']

"""**Selected artributes to check for NaNs(Training data)**"""

Training_Data = Training_Data.drop(Attributes_to_drop, axis = 1)



"""**Selected artributes to check for NaNs(Testing data)**"""

Testing_Data = Testing_Data.drop(Attributes_to_drop, axis = 1)

"""**Removing attributes with more than 30 % null values(Training Data).**"""

# Removing attributes with more than 30 % null values.
Condition = 0.7 * len(Training_Data)
Filtered_Training_Data = Training_Data.dropna(thresh = Condition, axis=1)

"""**Removing attributes with more than 30 % null values(Training Data).**"""

Condition = 0.7 * len(Testing_Data)
Filtered_Testing_Data = Testing_Data.dropna(thresh = Condition, axis=1)

"""**Imputing null values of both training and testing data using forward fill**"""

Filtered_Training_Data.fillna(method = 'ffill', inplace = True)
Filtered_Testing_Data.fillna(method = 'ffill', inplace = True)

pd.options.display.max_columns = None

Filtered_Training_Data

Filtered_Testing_Data

"""**A list containing non-numeric attributes to be encoded**"""

Attributes_To_be_Encoded = ['player_positions', 'club_position', 'work_rate', 'ls', 'st', 'rs', 'lw',	'lf',	'cf', 'rf',	'rw',	'lam',	'cam',	'ram',	'lm',	'lcm',	'cm',	'rcm',	'rm',	'lwb',	'ldm',	'cdm',	'rdm',	'rwb',	'lb',	'lcb',	'cb',	'rcb',	'rb',	'gk']

"""**Encoding the non-numeric attributes in the training data frame.**"""

for non_numeric_attribute in Attributes_To_be_Encoded:
  Filtered_Training_Data[non_numeric_attribute],_=pd.factorize(Filtered_Training_Data[non_numeric_attribute])

Filtered_Training_Data

"""**Encoding the non-numeric attributes in the testing data frame.**"""

for non_numeric_attribute in Attributes_To_be_Encoded:
  Filtered_Testing_Data[non_numeric_attribute],_=pd.factorize(Filtered_Testing_Data[non_numeric_attribute])

Filtered_Testing_Data

"""**Spliting data into Input_training(X) and Output_training(Y) for feature inportance test.**"""

Input_Training = Filtered_Training_Data.drop('overall', axis = 1)
Output_Training = pd.DataFrame(Filtered_Training_Data['overall'], columns = ['overall'])

Input_Training_Attribute = Input_Training.columns

"""**Training XGBRegressor model for feture importance testand printing the output**"""

from xgboost import XGBRegressor
from xgboost import plot_importance
from matplotlib import pyplot


# fit model no training data
model = XGBRegressor()
model.fit(Input_Training, Output_Training)
# plot feature importance
importances = model.feature_importances_


# Print or use feature importances
sorted_indices = np.argsort(importances)[::-1]
for index in sorted_indices:
   print(f"'{Input_Training_Attribute[index]}', '{importances[index]}'")
   print()



"""**A list containing the least important attributes to be dropped**"""

Final_Attributes_To_drop = ['defending_sliding_tackle', 'mentality_composure', 'club_position', 'skill_ball_control', 'mentality_penalties', 'movement_agility', 'lcb', 'defending_standing_tackle', 'pace', 'skill_dribbling', 'attacking_finishing', 'attacking_heading_accuracy', 'defending_marking_awareness', 'mentality_vision', 'power_long_shots', 'movement_sprint_speed', 'mentality_aggression', 'mentality_interceptions', 'power_jumping', 'attacking_short_passing', 'attacking_volleys', 'movement_acceleration', 'power_strength', 'player_positions', 'power_shot_power', 'skill_curve', 'skill_fk_accuracy', 'movement_balance', 'weight_kg', 'skill_long_passing', 'work_rate', 'skill_moves', 'rcb', 'cb', 'rwb', 'rdm', 'cdm', 'rm', 'rb', 'st', 'rcm', 'cm', 'ram', 'cam', 'rf', 'cf', 'rs', 'rw','ls', 'lw', 'lf', 'lam', 'lm', 'lcm', 'lwb', 'ldm', 'lb', 'gk']

"""**Dropping least important attributes to form Input_training(X)**"""

Input_Training = Input_Training.drop(Final_Attributes_To_drop, axis = 1)

Input_Training

"""**Spliting data into Input_testing(X) and Output_testing(Y) for model testing**"""

Input_Testing = Filtered_Testing_Data.drop('overall', axis = 1)
Output_Testing = pd.DataFrame(Filtered_Testing_Data['overall'], columns = ['overall'])

"""**Dropping least important attributes to form Input_testing(X)**"""

Input_Testing = Input_Testing.drop(Final_Attributes_To_drop, axis = 1)

Input_Testing



"""# **Model One**

**Importing relevant libraries for model training**
"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

"""**Creating the LinearRegression model to be trained**"""

Linear_Regressor_Model = LinearRegression()

"""**Fitting the linear regression model with training data**"""

Linear_Regressor_Model.fit(Input_Training, Output_Training)

"""**Predicting overall rating using testing data**"""

Linear_Regressor_Model_Prediction = Linear_Regressor_Model.predict(Input_Testing)

Linear_Regressor_Model_Prediction

"""**Checking the mean_absolute_error of the linear regression model**"""

mean_absolute_error(Linear_Regressor_Model_Prediction, Output_Testing)



"""# **Model Two**

**Importing DecisionTreeRegressor**
"""

from sklearn.tree import DecisionTreeRegressor



"""**Creating the DecisionTreeRegressor model to be trained**"""

Tree_Regressor_Model = DecisionTreeRegressor()

"""**Fitting the DecisionTreeRegressor model with training data**"""

Tree_Regressor_Model.fit(Input_Training, Output_Training)

"""**Predicting overall rating using testing data**"""

Tree_Regressor_Model_Prediction = Tree_Regressor_Model.predict(Input_Testing)

Tree_Regressor_Model_Prediction

"""**Checking the mean_absolute_error of the DecisionTreeRegressor model**"""

mean_absolute_error(Tree_Regressor_Model_Prediction, Output_Testing)





"""**Saving Tree_Regressor_Model using Pickle**"""

import pickle
pickle.dump(Tree_Regressor_Model, open("Random_model.sav", 'wb'))

"""# **Model Three**

***Importing RandomForestRegressor***
"""

from sklearn.ensemble import RandomForestRegressor

"""**Creating the RandomForestRegressor model to be trained**"""

Random_Forest_Regressor_Model = RandomForestRegressor(n_estimators = 500, max_depth = 15,criterion = 'absolute_error', random_state = 0, min_samples_split = 2, min_samples_leaf = 1, max_features = 'auto', bootstrap = True)

"""**Fitting the RandomForestRegressor model with training data**"""

Random_Forest_Regressor_Model.fit(Input_Training, Output_Training)

"""**Predicting overall rating using testing data**"""

Random_Forest_Regressor_Prediction = Random_Forest_Regressor_Model.predict(Input_Testing)

Random_Forest_Regressor_Prediction

"""**Checking the mean_absolute_error of the RandomForestRegressor model**"""

mean_absolute_error(Random_Forest_Regressor_Prediction, Output_Testing)



"""**Saving Random_Forest_Regressor_model using Pickle**"""

import pickle
pickle.dump(Random_Forest_Regressor_Model, open("Random_Forest_Regressor_model.sav", 'wb'))





"""# **Model Four**

**Importanting VotingRegressor, SVR, KNeighborsRegressor, DecisionTreeRegressor for ensemble model**
"""

from sklearn.ensemble import VotingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

"""Creating the SVR, KNeighborsRegressor, and DecisionTreeRegressor  models to be trained"""

decision_tree = DecisionTreeRegressor(random_state=42, criterion='absolute_error')
knn = KNeighborsRegressor(n_neighbors=8)
svm = SVR(C = 1.0, epsilon=0.2)



"""**Creating the VotingRegressor model to be trained**"""

voting_regressor = VotingRegressor(estimators=[('decision_tree', decision_tree), ('knn', knn), ('svm', svm)])

"""**Fitting the ensemble model with training data**"""

for model in (decision_tree, knn, svm, voting_regressor):
  model.fit(Input_Training, Output_Training)
  Ensemble_Model_Prediction = model.predict(Input_Testing)
  print(model.__class__.__name__,mean_absolute_error(Ensemble_Model_Prediction, Output_Testing))

"""**Checking the mean_absolute_error of the ensemble model**"""

mean_absolute_error(Ensemble_Model_Prediction, Output_Testing)

"""# **Model Five(Model chosen to be deployed based on the mean absolute error).**

**Importanting an ensemble RandomForestRegressor**
"""

from sklearn.ensemble import RandomForestRegressor

"""**Creating the RandomForestRegressor model to be trained**"""

Random_Forest_Regressor_Model = RandomForestRegressor(n_estimators = 500, max_depth = 15, criterion = 'absolute_error')

"""Fitting the ensemble RandomForestRegressor model with training data"""

Random_Forest_Regressor_Model.fit(Input_Training, Output_Training)

"""**Predicting overall rating using testing data**"""

Random_Forest_Model_Prediction = Random_Forest_Regressor_Model.predict(Input_Testing)

"""**Checking the mean_absolute_error of the ensemble RandomForestRegressor model**"""

mean_absolute_error(Random_Forest_Model_Prediction, Output_Testing)

""" **Calculating the confidence score of the RandomForestRegressor model**"""

from sklearn.metrics import r2_score
r2 = r2_score(Output_Testing, Random_Forest_Model_Prediction)
r2

"""**Saving the ensemble RandomForestRegressor model using Pickle**"""

import pickle
pickle.dump(Random_Forest_Regressor_Model, open("Random_Forest_model.sav", 'wb'))

