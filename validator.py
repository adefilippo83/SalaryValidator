import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
import os
import argparse
import json
import datetime

class DataValidator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.report = {}
    

    def load_data(self):
        self.df = pd.read_csv(self.filepath)

    def validate_columns(self):
        self.report["missing_values"] = self.df.isna().sum().to_dict()
        #print(self.df.head())
        #print(self.df.isna().sum())

        missing = self.df.isna().sum()
        missing = missing[missing > 0]
        self.report["missing_values"] = {k: int(v) for k, v in missing.to_dict().items()}
    
    def duplicates_rows(self):
    
        self.report["duplicates_rows"] = int(self.df.duplicated().sum())

    def save_report(self, filepath):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
        filename = f"report_{timestamp}.json"
        full_path = os.path.join(filepath,filename)

        with open(full_path, 'w') as f:
            json.dump(self.report, f, indent = 4)
        print(f"Report saved as {filename}")

    
    def run(self, report_path = None):

        self.load_data()
        self.validate_columns()
        self.duplicates_rows()
        
        if report_path is not None:
            self.save_report(report_path)

        return self.report

class DataVisualizer:
    def __init__(self, df, columns_to_plot = None):
        self.df = df
        self.columns_to_plot = columns_to_plot or df.columns.tolist()
    
    def plot_missing_heatmap(self):
        #fetch missing values
        missing_matrix = self.df.isna()

        plt.figure(figsize=(10, 6))
        sns.heatmap(missing_matrix, cbar=False, cmap="viridis")
        plt.title("Missing Values Heatmap")
        plt.show()
    
    def plot_distribution(self, column):
        
        if column not in self.df.columns:
            print(f"This column does not exist")
            return
        
        #exclude missing values
        data = self.df[column].dropna() 

        plt.figure(figsize=(8, 5))
        sns.histplot(data, kde=True, bins=20)
        plt.title(f"Distribution of {column}")
        plt.show()
    
    def plot_correlation_matrix(self):
        #select columns
        numeric_df = self.df[self.columns_to_plot]

        #calculate correlation
        corr = numeric_df.corr()

        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Matrix")
        plt.show()
    
    def plot_categorical_distribution(self,column):
        if column not in self.df.columns:
            print(f"This column does not exist")
            return
        
        #exclude missing values
        data = self.df[column].dropna()

        #calculate each category
        counts = data.value_counts()

        plt.figure(figsize=(8, 5))
        sns.barplot(x=counts.index, y=counts.values)
        plt.title(f"Categorical Distribution of {column}")
        plt.xticks(rotation=45)
        plt.show()


if __name__ == "__main__":
    #create parser
    parser = argparse.ArgumentParser(description="DataValidator: validate CSV datasets.")

    parser.add_argument(
        "--file",
        "-f",
        required = True,
        help = "Path to the CSV file you want to validate."
    )

    parser.add_argument("--report", "-r", default=".", help="Folder path to save the report.")

    parser.add_argument(
        "--num_columns",
        help = "Comma-separated list of numerical columns to plot"
    )

    parser.add_argument(
        "--cat_columns",
        help= "Comma-separated list of categorical columns to plot"
    )


    args = parser.parse_args()

    validator = DataValidator(args.file)

    report = validator.run(args.report)

    num_columns = args.num_columns.split(",") if args.num_columns else []
    cat_columns = args.cat_columns.split(",") if args.cat_columns else []

    visualizer = DataVisualizer(validator.df)
    visualizer.plot_missing_heatmap()
    visualizer.plot_distribution()
    visualizer.plot_correlation_matrix()

    for col in num_columns:
        visualizer.plot_distribution(col)


    print(report)







        
        
        




        

