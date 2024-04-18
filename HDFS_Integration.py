from hdfs import InsecureClient

# Connect to HDFS
client = InsecureClient('http://localhost:9870', user='username')

# Upload file to HDFS
client.upload('/user/username/example.txt', 'example.txt')

# Download file from HDFS
client.download('/user/username/example.txt', 'example_downloaded.txt', overwrite=True)
