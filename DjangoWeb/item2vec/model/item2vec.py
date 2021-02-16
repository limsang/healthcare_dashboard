#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import os

from model.model import SGNS
from data_utils.data_utils import item2vec_dataset
from termcolor import colored
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from config.config import config
import sys
import csv, json
from collections import OrderedDict


class ApRecsys_Item2Vec(object):

    def __init__(self):
        # config
        params = config().get_config()
        run_env = "DEVELOP"  # os.environ['RUN_ENV']
        branch = "MODEL"

        self.device_type = params[run_env][branch]["DEVICE_TYPE"]
        self.dataloader_workers = params[run_env][branch]["DATALOADER_WORKERS"]
        self.train_epochs = params[run_env][branch]["TOTAL_EPOCH"]
        self.batch_size = params[run_env][branch]["BATCH_SIZE"]
        self.print_train_iter = params[run_env][branch]["TRAINING_LOG_PER_ITERATION"]
        self.learning_rate = params[run_env][branch]["LEARNING_RATE"]
        self.window_size = params[run_env][branch]["WINDOW_SIZE"]
        self.negative_sample_count = params[run_env][branch]["WINDOW_SIZE"]
        self.emb_dim = params[run_env][branch]["EMBEDDING_DIMENSION"]
        self.train_item_data_path = params[run_env][branch]["TRAIN_DATA_PATH"] + params[run_env][branch][
            "TRAIN_DATA_ITEMS_NAME"]
        self.train_user_data_path = params[run_env][branch]["TRAIN_DATA_PATH"] + params[run_env][branch][
            "TRAIN_DATA_USERS_NAME"]
        self.model_save_dir = params[run_env][branch]["MODEL_SAVE_PATH"]
        self.model_load_dir = params[run_env][branch]["MODEL_LOAD_PATH"]
        self.model_log_dir = params[run_env][branch]["MODEL_LOG_PATH"]
        self.tensorboard_logdir = params[run_env][branch]["TENSORBOARD_PATH"]
        self.early_stop_patience_limit = params[run_env][branch]["EARLYSTOPPING_PATIENCE_COUNT"]
        self.early_stop_delta = params[run_env][branch]["EARLYSTOPPING_DELTA"]
        self.recommend_list_path = params[run_env][branch]["RECOMMENDATION_LIST_PATH"]
        self.recommend_list_name = params[run_env][branch]["RECOMMENDATION_LIST_NAME"]
        self.code_recommend_list_name = params[run_env][branch]["RECOMMENDATION_LIST_NAME_API"]

        print("Train Epochs : ", self.train_epochs)
        print("Model Initialize start ...")
        self.device = torch.device(self.device_type)

        self.early_stop_condition = None
        self.early_stop_patience_count = 0
        self.early_stop_memorized_score = None

        self.dataset = self.load_train_dataset()
        self.prd_occurence_table = self.dataset.get_prd_occurence_table()
        self.prdcd_to_itemindex = self.dataset.get_prdcd_to_itemindex_dict()
        self.itemindex_to_prdcd = self.dataset.get_itemindex_to_prdcd_dict()
        self.prdcd_to_prdnm = self.dataset.get_prdcd_to_prdnm_dict()
        self.prdnm_to_prdcd = self.dataset.get_prdnm_to_prdcd_dict()
        self.vocab_size = len(self.itemindex_to_prdcd)

        self.model = SGNS(vocab_size=self.vocab_size,
                          emb_dim=self.emb_dim)

        if (self.device_type == 'cuda'):
            self.model = self.model.to(self.device)

        self.optimizer = torch.optim.Adam(params=self.model.parameters(),
                                          lr=self.learning_rate)
        print("Model Initialize done ...")

    def load_train_dataset(self):
        dataset = item2vec_dataset(item_data_path=self.train_item_data_path,
                                   user_data_path=self.train_user_data_path,
                                   neg_cnt=self.negative_sample_count)
        return dataset

    def train(self):
        self.early_stop_condition = False

        print(colored("Training Start", "yellow"))
        trainloader = DataLoader(dataset=self.dataset,
                                 batch_size=self.batch_size,
                                 shuffle=True,
                                 num_workers=self.dataloader_workers)

        for epoch in range(self.train_epochs):
            average_loss = 0
            train_data_index = 0
            for train_data_index, train_data_val in enumerate(trainloader):
                pos_target_id, pos_context_id, neg_context_ids = train_data_val
                neg_context_ids = torch.stack(neg_context_ids, dim=1)

                pos_target_id = pos_target_id.to(self.device)
                pos_context_id = pos_context_id.to(self.device)
                neg_context_ids = neg_context_ids.to(self.device)

                loss = self.model(pos_target_id,
                                  pos_context_id,
                                  neg_context_ids)

                self.optimizer.zero_grad()
                loss = loss.mean()
                loss.backward()
                self.optimizer.step()

                average_loss += loss.item()

                self.early_stop_condition = self.early_stopping(epoch, train_data_index, loss.item())

                if (self.early_stop_condition == True): break

                if (train_data_index % self.print_train_iter == 0):
                    print(colored(f" Loss per Iter {train_data_index} - Loss {loss.item()}", 'blue'))

            average_loss = average_loss / train_data_index
            print(colored(f"\tAverage Loss per Epoch {epoch} - Avg Loss {average_loss}", 'green'))

            self.save_model(mode='checkpoint', epoch=epoch)

            if (self.early_stop_condition == True): break

        self.save_model(mode='inference')

    def early_stopping(self, epoch, epoch_iter, loss):
        if (self.early_stop_memorized_score is None):
            self.early_stop_memorized_score = loss
        elif (loss < self.early_stop_memorized_score - self.early_stop_delta):
            self.early_stop_patience_count = 0
        else:
            self.early_stop_patience_count += 1
            print(colored(
                f"\tEarly Stopping on Epoch {epoch}, Iter {epoch_iter} - Status {self.early_stop_patience_count}/{self.early_stop_patience_limit} Loss {loss}",
                'red'))
            if (self.early_stop_patience_count > self.early_stop_patience_limit):
                return True

        return False

    def serve(self):
        pass

    def save_model(self, mode='inference', epoch=None):
        if (mode == 'inference'):
            torch.save(self.model.state_dict(), self.model_save_dir + '/inference.pt')
        elif (mode == 'checkpoint'):
            torch.save({
                'epoch': epoch,
                'state_dict': self.model.state_dict(),
                'optimizer': self.optimizer.state_dict(),
            },
                self.model_save_dir + '/checkpoint_%d.pt' % epoch)

        elif (mode == 'abstract'):
            torch.save(self.model, self.model_save_dir + '/abstract.pt')
        else:
            pass

    def load_model(self, mode='inference', epoch=None):
        if (mode == 'inference'):
            self.model.load_state_dict(torch.load(self.model_load_dir + '/inference.pt'))
            if (self.device_type == 'cuda'):
                # self.model.module.eval()
                self.model.eval()  # is for validate
            else:
                self.model.eval()

        elif (mode == 'checkpoint'):
            checkpoint = torch.load(self.model_load_dir + '/checkpoint_%d.pt' % epoch)
            self.model.load_state_dict(checkpoint['state_dict'])
            self.optimizer.load_sate_dict(checkpoint['optimizer'])
            epoch = checkpoint['epoch']
            self.model.train()

        elif (mode == 'abstract'):
            self.model = torch.load(self.model_load_dir + '/abstract.pt')
        else:
            pass

    def total_items(self):
        return len(self.prdcd_to_itemindex)

    def get_target_embeddings(self):
        model_state_dict = None

        if (self.device_type == 'cuda'):
            # model_state_dict = self.model.module.state_dict()
            model_state_dict = self.model.state_dict()
        else:
            model_state_dict = self.model.state_dict()

        return model_state_dict['target_emb.weight']

    def get_context_embeddings(self):
        model_state_dict = None

        if (self.device_type == 'cuda'):
            # model_state_dict = self.model.module.state_dict()
            model_state_dict = self.model.state_dict()
        else:
            model_state_dict = self.model.state_dict()

        return model_state_dict['context_emb.weight']

    def save_vector_text(self):
        target_emb = self.get_target_embeddings()
        context_emb = self.get_context_embeddings()

        target_emb_list = target_emb.tolist()
        context_emb_list = context_emb.tolist()

        with open(self.model_save_dir + '/target_emb_vector.csv', 'w') as target_file:
            for idx, val in enumerate(target_emb_list):
                item_code = self.itemindex_to_prdcd[str(idx)][0]
                # item_name = self.prdcd_to_prdnm[item_code]
                embed_list = [str(i) for i in val]
                line_str = ',\t'.join(embed_list)
                # target_file.write(item_code + ',\t' + item_name + ',\t' + line_str + '\n')
                target_file.write(item_code + ',\t' + line_str + '\n')
                if (idx > 3600): break

    def most_similar(self, item_code, top_k=10):

        item_index = int(self.prdcd_to_itemindex[str(item_code)][0])
        input_item_index = torch.tensor(item_index, dtype=torch.long).to(self.device).unsqueeze(0)

        input_embedding = None
        total_embedding = None

        if (self.device_type == 'cuda'):
            # input_embedding = self.model.module.predict(input_item_index) # (1, 300)
            # total_embedding = self.model.module.target_emb.weight.transpose(0,1) # (300, 4000)
            input_embedding = self.model.predict(input_item_index)  # (1, 300)
            total_embedding = self.model.target_emb.weight.transpose(0, 1)  # (300, 4000)

        else:
            input_embedding = self.model.predict(input_item_index)  # (1, 300)
            total_embedding = self.model.target_emb.weight.transpose(0, 1)  # (300, 400)

        similarity = torch.mm(input_embedding, total_embedding)

        top_n = 10
        sort_similarity = (-similarity[0]).sort()[1][1:top_n + 1]
        # print(len(sort_similarity))
        # sys.exit()
        final_list_as_code = [self.itemindex_to_prdcd[str(idx.item())][0] for idx in sort_similarity]
        final_list_as_name = [self.prdcd_to_prdnm[c][0] for c in final_list_as_code]

        # for c, n in zip(final_list_as_code, final_list_as_name):
        #    print(c, n)

        return final_list_as_code, final_list_as_name

    def get_top_occur_prdcd(self, top_n=10):
        # print(self.prd_occurence_table)
        sorted_occur_table = sorted(self.prd_occurence_table.items(), key=lambda item: item[1], reverse=True)
        test_candidates = [item[0] for item in sorted_occur_table]
        return test_candidates[:top_n + 1]

    # def test_case_1(self, top_n, top_k):
    #     candidates = self.get_top_occur_prdcd(top_n=top_n)
    #
    #     header = ['연관아이템' + str(i+1) for i in range(top_k)]
    #     header.insert(0,'타깃아이템')
    #     with open(self.recommend_list_path + '/test_case_1.tsv', 'w', encoding='utf8') as test_case:
    #         test_case.write(',\t'.join(header) + '\n')
    #         for candidate in candidates:
    #             _, final_list_as_name = self.most_similar(candidate, top_k=top_k)
    #             final_list_as_name.insert(0, self.prdcd_to_prdnm[candidate][0])
    #             test_case.write(',\t'.join(final_list_as_name) + '\n')
    #
    def get_all_items_similar_items(self):
        candidates = self.get_top_occur_prdcd(top_n=-2)

        with open(self.recommend_list_path + '/' + self.recommend_list_name, 'w') as test_case:
            writer = csv.writer(test_case)
            for candidate in candidates:
                _, final_list_as_name = self.most_similar(candidate, top_k=-2)
                final_list_as_name.insert(0, self.prdcd_to_prdnm[candidate][0])
                writer.writerow(final_list_as_name)
                # test_case.write(',\t'.join(final_list_as_name) + '\n')

        with open(self.recommend_list_path + '/' + self.code_recommend_list_name, 'w') as test_case:
            writer = csv.writer(test_case)
            for candidate in candidates:
                final_list_as_code, final_list_as_name = self.most_similar(candidate, top_k=-2)
                final_list_as_code.insert(0, candidate)
                writer.writerow(final_list_as_code)

    def load_json_data(self, prd_nm):
        with open("item_info.json", 'r') as f:
            json_data = json.load(f)

    def gen_item_info_json(self):
        # print(self.prdnm_to_prdcd['랑팔라투르 유기농 비누 마르세유 벌트 600g'][0])

        f = open('model_output/item2vec_recommend_list.csv', 'r', encoding='utf-8')
        code_f = open('model_output/code_item2vec_recommend_list.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)
        code_rdr = csv.reader(code_f)

        file_data = OrderedDict()
        file_member = OrderedDict()

        # base = name
        for index, item in enumerate(rdr):
            file_member['target_item'] = item[0]
            file_member['rec_items'] = item[1:]
            file_data[self.prdnm_to_prdcd[item[0]][0]] = file_member

        # base = code
        for index, item in enumerate(code_rdr):
            file_member['rec_items_cd'] = item[1:]
            file_data[item[0]] = file_member

        # 한글 인코딩
        json_val = json.dumps(file_data, ensure_ascii=False, indent="\t")
        with open("item_info.json", 'w') as f:
            f.write(json_val)

    def gen_prdnm_code_json(self):

        file_data = OrderedDict()
        for index, item in enumerate(self.prdnm_to_prdcd):
            file_data[self.prdnm_to_prdcd[item][0]] = item

        # 한글 인코딩
        json_val = json.dumps(file_data, ensure_ascii=False, indent="\t")
        with open("code_name.json", 'w') as f:
            f.write(json_val)


def test():
    item2vec = ApRecsys_Item2Vec()
    # item2vec.train()
    item2vec.load_model()
    item2vec.test_case_1(100, 10)


"""
#from torch.utils.tensorboard import SummaryWriter
def tensorboard_add_embedding():
    print("WHAT")
    item2vec = ApRecsys_Item2Vec()
    item2vec.load_model()
    writer = SummaryWriter('runs/experiment_1')
    item_embedding = item2vec.get_context_embeddings()

    item_names = []
    for k, v in item2vec.itemindex_to_prdcd.items():
        #print(k, v, item2vec.prdcd_to_prdnm[v[0]][0])
        item_names.append(item2vec.prdcd_to_prdnm[v[0]][0])
    writer.add_embedding(mat=item_embedding, metadata=item_names)

if __name__ == "__main__":
    tensorboard_add_embedding()



"""