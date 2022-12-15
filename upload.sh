# Make sure the AWS CLI is installed
if ! [ -x "$(command -v aws)" ]; then
  echo 'Error: AWS CLI is not installed. Try pip install awscli ' >&2
  exit 1
fi

# Set the path to the directory to upload
dir_path=./mds-pol

# Set the S3 bucket URL
bucket_url=s3://mosaicml-internal-checkpoints-shared/sam/pile-of-law

# Upload the directory to the S3 bucket
aws s3 cp $dir_path $bucket_url --recursive
