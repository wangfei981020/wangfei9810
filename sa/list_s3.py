import boto3
from botocore.exceptions import ClientError

# 配置
access_key = 'AKIA3YGR4PXGHKUZDUWY'
secret_key = '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'
region = 'ap-east-1'
bucket_name = 'ppu-s3'
prefix = 'ppu-tidb-back/'

def list_s3_files():
    try:
        # 使用显式凭证创建 S3 客户端
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        # 获取对象列表
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if 'Contents' not in response:
            print(f"⚠️ 没有找到任何对象在 {bucket_name}/{prefix}")
            return

        print(f"\n📂 文件列表（{bucket_name}/{prefix}）：\n")
        for obj in response['Contents']:
            print(obj['Key'])

    except ClientError as e:
        print(f"❌ S3 请求失败：{e.response['Error']['Message']}")

if __name__ == "__main__":
    list_s3_files()