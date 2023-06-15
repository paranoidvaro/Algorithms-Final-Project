from . import utils



# Global data to store information

stocks_prices = {}



def prepare(filename : str, threshold : float):
    
    utils.utils_threshold = threshold

    # reading the text file:
    with open('C:/Users/Valerio Cadura/OneDrive - LUISS Libera Università Internazionale degli Studi Sociali Guido Carli/Uni/Programmi Luiss/Algorithms/project_skeleton_final/{}'.format(filename)) as data:
        global correlations, connected_components, stock_prices
        correlations, connected_components, stocks_prices = {}, [], {}

        # reading and splitting the text file using a generator comprehension:
        read_data = (line.split(',') for line in data.read().split('\n') if line != '')
        
        # getting the first and last days prices and computing the returns:
        for stock in read_data:
            if int(stock[1]) % 365 == 0 or int(stock[1]) == 1:
                try:
                    
                    if int(stock[1]) == 365:
                        stocks_prices[stock[0]][0] = int(stock[2])
                    else:
                        stocks_prices[stock[0]][1] = int(stock[2])

                    try:
                        stocks_prices[stock[0]][2] = round((stocks_prices[stock[0]][1] - stocks_prices[stock[0]][0]) / stocks_prices[stock[0]][0], 5)
                    except ZeroDivisionError:
                        stocks_prices[stock[0]][2] = 1
                except KeyError:
                    if int(stock[1]) == 365:
                        stocks_prices[stock[0]] = [int(stock[2]), 0, 0]
                    else:
                        stocks_prices[stock[0]] = [0, int(stock[2]), 0]
        
        # initializing the graph data structure from utils to start constructing:
        stocks_list = list(stocks_prices.keys())
        while stocks_list:
            temp_index, connected = None, False
            
            correlations[stocks_list[0]] = correlations.get(stocks_list[0], set())
        
            for index in range(1, len(stocks_list)):
                temp_index_2 = None
                
                if abs(stocks_prices[stocks_list[0]][2] - stocks_prices[stocks_list[index]][2]) < threshold:
                    connected = True
                    correlations[stocks_list[0]].add(stocks_list[index])
                    
                    try:
                        correlations[stocks_list[index]].add(stocks_list[0])
                    except KeyError:
                        correlations[stocks_list[index]] = {stocks_list[0]}
                    
                    
                    for second_index in range(len(connected_components)):
                        
                        if stocks_list[0] in connected_components[second_index]:
                            temp_index = second_index
                        if stocks_list[index] in connected_components[second_index]:
                            temp_index_2 = second_index
                        
                    if temp_index != None and temp_index_2 != None:
                        if temp_index != temp_index_2:
                            connected_components[temp_index].update(connected_components.pop(temp_index_2))
                    
                    elif temp_index != None and temp_index_2 == None:
                        connected_components[temp_index].add(stocks_list[index])
                    
                    elif temp_index == None and temp_index_2 != None:
                        connected_components[temp_index_2].add(stocks_list[0])
                    
                    
                    else:
                        connected_components.append({stocks_list[0], stocks_list[index]})
                        
            if not connected:
                for stock_connected_nodes in connected_components: 
                    if stocks_list[0] in stock_connected_nodes:
                        connected = True
                        break
                
                if not connected:
                    connected_components.append({stocks_list[0]})
            stocks_list.pop(0)






def query(stock : str, corr_level : int) -> list:

    if corr_level == 1:
        return sorted(correlations[stock])
    
    pre_set, final_set = set(), correlations[stock]
    
    if (stock, corr_level, utils.utils_threshold) in utils.caching_dict:
        return utils.caching_dict[(stock, corr_level, utils.utils_threshold)]
    
    for count in range(1, corr_level):
        pre_set.update(final_set)
        final_set = utils.update_function(final_set).difference(pre_set)
        
        if tuple(final_set) not in utils.caching_dict:
            try:
                final_set.remove(stock)
            
            except KeyError:
                pass
            utils.caching_dict[(stock, corr_level, utils.utils_threshold)] = sorted(final_set)
            
    return sorted(final_set)


def num_connected_components() -> int:
    return len(connected_components)

# to speed up the code, we could trying moving the query part to prepare, then calculate the correlation levels up to
# the highest correlation level he asked for in the main.py.
# or we could try to do it the same way, but like this:
# we do it for the first level for each stock, then we check,
# if there are correlated stocks in the next level, we compute it, otherwise, we move on to the next one.