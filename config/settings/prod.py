from .base import *

# AWS Secrets Manager 시작
import boto3, json
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name) -> dict:
    """
    Secrets Manager에서 비밀번호를 가져오는 함수
    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    
    # Your code goes here.
    return json.loads(secret)

# AWS Secrets Manager 끝


# AWS Parameter Store 시작
# if 'REGION_NAME' in os.environ:
#     '''
#     필요한 환경 변수와 충분한 권한이 있는 경우 mysql 접속을 시도하도록 수정
#     '''
#     # AWS SSM 클라이언트 인스턴스 생성
#     ssm_client = boto3.client("ssm", region_name=os.getenv('REGION_NAME'))

#     # Parameter Store에 저장되어 있는 변수 가져오기
#     try:
#         secret_name = ssm_client.get_parameter(Name='/altudy/rds/secret_name', WithDecryption=True).get('Parameter').get('Value')
#         hostname = ssm_client.get_parameter(Name='/altudy/rds/hostname', WithDecryption=True).get('Parameter').get('Value')
#         db_name = ssm_client.get_parameter(Name='/altudy/rds/db_name', WithDecryption=True).get('Parameter').get('Value')


#         # Use this code snippet in your app.
#         # If you need more information about configurations
#         # or implementing the sample code, visit the AWS docs:
#         # https://aws.amazon.com/developer/language/python/

#         # mysql database
#         # https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html
#         if 'RDS_PORT' in os.environ and 'REGION_NAME' in os.environ:
#             try:
#                 secrets = get_secret(
#                     secret_name=secret_name,
#                     region_name=os.getenv('REGION_NAME'),
#                 )
#                 '''
#                 Model Manager를 'users' DB를 사용하도록 일일이 커스텀 할 수 없어서
#                 RDS 관련 정보가 환경변수에 있는 경우 MySQL을 디폴트 DB로 사용하도록 수정
#                 '''
#                 DATABASES['default'] = {
#                     'ENGINE': 'django.db.backends.mysql',
#                     'NAME': db_name,
#                     'USER': secrets.get('username'),
#                     'PASSWORD': secrets.get('password'),
#                     'HOST': hostname,
#                     'PORT': os.getenv('RDS_PORT'),
#                     'OPTIONS': {
#                         'sql_mode': 'STRICT_ALL_TABLES'
#                     },
#                 }
#             except ClientError as e:
#                 print("에러 내용(Secrets Manager) :", e.response)

#     except ClientError as e:
#         if e.response['Error']['Code'] == 'AccessDeniedException':
#             print("Parameter Store로 접근이 거부되었습니다.")
#         else:
#             print("에러 내용(Parameter Store) :", e.response)

# AWS Parameter Store 끝


SECRET_KEY = get_secret(
    secret_name='DJANGO_SECRET_KEY',
    region_name=os.getenv('REGION_NAME')
).get('DJANGO_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['*']

AWS_STORAGE_BUCKET_NAME = "altudy-bucket-2023"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + ".s3.ap-northeast-2.amazonaws.com"
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False

# STATIC_ROOT = BASE_DIR / 'static'

STORAGES = {
    "staticfiles": {"BACKEND": "config.storage.S3Storage"}
}

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]