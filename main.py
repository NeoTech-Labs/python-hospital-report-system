
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=NEO-LAPTOP\\SQLEXPRESS;'
    'DATABASE=HospitalDB;'
    'Trusted_Connection=yes;'
)

# Patient Spending Report
patient_query = """
SELECT p.patient_name,
       p.province,
       SUM(t.total_cost) AS total_spent
FROM Patients p
JOIN Treatments t
ON p.patient_id = t.patient_id
GROUP BY p.patient_name, p.province
ORDER BY total_spent DESC
"""

# Revenue by Category
category_query = """
SELECT category,
       SUM(total_cost) AS revenue
FROM Treatments
GROUP BY category
"""

# Monthly Revenue
monthly_query = """
SELECT MONTH(treatment_date) AS month,
       SUM(total_cost) AS revenue
FROM Treatments
GROUP BY MONTH(treatment_date)
"""


try:

    while True:

        print("\n====== HOSPITAL REPORT SYSTEM ======")
        print("1. Patient Spending Report")
        print("2. Revenue by Category")
        print("3. Monthly Revenue")
        print("4. Search Patient")
        print("5. Filter Treatments by Date")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            patient_df = pd.read_sql(patient_query, conn)

            print(patient_df)

            print("Patient report generated!")

            plt.bar(patient_df['patient_name'], patient_df['total_spent'])

            plt.xlabel("Patients")
            plt.ylabel("Amount Spent")
            plt.title("Patient Spending Report")

            plt.savefig("charts/patient_spending_chart.png")

            plt.show(block=False)
            plt.pause(5)
            plt.close()

            patient_df.to_excel(
                "reports/patient_report.xlsx",
                index=False
            )

        elif choice == "2":

            category_df = pd.read_sql(category_query, conn)

            print(category_df)

            category_df.to_excel(
                "reports/category_report.xlsx",
                index=False
            )

            print("Category report generated!")

        elif choice == "3":

            monthly_df = pd.read_sql(monthly_query, conn)

            print(monthly_df)

            monthly_df.to_excel(
                "reports/monthly_report.xlsx",
                index=False
            )

            print("Monthly report generated!")

        elif choice == "4":

            patient_name = input("Enter patient name: ")

            search_query = """
                SELECT p.patient_name,
                       t.treatment_name,
                       t.category,
                       t.total_cost,
                       t.treatment_date
                FROM Patients p
                JOIN Treatments t
                ON p.patient_id = t.patient_id
                WHERE p.patient_name LIKE ?
                """

            search_df = pd.read_sql(
                search_query,
                conn,
                params=(f"%{patient_name}%",)
            )

            if search_df.empty:
                print("Patient not in data")
            else:
                print(search_df)

        elif choice == "5":

            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")

            date_query = """
                SELECT *
                FROM Treatments
                WHERE treatment_date BETWEEN ? AND ?
                """

            date_df = pd.read_sql(
                date_query,
                conn,
                params=(start_date, end_date)
            )

            if date_df.empty:
                print("Dates for treatments not found")
            else:
                print(date_df)
        elif choice == "6":

            print("Exiting system...")
            break

        else:

            print("Invalid choice!")

except Exception as e:

    print("An error occurred:")
    print(e)

conn.close()
