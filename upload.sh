# Make sure the AWS CLI is installed
if ! [ -x "$(command -v aws)" ]; then
  echo 'Error: AWS CLI is not installed. Try pip install awscli ' >&2
  exit 1
fi

# Make sure there is an s3 bucket passed
if (( $# != 1 )); then
    >&2 echo "This script takes one argument; the s3 bucket URI"
fi

# Set the path to the directory to upload
dir_path=./mds-pol

# Set the S3 bucket URL
bucket_url="$1"

# Upload the directory to the S3 bucket
aws s3 cp $dir_path $bucket_url --recursive
