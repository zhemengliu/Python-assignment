class HashableItem:

    def __init__(self, id, data):
        self.id = id
        self.data = data
    
    def __eq__(self, other):
        if not isinstance(other, HashableItem):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

item1 = HashableItem(1, "A")
item2 = HashableItem(1, "B")
item3 = HashableItem(2, "A")

print(item1 == item2)  
print(item1 == item3)  

unique_set = {item1, item2, item3}
print(f"集合大小: {len(unique_set)}")
