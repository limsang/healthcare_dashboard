#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
import random
from collections import Counter


# In[2]:


class SGNS(nn.Module):
    def __init__(self, vocab_size, emb_dim):
        super(SGNS, self).__init__()
        self.target_emb = nn.Embedding(vocab_size, emb_dim)
        self.context_emb = nn.Embedding(vocab_size, emb_dim)
        self.log_sigmoid = nn.LogSigmoid()
    
        init_range =(2.0 / (vocab_size + emb_dim)) ** 0.5 # Xaiver init
        self.target_emb.weight.data.uniform_(-init_range, init_range)
        self.context_emb.weight.data.uniform_(-0, 0)
    
    def forward(self, target_input, context, neg):
        """
        : param target_input : [batch_size]
        : param context : [batch_size]
        : param neg : [batch_size, neg_size]
        : return :
        """
        #print("\tIn Model : input size", target_input.size())
        
        # u, v : [batch_size, emb_dim]
        v = self.target_emb(target_input)
        u = self.context_emb(context)
        # positive_val : [batch_size]
        positive_val = self.log_sigmoid(torch.sum(u*v, dim=1)).squeeze()
        
        # u_hat : [batch_size, neg_size, emb_dim]
        u_hat = self.context_emb(neg)
        # [batch_size, neg_size, emb_dim] X [batch_size, emb_dim, 1] = [batch_size, neg_size, 1]
        # neg_vals : [batch_size, neg_size]
        
        # print('neg with batch : ', neg.shape)
        # print('u_hat : ', u_hat.shape)
        
        neg_vals = torch.bmm(u_hat, v.unsqueeze(2)).squeeze(2)
        # neg_val : [batch_size]
        neg_val = self.log_sigmoid(-torch.sum(neg_vals, dim=1)).squeeze()
        
        loss = positive_val + neg_val
        
        #print("\tIn Model : input size", loss.mean().size())
        
        return -loss.mean()
    
    def predict(self, inputs):
        return self.target_emb(inputs)