from item2vec import ApRecsys_Item2Vec
from config.config import config 
import boto3
import mlflow as mf
import sys

def download_training_raw_data(s3_source_bucket, s3_download_prefix, destination_path, destination_filename):
    bucket_name = s3_source_bucket
    prefix = s3_download_prefix + '/' + destination_filename.split('.')[0]    
    destination = destination_path + destination_filename

    s3 = boto3.client('s3')
    
    csv_file = ""
    for i, obj in enumerate(s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)['Contents']):
        if obj['Key'].find("csv") != -1:
            csv_file = obj['Key']
    
    try:
        print(f"Download File From - {bucket_name}, Key - {obj['Key']}, Destination - {destination}")
        s3.download_file(bucket_name, obj['Key'], destination)
    except Exception as e:
        print('Exception : ', str(e))


def upload_recommendation_list(s3_upload_bucket, source_path, source_filename):
    source = source_path + '/' + source_filename

    s3 = boto3.client('s3')

    try:
        print(f"Upload File From - {source}, Destination - {s3_upload_bucket}")
        response = s3.upload_file(source, s3_upload_bucket)
    except Exception as e:
        print('Exception : ', str(e))

    print(response)
    

def train():
    # print("Progress Start")
    # print("Download Training Data")
    # run_env = "DEVELOP" # os.environ['RUN_ENV']
    # params = config().get_config()
    # download_bucket = params[run_env]["AWS"]["S3"]["TRAIN_DATA_BUCKET"]
    # download_prefix = params[run_env]["AWS"]["S3"]["TRAIN_DATA_PREFIX"]
    #
    # destination_path = params[run_env]["MODEL"]["TRAIN_DATA_PATH"]
    # destination_filename = [ params[run_env]["MODEL"]["TRAIN_DATA_ITEMS_NAME"], params[run_env]["MODEL"]["TRAIN_DATA_USERS_NAME"]]
    #
    # download_training_raw_data(download_bucket, download_prefix, destination_path, destination_filename[0])
    # download_training_raw_data(download_bucket, download_prefix, destination_path, destination_filename[1])
    
    print("Training Start")
    item2vec = ApRecsys_Item2Vec()

    item2vec.train()

    print("Load Model")
    item2vec.load_model()

    print("Get All Items Similar Items")
    item2vec.get_all_items_similar_items()
    item2vec.gen_item_info_json()
    item2vec.gen_prdnm_code_json()

    # s3_upload_bucket = params[run_env]["AWS"]["S3"]["RECSYS_RESULT_BUCKET"]
    # source_path = params[run_env]["MODEL"]["RECOMMENDATION_LIST_PATH"]
    # source_filename = params[run_env]["MODEL"]["RECOMMENDATION_LIST_NAME"]
    #
    # upload_recommendation_list(s3_upload_bucket, source_path, source_filename)
    # print("Progress Done")
    # print("Terminate")

if __name__ == "__main__":
    train()
