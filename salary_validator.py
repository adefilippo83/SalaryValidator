import pandas as pd
import json
import os
import matplotlib.pyplot as plt

class SalaryDataValidator:
    def __init__(self,filepath):
        self.filepath = filepath
        self.df = None
        self.report = {}
    
    def load_data(self):
        """Load CSV into DataFrame."""
        try:
            self.df = pd.read_csv(self.filepath)
            self.report["total_rows"] = len(self.df)
            self.report["columns"] = list(self.df.columns)
            print("Data loaded successfully.")
        except Exception as e:
            print("Failed to load file:", e)
            raise e
    
    def check_missing(self):
        missing_counts = self.df.isna().sum()
        duplicate_count = self.df.duplicated().sum()

        self.report["missing_values"] = missing_counts.to_dict()
        self.report["duplicate_count"] = int(duplicate_count)
    
    def select_columns(self):
        """Keep only necessary columns."""
        columns_to_keep = [
            "work_year",
            "experience_level",
            "employment_type",
            "job_title",
            "salary_in_usd"
        ]
        self.df = self.df[columns_to_keep]
        self.report["columns"]=list(columns_to_keep)
    
    def validate_experience_level(self):
        """Check valid experience level input"""
        allowed = ["EN", "MI", "SE", "EX"]
        invalid_rows = self.df[~self.df["experience_level"].isin(allowed)]
        self.report["invalid_experience_level_count"] = len(invalid_rows)

        if len(invalid_rows)>0:
            print("Found invalid experience_level values:")
            print(invalid_rows.head())
        else:
            print("All experience_level values are valid.")

        counts = self.df["experience_level"].value_counts()
        total = counts.sum()

        plt.figure(figsize=(6,4))
        bars = plt.bar(counts.index, counts.values, color='skyblue')

       
        for bar, (level, count) in zip(bars, counts.items()):
            height = bar.get_height()
            pct = count / total * 100
            plt.text(
                bar.get_x() + bar.get_width()/2,
                height + total*0.01,
                f"{count} ({pct:.1f}%)",
                ha='center',
                va='bottom',
                fontsize=10
        )

        plt.title("Experience Level Distribution")
        plt.ylabel("Number of Employees")
        plt.xlabel("Experience Level")
        plt.ylim(0, max(counts.values)*1.15)

        plt.show()

        return invalid_rows
    
    def top_job_by_salary(self, top_n=5):
        """Check the job titles with the highest top 5 average salary"""
        df = self.df[["job_title", "salary_in_usd"]]#two colums needed
        total_job_roles = df["job_title"].nunique()
        self.report["total_job_roles"] = int(total_job_roles)

        avg_salary = df.groupby("job_title")["salary_in_usd"].mean()
        avg_salary = avg_salary.round(0)
        top5 = avg_salary.sort_values(ascending=False).head(5)
        self.report["top5_jobs_by_avg_salary"] = top5.to_dict()


        #plt.figure(figsize=(10,6))
        #top5.plot(kind='bar', color='skyblue')
        #plt.title("Top 5 Job Titles by Average Salary")
        #plt.ylabel("Average Salary (USD)")
        #plt.xticks(rotation=45, ha="right")  
        #plt.tight_layout()
        #plt.show()
        return top5


    
    def detect_salary_outliers(self):
        """IQR method."""
        Q1 = self.df['salary_in_usd'].quantile(0.25)
        Q3 = self.df['salary_in_usd'].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = max(0, Q1 - 1.5 * IQR)
        upper_bound = Q3 + 1.5 * IQR

        outliers = self.df[(self.df['salary_in_usd'] < lower_bound) |
                           (self.df['salary_in_usd'] > upper_bound)]
        self.report["salary_range"] = {
            #"Q1": float(Q1),
            #"Q3": float(Q3),
            #"IQR": float(IQR),
            "lower_bound": float(lower_bound),
            "upper_bound":float(upper_bound)
        }

        self.report["salary_outliers_count"] = len(outliers)
        print("Outlier detection complete.")


        #draw image
        lower = self.df['salary_in_usd'].quantile(0.01)
        upper = self.df['salary_in_usd'].quantile(0.99)

        filtered = self.df[(self.df['salary_in_usd'] >= lower) & (self.df['salary_in_usd'] <= upper)]

        plt.figure(figsize=(8,5))
        plt.hist(filtered['salary_in_usd'], bins=50, color='skyblue')
        plt.title("Salary Distribution Histogram (Filtered 1%-99%)")
        plt.xlabel("Salary (USD)")
        plt.ylabel("Number of Employees")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()


        return outliers
    
    def clean_data(self):
        """Clean the dataset"""

        initial_rows = len(self.df)
        self.df = self.df[self.df['salary_in_usd']> 0]
        print(f"Dropped {initial_rows - len(self.df)} rows with invalid salary <=0")

        self.df['experinence_level'] = self.df ['experience_level'].str.upper().str.strip()
        self.df['employment_type'] = self.df['employment_type'].str.upper().str.strip()


        #clean duplicates
        total_rows = len(self.df)
        self.report["total_rows"]

        duplicate_mask = self.df.duplicated()#true or false
        duplicate_count = duplicate_mask.sum()
        self.report["duplicate_count"] = int(duplicate_count)
        self.df= self.df.drop_duplicates()

        duplicates_removed = duplicate_count
        self.report["duplicates_removed"] = int(duplicates_removed)





    

    def save_report(self, output = "validation_report.json"):
        """Save validation report into JSON"""
        with open(output, "w") as f:
            json.dump(self.report, f, indent = 4)
        print(f"Rrport saved to {output}")
    
    def run(self):
        """
        Main validation pipeline.
       1. Load CSV
       2. Select relevant columns
       3. Detect salary outliers
       4. Save JSON report
       """
        self.load_data()
        self.select_columns()
        self.top_job_by_salary()
        self.check_missing()
        self.clean_data()


        outliers = self.detect_salary_outliers()
        invalid_experience_input = self.validate_experience_level()
        self.save_report()
        plt.savefig("salary_boxplot.png")
        plt.savefig("salary_histogram.png")


        return outliers, invalid_experience_input


    
if __name__ == "__main__":
    validator = SalaryDataValidator("data_salary.csv")
    validator.run()


