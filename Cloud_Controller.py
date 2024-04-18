import os
import shutil
from Crypto.Cipher import AES

class CloudController:
    def __init__(self):
        self.segment_size = 1024  # Segment size in bytes
        self.key = b'my_secret_key_123'  # Encryption key

    def segment_file(self, input_file):
        segments = []
        with open(input_file, 'rb') as f:
            while True:
                segment = f.read(self.segment_size)
                if not segment:
                    break
                segments.append(segment)
        return segments

    def encrypt_segment(self, segment):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(segment)

    def decrypt_segment(self, encrypted_segment):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.decrypt(encrypted_segment)

    def upload_file(self, input_file):
        segments = self.segment_file(input_file)
        encrypted_segments = [self.encrypt_segment(segment) for segment in segments]
        # Upload encrypted_segments to HDFS or cloud storage

    def download_file(self, output_file):
        # Download encrypted_segments from HDFS or cloud storage
        encrypted_segments = []
        # Decrypt and reconstruct original file
        with open(output_file, 'wb') as f:
            for encrypted_segment in encrypted_segments:
                decrypted_segment = self.decrypt_segment(encrypted_segment)
                f.write(decrypted_segment)

# Example usage
controller = CloudController()
controller.upload_file('example.txt')
controller.download_file('example_downloaded.txt')
