import random, os, string, requests
from dotenv import load_dotenv

load_dotenv()


def generate_random_number(start, end):
    return random.randint(start, end)


random_number_for_price = generate_random_number(1, 9999)

# to be invalid the generated number should not be available in your database
random_number_for_category = generate_random_number(1, 5)

# to be invalid this number must be negative
random_number_for_inventory = generate_random_number(-10, -1)


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

random_string = generate_random_string(300)


api_url = 'http://localhost:8000/shop/products/'

data = {
    'title': random_string,
    'price': random_number_for_price,
    'inventory': random_number_for_inventory,
    'category': random_number_for_category
}


# to be invalid this image must be larger than 600 KB !
# you can also ignore this file cause it's optional
# but if you wanna test your validation you can set this
IMAGE_NAME = 'markus.jpg'
image_path = os.path.join(os.environ.get("PATH_TO_DJANGO_BASE_DIR"), 'media', IMAGE_NAME)
files = {'product_image': open(image_path, 'rb')}




response = requests.post(api_url, data=data, files=files)

print(response.status_code)
print(response.json())