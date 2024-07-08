import datetime
import os


def generate_unique_data():
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the current date and time to ensure uniqueness
    date_time_str = now.strftime("%Y%m%d_%H%M%S")

    csv_file_path = os.path.abspath(
        os.path.join("C:\\PycharmProjects\\Portal_Automation\\Portal_Automation\\Bulk_import_file\\bulk_user_add_Files.csv"))

    # Define the base JSON structure with unique values
    data = {
        "username": "sneha@sanas.ai",
        "password": "Snehasahu@123",
        "invalid_username": f"userid_{date_time_str}",
        "invalid_password": "invalid@password",
        "Uat_Portal": "https://portal-staging.sanas.ai/",
        "Enterprise": f"ent_{date_time_str}",
        "BPO": f"bpo_{date_time_str}",
        "location": f"loc_{date_time_str}",
        "seats": "1000",
        "Enterprise_exists": "neha",
        "BPO_exists": "sun",
        "location_exists": "do",
        "seats_exists": "1000",
        "invalid_Email": f"test_{date_time_str}@sanas",
        "Email": f"test_{date_time_str}@sanas.ai",
        "TeamName": f"team_{date_time_str}",
        "NewUser": f"user_{date_time_str}",
        "invalid_UserId": f"user_id_{date_time_str}",
        "invalid_TeamName": f"team_{date_time_str}",
        "invalid_NewUser": f"user_{date_time_str}",
        "UserId": f"user_id_{date_time_str}",
        "Invalid_UserName": "Invalid",
        "Invalid_UserId": "1",
        "CSV": "C:\\Users\\Sneha\\PycharmProjects\\Portal_Automation\\pythonProject\\CSV\\bulkuseraddFiles.csv",
        "invalid_CSV": "C:\\Users\\Sneha\\PycharmProjects\\Portal_Automation\\pythonProject\\CSV\\invalidbulkuseraddFiles.csv"

    }

    return data


# Example usage
unique_data = generate_unique_data()
print(unique_data)

