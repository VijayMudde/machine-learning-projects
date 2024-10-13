#!/usr/bin/env python
# coding: utf-8

# In[5]:


# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib


# In[6]:


print(pd.__version__)
print(np.__version__)
print(sns.__version__)
print(sklearn.__version__)


# In[8]:


# Load the dataset
df = pd.read_csv('C:/Users/vijay/OneDrive/Desktop/AI-ML-DS/ML model/DiabPredict/DiabetesModel/diabetes.csv')


# In[9]:


# Display the first few rows of the dataset
print(df.head())


# In[10]:


# Check for missing values
print(df.isnull().sum())


# In[11]:


# Visualizing the distribution of the 'Outcome' variable
sns.countplot(df['Outcome'])
plt.title('Distribution of Outcome')
plt.show()


# In[12]:


# Correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()


# In[13]:


# Data preprocessing
sc = StandardScaler()


# In[14]:


# Separating features and target variable
X = df.drop(columns='Outcome')
y = df['Outcome']


# In[15]:


# Scaling the features
X = sc.fit_transform(X)


# In[16]:


# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


# In[17]:


# Training the K-Nearest Neighbors (KNN) classifier
knn = KNeighborsClassifier(n_neighbors=11, p=3, metric='minkowski')
knn.fit(X_train, y_train)


# In[18]:


# Making predictions on the test set
y_pred = knn.predict(X_test)


# In[19]:


# Evaluating the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')


# In[20]:


# Saving the classifier model and the scaler using joblib
joblib.dump(knn, 'final_knn_model.joblib')
joblib.dump(sc, 'final_knn_scaler.joblib')


# In[ ]:




