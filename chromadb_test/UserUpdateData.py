with open("./machine_transfer/RMF-Client01/debian_patch_report.txt") as file: 
    content = file.read()

user_update_data = content

def get_user_update_data():
    return user_update_data
