import os
import pandas as pd 
import numpy as np 
import csv 


class Dataset_Process(object):
    def __init__(self, filename, discrete_features, continuos_features):
        self.raw = pd.read_csv(filename, dtype=str)
        # self.category_feature('prd_brnd_cd')
        ## 002081000008 -> 2081000008 로 읽네... prd_cd , dtype=str
        

    def get_column_data(self, feature_name):
        return self.raw[feature_name]

    def category_feature(self, feature_name):
        """
        카테고리 Feature가 들어오면 Unique한 Dict를 빼내고 인코딩을 한다. 
        """
        feature_values = self.raw[feature_name]
        unique_vals = feature_values.unique()
        
        id_to_val = {index:value for index,value in enumerate(unique_vals)}
        
        return id_to_val
    
    def continuous_feature(self, feature_name):
        """
        범위 데이터가 들어오면 Normalize한 결과가 나오도록 만든다.
        return tuple(min, max) , normalized values
        """
        pass

    def zip_column_dict(self, first, second):
        raw = self.raw
        res_dict = {index:value for index,value in zip(raw[first], raw[second])}
        return res_dict, len(res_dict)



class skip_gram_sampling(object):
    def __init__(self, dataset, window_size):
        self.raw_dataset = dataset
        self.window_size = window_size

        # 윈도우 사이즈 보다 작은 데이터 시퀀스는 자른다
        self.raw_dataset = [data for data in self.raw_dataset if len(data) >= self.window_size]
        self.occurence_table = self.create_occurence_table()

        #print( self.occurence_table )
        self.pos_pairs = self.pos_sample()


    def pos_sample(self):
        window = self.window_size / 2
        pos_pairs = []
        
        for item_seq in self.raw_dataset:
            for idx, target_item in enumerate(item_seq):
                l_limit = int( max(0, idx-window+1) )
                r_limit = int( min(len(item_seq), idx+window+1) )
                left_items = item_seq[ l_limit:idx ]
                right_items = item_seq[ idx+1:r_limit ]
                context_items = left_items + right_items
                #print(context_items)
                # print(f"left : {left_items},\tmid : {target_item},\tright : {right_items}\n")
                tmp = [(target_item, context_item) for context_item in context_items]
                pos_pairs += tmp
        
        #print(pos_pairs)
        pos_pair_dict = dict()

        for index, pos_pair in enumerate(pos_pairs):
            try:
                pos_pair_dict[pos_pair] += 1
            except:
                pos_pair_dict[pos_pair] = 1

        with open('pos_pair_dict.csv', 'w') as f:
            for key, val in pos_pair_dict.items():
                line = str(key) + '\t' + str(val) + '\n'
                f.write(line)
        
        #print(pos_pair_dict)
        return pos_pair_dict

    def create_pair_occurence_table(self, item_to_id):
        total_items = np.max( [ int(val) for val in item_to_id.values() ] )
        id_to_item = {val:key for key,val in item_to_id.items()}
        #print(id_to_item)

        #print(f"KKK Total Items : {total_items}") # 전체 아이템 수
        
        pair_occurence_table = np.zeros(shape=(total_items+1, total_items+1), dtype='int32')
        #print(pair_occurence_table.shape)            


        for pos_pair in self.pos_pairs:
            target = int( item_to_id[ pos_pair[0] ] )
            context = int( item_to_id[ pos_pair[1] ] )
            pair_occurence_table[target][context] += 1
            
        #print( pair_occurence_table ) 

        not_paired_items = []

        for target_item_index, occur_hist in enumerate(pair_occurence_table):
            for context_item_index, context_item in enumerate(occur_hist):
                target_item_index = str(target_item_index)
                context_item_index = str(context_item_index)
                if(context_item == 0):
                    try:
                        not_paired_items += [(id_to_item[target_item_index], id_to_item[context_item_index])]
                    except:
                        print("id_to_item :", target_item_index, context_item_index)
        print(len( not_paired_items))
        with open('not_paired_items.csv', 'w') as f:
            for key in not_paired_items:
                line = str(key) + '\n'
                f.write(line)





    def create_occurence_table(self): 
        o_table = dict()
        # 데이터셋을 이중 포문으로 읽으면서 아이템의 등장 횟수를 센다.
        for item_seq in self.raw_dataset:
            for item in item_seq:
                try:
                    o_table[item] += 1
                except:
                    o_table[item] = 1
        
        with open('occurence_dict.csv', 'w') as f:
            for key, val in o_table.items():
                line = str(key) + '\t' + str(val) + '\n'
                f.write(line)
        
        return o_table

    def neg_sampling_table(self):
        pass
        # negative sampling 




if __name__ == "__main__":
    cur_path = os.getcwd()
    items_path = os.path.join(cur_path, 'dataset/apmall/items.csv')
    items_dataset, total_items = Dataset_Process(items_path, 
                                    None, 
                                    None).zip_column_dict('prd_cd' ,'item_index')
    print("Total_Items : ", total_items)
    
    users_path = os.path.join(cur_path, 'dataset/apmall/users.csv')
    users_dataset = Dataset_Process(users_path,
                                    None,
                                    None)
    user_click_prds = users_dataset.get_column_data('prdcd_seq')
    user_click_prds = [user_click_prd.split(',') for user_click_prd in user_click_prds]

    skip_gram_sampling(user_click_prds, 5).create_pair_occurence_table(items_dataset)
