# Function to validate if entities are equal or not
def equals(obj1, obj2):
    if obj1.__class__ == obj2.__class__:
        return obj1.__dict__ == obj2.__dict__
    else:
        return False
