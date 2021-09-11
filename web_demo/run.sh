#!/bin/sh
# Because source command is a Bash builtin, but not a sh builtin.
# To source a file in sh, you should use . (dot). . /etc/profile
#cd ..
#pwd
#pip list
#cd web_demo
streamlit run main.py --server.maxUploadSize=1028
