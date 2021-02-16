#!/usr/bin/env python
# coding: utf-8

# # 파이토치 학습 데이터 생성기
# 원하는 batch_size 만큼의 positive_pair와 negative_pair 가 나오길 원함

# In[79]:


import os
import pandas as pd
import numpy as np
import sys

# In[80]:


class Dataset_Process(object):
    def __init__(self, filename, discrete_features, continuos_features):
        self.raw = pd.read_csv(filename, dtype=str)
        # self.category_feature('prd_brnd_cd')
        ## 002081000008 -> 2081000008 로 읽네... prd_cd , dtype=str
        # print(self.raw.head())

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
        
        res_dict = {}
        
        for index, value in zip(raw[first], raw[second]):
            try:
                res_dict[index].append(value)
            except:
                res_dict[index] = [value]
        return res_dict


# In[81]:


import random 

class skip_gram_sampling(object):
    def __init__(self, dataset, window_size):
        self.raw_dataset = dataset
        self.window_size = window_size

        # 윈도우 사이즈 보다 작은 데이터 시퀀스는 자른다
        self.raw_dataset = [data for data in self.raw_dataset if len(data) >= self.window_size]
        self.occurence_table = self.create_occurence_table()
        self.neg_sample_table = self.neg_sampling_table()

        self.pos_pairs_count, self.pos_pairs_set = self.pos_sample()

    def get_pos_pairs(self):
        return list(self.pos_pairs_count.keys())
    def get_pos_context_set(self):
        return self.pos_pairs_set
    
    
    def get_occurence_table(self):
        return self.occurence_table

    def get_neg_sampling_table(self):
        return self.neg_sample_table
    
    
    def pos_sample(self):
        window = self.window_size / 2
        pos_pairs = []
        pos_pair_set = dict()
        
        for item_seq in self.raw_dataset:
            for idx, target_item in enumerate(item_seq):
                l_limit = int( max(0, idx-window+1) )
                r_limit = int( min(len(item_seq), idx+window+1) )
                left_items = item_seq[ l_limit:idx ]
                right_items = item_seq[ idx+1:r_limit ]
                context_items = left_items + right_items
                #print(context_items)
                #print(f"left : {left_items},\tmid : {target_item},\tright : {right_items}\n")
                tmp = [(target_item, context_item) for context_item in context_items]
                
                if target_item in pos_pair_set:
                    pos_pair_set[str(target_item)].update(context_items)
                else:
                    pos_pair_set[str(target_item)] = set(context_items)                    
                pos_pairs += tmp
        
        #print(pos_pair_set)
        #print(pos_pairs)
        pos_pair_count = dict()

        
        
        
        for index, pos_pair in enumerate(pos_pairs):
            
            try:
                pos_pair_count[pos_pair] += 1
            except:
                pos_pair_count[pos_pair] = 1
                
                
                

        with open('pos_pair_count.csv', 'w') as f:
            for key, val in pos_pair_count.items():
                line = str(key) + '\t' + str(val) + '\n'
                f.write(line)
        
        # print(pos_pair_count)
        return pos_pair_count, pos_pair_set 

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
                        pass
        # print(len( not_paired_items))
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
        # 기준이 되는 table은 
        #                           해당 단어의 등장 빈도수 ^ 0.75 
        # Negative Sampling 기준 = -------------------------
        #                               전체 단어 수 ^ 0.75
        occurence_table = self.occurence_table
        neg_sampling_table = dict()
        
        
        total_occur_items = len(occurence_table.keys())
        
        for key in occurence_table.keys():
            neg_sampling_table[key] = (occurence_table[key]/total_occur_items) ** 0.75 
        
        # negative sampling 
        item_population = list(neg_sampling_table.keys())
        item_weights = list(neg_sampling_table.values())
        
        # Test
        """
        neg_context = random.choices(population = item_population,
                                     weights = item_weights,
                                     k = 10)
        """
        return neg_sampling_table


# In[84]:


import torch
from torch.utils.data import Dataset, DataLoader
# 커스텀 데이터셋 torch.utils.data.Dataset을 상속 받아
class item2vec_dataset(Dataset):
    def __init__(self, item_data_path='dataset/apmall/users.csv', user_data_path='dataset/apmall/items.csv', neg_cnt=5):
        self.negative_context_count = neg_cnt
        self.item_data_path = item_data_path
        self.user_data_path = user_data_path
        cur_path = os.getcwd()
        # 데이터셋의 전처리를 해주는 부분
        users_path = os.path.join(cur_path, self.user_data_path)
        users_dataset = Dataset_Process(users_path, None, None)
        
        items_path = os.path.join(cur_path, self.item_data_path)
        self.items = Dataset_Process(items_path, None, None)
        self.prdcd_to_itemindex = self.items.zip_column_dict('prd_cd', 'item_index')
        self.itemindex_to_prdcd = self.items.zip_column_dict('item_index', 'prd_cd')
        self.prdcd_to_prdnm = self.items.zip_column_dict('prd_cd', 'prd_nm')
        self.prdnm_to_prdcd = self.items.zip_column_dict('prd_nm', 'prd_cd')

        user_click_prds = users_dataset.get_column_data('prdcd_seq')
        # print(user_click_prds)
        user_click_prds = [user_click_prd.split(',') for user_click_prd in user_click_prds]
        # print(user_click_prds)
        # sys.exit()

        skip_gram_creator = skip_gram_sampling(user_click_prds, 5)
        self.occurence_table = skip_gram_creator.create_occurence_table()
        self.pos_pairs_count = skip_gram_creator.get_pos_pairs()
        self.pos_context_set = skip_gram_creator.get_pos_context_set()
        
        
        self.neg_sample_table = skip_gram_creator.neg_sampling_table()
        self.neg_sample_population = list(self.neg_sample_table.keys())
        self.neg_sample_weights = list(self.neg_sample_table.values())

    def __len__(self):
        return len(self.pos_pairs_count) # 데이터셋의 길이. 즉, 총 샘플의 수를 적어주는 부분
    
    def __getitem__(self, idx):
        pos_pair_item = self.pos_pairs_count[idx]

        target_item = pos_pair_item[0]
        neg_pair_item = self.neg_sampling(target_item, self.negative_context_count)
                        
        pos_target_id = self.prdcd_to_id(pos_pair_item[0])
        pos_context_id = self.prdcd_to_id(pos_pair_item[1])
        
        return pos_target_id, pos_context_id, neg_pair_item # 데이터셋에서 특정 1개의 샘플을 가져오는 함수
    
    def get_prd_occurence_table(self):
        return self.occurence_table
    
    def get_prdcd_to_itemindex_dict(self):
        return self.prdcd_to_itemindex
    
    def get_itemindex_to_prdcd_dict(self):
        return self.itemindex_to_prdcd
    
    def get_prdcd_to_prdnm_dict(self):
        return self.prdcd_to_prdnm
    
    def get_prdnm_to_prdcd_dict(self):
        return self.prdnm_to_prdcd     
    
    def prdcd_to_id(self, prdcd):
        return int(self.prdcd_to_itemindex[prdcd][0])

    
    def neg_sampling(self, target_item, count):
        pos_context = self.pos_context_set[target_item]
        
        neg_sample = list()
        
        while( count > len(neg_sample)):
            neg_context = random.choices(population = self.neg_sample_population,
                                         weights = self.neg_sample_weights,
                                         k=count)
            neg_sample = list(set(neg_context) - pos_context)
        
        # target_item = self.prdcd_to_id(target_item)
        neg_context = [self.prdcd_to_id(tmp) for tmp in neg_sample]
        # print('neg_sample : ', neg_sample)
        # neg_pair = [(target_item, neg_context_item) for neg_context_item in neg_sample]
        return neg_context
        
        
     


# In[89]:

def test():
    cur_path = os.getcwd()
    items_path = os.path.join(cur_path, 'dataset/apmall/items.csv')
    items_dataset = Dataset_Process(items_path, 
                                    None, 
                                    None).zip_column_dict('prd_cd' ,'item_index')
    
    total_items = len(items_dataset)
    print("Total_Items : ", total_items)
    
    users_path = os.path.join(cur_path, 'dataset/apmall/users.csv')
    users_dataset = Dataset_Process(users_path,
                                    None,
                                    None)
    user_click_prds = users_dataset.get_column_data('prdcd_seq')
    user_click_prds = [user_click_prd.split(',') for user_click_prd in user_click_prds]

    # skip_gram_sampling(user_click_prds, 5).neg_sampling_table()
    item2vec_data = item2vec_dataset(neg_cnt=2)
    
    
    dataloader = DataLoader(item2vec_data, 
                            batch_size=10,
                            shuffle=True, 
                            num_workers=0)
    
    
    for idx, pair in enumerate(dataloader):
        print(pair)
        #pos_pair, neg_pair = pair
        #pos_pair = torch.tensor(pos_pair, dtype=torch.long)
        #pos_pair = torch.tensor(pos_pair, dtype=torch.long)
        #print("Pos_Pairs-", pos_pair, torch.tensor(pos_pair).size)
        #print("Neg_Pairs-", neg_pair, neg_pair.size)
        
        
        break

def item2vec_dataset_test():
    cur_path = os.getcwd()
    items_path = os.path.join(cur_path, 'dataset/apmall/items.csv')
    items_dataset = Dataset_Process(items_path,
                                    None,
                                    None)
    prd_cd_to_item_index = items_dataset.zip_column_dict('prd_cd', 'item_index')
    prd_cd_to_prd_nm = items_dataset.zip_column_dict('prd_cd', 'prd_nm')
    item_index_to_prd_nm = items_dataset.zip_column_dict('item_index', 'prd_nm')
    
    print( item_index_to_prd_nm.keys )


if __name__ == "__main__":
    
    item2vec_dataset_test() 

# https://discuss.pytorch.org/t/loading-huge-data-functionality/346/2

# In[ ]:




