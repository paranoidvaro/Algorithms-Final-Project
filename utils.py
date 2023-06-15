from . import project

caching_dict, utils_threshold = {}, 0

def update_function(array : list) -> set:
    temporary_set = set()
    set_comprehension = {temporary_set.update(project.correlations[stock]) for stock in array}
    
    return temporary_set

