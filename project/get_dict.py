from project.models import Users, Products, Images, Orders, Cart


# take a list and return list of unique items
def unique(lst):
    unique_lst = []
    for i in lst:
        if i not in unique_lst:
            unique_lst.append(i)
    return unique_lst


# take products as list and return list of images in 2d list with first two indexes of primary and secondary images for each product
def get_images(products):
    images_list = [] # 2d array to store images of all products
    for i in products:
        product_id = i.id
        images = Images.query.with_entities(Images.filename).filter_by(product_id=product_id).order_by("order").all()
        images = [i[0] for i in images] # save only first item of each row since we only need filename of images
        if not images:
            images.append(None)
        images_list.append(images)
    return images_list


def get_images_data(products):
    images_dict = {}
    for prd in products:
        product_id = prd.id
        images = Images.query.filter_by(product_id=product_id).order_by("order").all()
        images_list = []
        for img in images:
            image = {
                'id': img.id,
                'filename': img.filename
            }
            images_list.append(image)
        images_dict[product_id] = images_list
    return images_dict


def get_product_dict(products):
    products_dict = []
    for prd in products:
        product = {
            'id': prd.id,
            'title': prd.title,
            'category': prd.category,
            'price': prd.price,
            'details': prd.details,
            'core_collection': prd.core_collection,
        }
        products_dict.append(product)
    return products_dict


# just get products as dictionary but not as array
def get_product_dict_id(products):
    products_dict = {}
    for prd in products:
        product = {
            'title': prd.title,
            'price': prd.price,
            'category': prd.category,
        }
        products_dict[prd.id] = product
    return products_dict


def get_images_dict(images):
    images_dict = []
    for img in images:
        image = {
            'id': img.id,
            'title': img.title,
            'filename': img.filename,
        }
        images_dict.append(image)
    return images_dict


def get_orders_dict(orders):
    orders_dict = {}
    for o in orders:
        order = {
            'f_name': o.f_name,
            'l_name': o.l_name,
            'address': o.address,
            'city': o.city,
            'postal_code': o.postal_code,
            'phone': o.phone,
            'note': o.note,
            'status': o.status
        }
        orders_dict[o.id] = order
    return orders_dict


def get_cart_dict(cart):
    cart_dict = {}
    for i in cart:
        if not cart_dict.get(i.order_id):
            cart_dict[i.order_id] = []
        item = {
            'product': i.product_id,
            'quantity': i.quantity
        }
        cart_dict[i.order_id].append(item)
    return cart_dict

