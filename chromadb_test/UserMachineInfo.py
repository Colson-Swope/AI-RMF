with open("./machine_transfer/RMF-Client01/debian_sys_config.txt") as file:
    content = file.read()

user_machine_data = content

def get_user_machine_info():
    return user_machine_data
