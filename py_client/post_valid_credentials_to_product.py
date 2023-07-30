import random, os, string, requests
from dotenv import load_dotenv

load_dotenv()


def generate_random_number(start, end):
    return random.randint(start, end)


random_number_for_price = generate_random_number(10000, 100000)

# depends on how many categories is available in your database
# the following number must be in the range of your categories
random_number_for_category = generate_random_number(1, 5)

random_number_for_inventory = generate_random_number(1, 10)



def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

random_string = generate_random_string(60)


api_url = 'http://localhost:8000/shop/products/'

data = {
    'title': random_string,
    'price': random_number_for_price,
    'inventory': random_number_for_inventory,
    'category': random_number_for_category
}


# to be valid this image must be less than 600 KB !!
IMAGE_NAME = 'tarik.jpg'

image_path = os.path.join(os.environ.get("PATH_TO_DJANGO_BASE_DIR"), 'media', IMAGE_NAME)

files = {'product_image': open(image_path, 'rb')}

response = requests.post(api_url, data=data, files=files)

print(response.status_code)
print(response.json())