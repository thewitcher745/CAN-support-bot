import json


def get_user_lists():
    """Get the full user lists from the JSON file."""
    with open('admin_panel/user_lists.json', 'r') as f:
        user_lists = json.load(f)

    return user_lists


def get_category_id_list():
    """Get the names and ID's of all categories."""
    user_lists = get_user_lists()
    category_id_list = []

    for category_id in user_lists.keys():
        label = user_lists[category_id]['label']
        category_id_list.append((category_id, label))

    return category_id_list


def get_categories_for_user(user_id):
    user_lists = get_user_lists()
    categories = []

    for category in user_lists.values():
        if user_id in category['users']:
            categories.append(category['label'])

    return categories


def add_user_to_category(user_id, category_id):
    """Add the user with ID user_id to category with ID category_id, if the user already exists in that list, do nothing."""
    user_lists = get_user_lists()

    if user_id in user_lists[category_id]['users']:
        return

    user_lists[category_id]['users'].append(user_id)

    print(user_lists)

    with open('admin_panel/user_lists.json', 'w') as f:
        json.dump(user_lists, f, indent=4)


def remove_user_from_category(user_id, category_id):
    """Remove the user with ID user_id from category with ID category_id, if the user does not exist in that list, do nothing."""
    user_lists = get_user_lists()

    if user_id not in user_lists[category_id]['users']:
        return

    user_lists[category_id]['users'].remove(user_id)

    print(user_lists)

    with open('admin_panel/user_lists.json', 'w') as f:
        json.dump(user_lists, f, indent=4)


def get_category_label_by_id(category_id):
    """Get the label of a category given its ID."""
    user_lists = get_user_lists()
    return user_lists[category_id]['label']


def is_user_admin(user_id):
    with open('admin_panel/admins.json', 'r') as f:
        admins = json.load(f)

    return user_id in admins['admins']
