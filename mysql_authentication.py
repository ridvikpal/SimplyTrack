import yaml

# function to write yaml file
def write_yaml_to_file(data,filename) -> None:
    with open(f'{filename}.yaml', 'w',) as f :
        yaml.dump(data,f,sort_keys=False)
    # print('Written to file successfully')

# function to read one block of a yaml file and returns it as a dictionary
def read_one_block_of_yaml_data(filename) -> dict:
    with open(f'{filename}.yaml','r') as f:
        output = yaml.safe_load(f)
    return output

# # create a data dictionary
# data = {
#     'Username':'username',
#     'Password':'passwd',
#     'Host':'hostname',
#     'Database':'db_name',
#     'Table':'table_name'
# }

# # dump the dictionary to yaml format and store it in a file
# write_yaml_to_file(data, 'server_configuration')

result = read_one_block_of_yaml_data('server_configuration')
