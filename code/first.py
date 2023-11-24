# import uuid

# def generate_short_id(length=8):
#     # Generate a UUID
#     new_uuid = uuid.uuid4()

#     # Convert the UUID to a hex string and truncate to the desired length
#     short_id = str(new_uuid.hex)[:length]

#     return short_id

# # Example usage
# short_id = generate_short_id()
# print(short_id)

import uuid

def generate_short_id():
    uuid_obj = uuid.uuid4()
    short_id = int(uuid_obj) % 1000000  # 1000000 is 10^6, ensuring a 6-digit number
    return short_id

# Example usage
short_id = generate_short_id()
print(short_id)

