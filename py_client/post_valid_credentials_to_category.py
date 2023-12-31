import random, os, string, requests
from dotenv import load_dotenv

load_dotenv()

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

random_string = generate_random_string(60)


api_url = 'http://localhost:8000/shop/categories/'

data = {
    'title': random_string,
}

# to be valid this image must be less than 600 KB !!
IMAGE_NAME = 'anonymous.jpg'

image_path = os.path.join(os.environ.get("PATH_TO_DJANGO_BASE_DIR"), 'media', IMAGE_NAME)

files = {'thumbnail': open(image_path, 'rb')}

response = requests.post(api_url, data=data, files=files)

print(response.status_code)
print(response.json())