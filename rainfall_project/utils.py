import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("rainfall.csv")
df['rainfall'] = df['rainfall'].map({'yes':1,'no':0})

def show_pie():
    counts = df['rainfall'].value_counts()
    plt.pie(counts, labels=["No","Yes"], autopct='%1.1f%%')
    plt.title("Rainfall Distribution")
    plt.show()

def show_box():
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df)
    plt.show()

def show_heatmap():
    sns.heatmap(df.corr(), annot=True)
    plt.show()