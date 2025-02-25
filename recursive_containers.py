"""
This program is a loot management system that handles items and containers, including basic containers, 
multi-containers, and magic containers/ multi magic_containers. It allows users to select containers, loot items, and store 
them based on available capacity. Additionally, users can also loot a container. Data is read from CSV files.
"""
import csv
import copy

class ReadFile:
    """
    Represents a class to read item & container file.
    """
    def read_items() -> None:
        """
        Read the item.csv and create item objects and store them on a list
        """
        with open("items.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip the header
            for row in reader:
                items[row[0]] = Item(row[0], row[1])
              
    def read_containers() -> None:
        """
        Read the containers.csv and create container objects and store them on a list
        """
        with open("containers.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip the header
            for row in reader:
                containers[row[0]] = Container(row[0], row[1], row[2])

class Container:
    """
    Represents a container that stores items and tracks its weight and capacity.
    """
    def __init__(self, name: str, weight: str, capacity: str) -> None:
        """
        Initializes the Container with a name, weight, and capacity.

        Parameters:
        name (str): The name of the container.
        weight (str): The weight of the empty container.
        capacity (str): The maximum capacity of the container.
        """
        self.name = name
        self.weight = int(weight)
        self.capacity = int(capacity)
        self.contents = []
        self.used_capacity = 0
        self.upper = None  


    def add_item(self, item: object, upper: object) -> None:
        """
        Adds an item to the container if it fits within the remaining capacity.

        Parameters:
        item (object): The item to add.
        upper (object): The upper container to be set.
        """
        if not isinstance(item, (MultiContainer, MagicMulti)):
            item_weight = item.weight
        else: 
            item_weight = item.empty_weight
        item.upper = upper
        self.used_capacity += item_weight
        self.contents.append(item)


    def remaining_capacity(self) -> int:
        """
        Returns the remaining capacity of the container.

        Returns:
        remainingCapacity (int): The available capacity left in the container.
        """
        remainingCapacity = self.capacity - self.used_capacity
        return remainingCapacity


    def total_weight(self) -> int:
        """
        Counts the total weight of the container, including its items.

        Returns:
        totalWeight (int): The total weight of the container and its items.
        """
        totalWeight = self.used_capacity + self.weight
        return totalWeight


    def copy_container(self) -> object:
        """
        Create a copy of a container

        Returns:
        copiedCon (object): The copied container's details and its items.
        """
        copiedCon = Container(self.name, self.weight, self.capacity)
        copiedCon.contents = copy.deepcopy(self.contents)
        copiedCon.used_capacity = self.used_capacity
        return copiedCon


    def __str__(self) -> str:
        """
        Returns a string representation of the container and its items.

        Returns:
        str: The container's name, weight and capacity.
        """
        return f"{self.name} (total weight: {self.total_weight()}, empty weight: {self.weight}, capacity: {self.used_capacity}/{self.capacity})"

class Item:
    """
    Represents an item with a name and weight.
    """
    def __init__(self, name: str, weight: str) -> None:
        """
        Initializes the Item with a name and weight.

        Parameters:
        name (str): The name of the item.
        weight (str): The weight of the item.
        """
        self.name = name
        self.weight = int(weight)
        self.upper = None  

    def set_upper(self, upper: object) -> None:
        """
        Set the upper container of the item.

        Parameters:
        upper (object): The upper container object of the item.
        """
        self.upper = upper


    def __str__(self) -> str:
        """
        Returns a string representation of the item.

        Returns:
        str: The item's name and weight as a string.
        """
        return f"{self.name} (weight: {self.weight})"


class MultiContainer:
    """
    Represents a container with multiple compartments.
    """
    def __init__(self, name: str, compartments: list) -> None:
        """
        Initializes the MultiContainer with a name and a list of compartments.

        Parameters:
        name (str): The name of the multi-container.
        compartments (list): A list of Container objects acting as compartments.
        """
        self.name = name
        self.compartments = compartments
        self.empty_weight = sum(multi_container.weight for multi_container in compartments)
        self.used_capacity = 0


    def total_weight(self) -> int:
        """
        Returns the total weight of the multi-container, including all compartments.

        Returns:
        totalWeight (int): The total weight of the multi-container.
        """
        totalWeight = 0
        for multi_container in self.compartments:
            totalWeight += multi_container.total_weight()

        return totalWeight


    def __str__(self)-> str:
        """
        Returns a string representation of the multi-container and its compartments.

        Returns:
        str: The multi-container's details and its compartments.
        """
        return f"{self.name} (total weight: {self.total_weight()}, empty weight: {self.empty_weight}, capacity: 0/0)"


class MagicContainer(Container):
    """
    Represents a magic container where the total weight and capacity are derived from other containers.
    It inherits from Container class.
    """
    def __str__(self) -> str:
        """
        Returns a string representation of the magic container and its compartments.

        Returns:
        str: The magic container's details and its compartments.
        """
        return f"{self.name} (total weight: {self.weight}, empty weight: {self.weight}, capacity: {self.used_capacity}/{self.capacity})"


class MagicMulti(MultiContainer):
    """
    Represents a magic multi container that holds magic compartments.
    It inherits from MultiContainer class.
    """
    def __str__(self)-> str:
        """
        Returns a string representation of the magic multi container and its compartments.

        Returns:
        str: The magic multi container's details and its compartments.
        """
        return f"{self.name} (total weight: {self.empty_weight}, empty weight: {self.empty_weight}, capacity: 0/0)"


class CreateContainers:
    """
    Represents a class to read multi_containers, 
    magic_containers and magic_multi_containers file.
    """
    def create_multi_containers() -> None:
        """
        Read the multi_containers.csv and create multi containers objects 
        and store them on a list
        """
        with open("multi_containers.csv",'r') as fileName:
            lines = csv.reader(fileName, skipinitialspace=True)
            next(lines)  # skip the header 
            for container in lines:
                compartments = [containers.get(name).copy_container() for name in container[1:]]
                multi_containers[container[0]] = MultiContainer(container[0], compartments)
                for compartment in multi_containers[container[0]].compartments:
                    compartment.upper = multi_containers[container[0]]


    def create_magic_containers() -> None:
        """
        Read the magic_containers.csv and create magic containers objects 
        and store them on a list
        """
        with open("magic_containers.csv", 'r') as fileName:
            lines = csv.reader(fileName, skipinitialspace=True)
            next(lines)  # skip the header
            for container in lines:
                container_copy1 = copy.deepcopy(containers.get(container[1]))
                magic_containers[container[0]] = MagicContainer(container[0], container_copy1.weight, container_copy1.capacity)


    def create_magic_multi_container() -> None:
        """
        Read the magic_multi_containers.csv and create magic multi containers objects 
        and store them on a list
        """
        with open("magic_multi_containers.csv",'r') as fileName:
            lines = csv.reader(fileName, skipinitialspace=True)
            next(lines)  # skip the header
            for container in lines:
                multi_container_copy1 = copy.deepcopy(multi_containers.get(container[1]))
                magic_multi_containers[container[0]] = MagicMulti(container[0], multi_container_copy1.compartments)
                for compartment in magic_multi_containers[container[0]].compartments:
                    compartment.upper = magic_multi_containers[container[0]]


class LootManager:
    """
    Manages items, containers, and multi-containers by loading them from CSV files 
    and performing operations.
    """
    def initialise() -> None:
        """
        Initialize the program by reading all the txt files.
        """
        ReadFile.read_items()
        ReadFile.read_containers()
        CreateContainers.create_multi_containers()
        CreateContainers.create_magic_containers()
        CreateContainers.create_magic_multi_container()

        # Calculate total counts off all items and containers
        total_items = len(items) + len(containers) + len(multi_containers) + len(magic_containers) + len(magic_multi_containers)
        total_containers = len(containers) + len(multi_containers) + len(magic_containers) + len(magic_multi_containers)

        print(f"Initialised {total_items} items including {total_containers} containers.\n")


    def select_container() -> None:
        """
        Select a container based on user input.
        """
        name = input("Enter the name of the container: ")
        if name in containers:
            user_container = copy.deepcopy(containers.get(name))
        elif name in multi_containers:
            user_container = copy.deepcopy(multi_containers.get(name))
        elif name in magic_containers:
            user_container = copy.deepcopy(magic_containers.get(name))
        elif name in magic_multi_containers:
            user_container = copy.deepcopy(magic_multi_containers.get(name))
        else:
            user_container = None

        if user_container != None:
            return user_container
        else:
            print(f'"{name}" not found. Try again.')
            return LootManager.select_container()


    def find_a_container(containers: object, weight: int) -> object:
        """
        Check if the container's capacity can store an item.

        Parameters:
        container (object): The container that will be checked.
        weight (int): the weight of the item that wants to be stored.

        Returns:
        available_container (object): A container that has enough capacity to store the item.
        """
        for container in containers:
            if isinstance(container, MagicContainer):
                if weight <= container.remaining_capacity():
                    return container

            if isinstance(container, (MultiContainer, MagicMulti)):
                available_container = LootManager.find_a_container(container.compartments, weight)
                if available_container:
                    return available_container

            if isinstance(container, Container):
                if weight <= container.remaining_capacity():
                    if LootManager.check_upper_cons_capacity(container, weight):
                        return container

            if isinstance(container, Container):
                available_container = LootManager.find_a_container(container.contents, weight)
                if available_container:
                    return available_container

        return None


    def check_upper_cons_capacity(container: object, weight: int) -> bool:
        """
        Check if the container's upper container capacity can store an item.

        Parameters:
        container (object): The container that will be checked.
        weight (int): the weight of the item that wants to be stored.

        Returns:
        bool: True if there is enough capacity to store the item's weight.
        """
        if not hasattr(container, "upper"):
            return True
        if container.upper is None:
            return True
        if isinstance(container.upper, (MagicMulti)):
            return True   
        if isinstance(container.upper, (MagicContainer)):
            if weight <= container.upper.remaining_capacity():
                return True
        elif isinstance(container.upper, MultiContainer):
            return LootManager.check_upper_cons_capacity(container.upper, weight)
        else:
            if weight <= container.upper.remaining_capacity():
                return LootManager.check_upper_cons_capacity(container.upper, weight)
            else:
                return False


    def check_has_magic_con(container: object) -> bool:
        """
        Check if the container contains a magic container

        Parameters:
        container (object): The container that will be checked.

        Returns:
        bool: True if there is a magic container inside container.
        """
        if isinstance(container, (MultiContainer, MagicMulti)):
            return True
        if len(container.contents) > 0 and hasattr(container, "contents"):
            return any(isinstance(content, (MagicContainer, MagicMulti)) for content in container.contents)
        return False


    def loot_item() -> None:
        """
        Allows the user to loot an item by name into the selected container.
        """
        name = input("Enter the name of the item: ")
        if name in items:
            temp_item = copy.deepcopy(items.get(name))
        elif name in containers:
            temp_item = copy.deepcopy(containers.get(name))
        elif name in multi_containers:
            temp_item = copy.deepcopy(multi_containers.get(name))
        elif name in magic_containers:
            temp_item = copy.deepcopy(magic_containers.get(name))
        elif name in magic_multi_containers:
            temp_item = copy.deepcopy(magic_multi_containers.get(name))
        else:
            temp_item = None
        if not temp_item:
            print(f'"{name}" not found. Try again.')
            return

        weight = temp_item.weight if not isinstance(temp_item, (MultiContainer, MagicMulti)) else temp_item.empty_weight

        # Determine whether the selected container can store an item.
        if not isinstance(user_container, (MultiContainer, MagicMulti)) and weight <= user_container.remaining_capacity():
            user_container.add_item(temp_item, user_container)
            print(f'Success! Item "{temp_item.name}" stored in container "{user_container.name}".')
            return

        # Print failed message if selected container cannot store an item.
        if not LootManager.check_has_magic_con(user_container):
            print(f'Failure! Item "{temp_item.name}" NOT stored in container "{user_container.name}".')
            return

        # Try finding another container inside the selected container
        if isinstance(user_container, (MultiContainer, MagicMulti)):
            contents = user_container.compartments 
        else:  
            contents = user_container.contents

        temp_container = LootManager.find_a_container(contents, weight)
        
        # Print success if successfully finding a suitable container to store an item.
        if temp_container:
            temp_container.add_item(temp_item, temp_container)
            print(f'Success! Item "{temp_item.name}" stored in container "{user_container.name}".')
        else:
            print(f'Failure! Item "{temp_item.name}" NOT stored in container "{user_container.name}".')


    def list_items(user_container: object) -> None:
        """
        Lists the items in the selected container.

        Parameters:
        user_container (object): The user container object
        """
        print(user_container)
        contents = user_container.compartments if isinstance(user_container, (MultiContainer, MagicMulti)) else user_container.contents
        LootManager.print_items(contents, 1)


    def print_items(items: list, store_level: int) -> None:
        """
        Prints each item stored in the selected container.

        Parameters:
        items (list): the list of items 
        store_level (int): the depth store level
        """
        indentation = "   " * store_level
        for each_item in items:
            print(f"{indentation}{each_item}")
            if isinstance(each_item, (MultiContainer, MagicMulti, Container)):
                
                if isinstance(each_item, (MultiContainer, MagicMulti)):
                    contents = each_item.compartments 
                else:
                    contents = each_item.contents

                if len(contents) > 0:
                    LootManager.print_items(contents, store_level + 1)


    def main_menu() -> None:
        """
        Displays the main menu for interacting with the program.
        """
        while True:
            print("==================================")
            print("Enter your choice:")
            print("1. Loot item.")
            print("2. List looted items.")
            print("0. Quit.")
            print("==================================")
            choice = input()
            if choice == "1":
                LootManager.loot_item()
            elif choice == "2":
                LootManager.list_items(user_container)
            elif choice == "0":
                quit()


if __name__ == "__main__":
    containers, items = {}, {}
    multi_containers = {}
    magic_containers = {}
    magic_multi_containers = {}
    user_container = None
    LootManager.initialise()
    user_container = LootManager.select_container()
    LootManager.main_menu()

        



