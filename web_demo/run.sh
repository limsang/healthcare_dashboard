#!/bin/zsh

cd ..
source venv/bin/activate
#pip list
cd web_demo
streamlit run main.py --server.maxUploadSize=1028