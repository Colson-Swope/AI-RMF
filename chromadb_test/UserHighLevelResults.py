# replace with dynamic file path when GUI is done 

def get_user_high_level_results(target_system_name_input):

    input_data = target_system_name_input

    # creates a dynamic file path according to the associated machine name 
    path_start = "./machine_transfer/"
    dynamic_name = input_data
    path_end = "/patch_report_ai.txt"
    full_path = path_start + dynamic_name + path_end

    with open(full_path) as file: 
        content = file.read()
        user_high_level_results = content

    return user_high_level_results
