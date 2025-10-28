import db as db

MODIFYUSERS = ['Manager']

def _ConnectWithConnector():
    #TODO: implement
    pass


def AddResource(user_position: str, resource) -> int:
    """
    Adds a resource to the database.
    Args:
        user_position (str): the user's position
        resource (dict): the resource to add
    Returns:
        int: the status code
    """
    #TODO: implement
    if user_position not in MODIFYUSERS:
        return 403
    
    # if location_id exists, check if employee_id is null
    if resource['location_id'] is null:
        if resource['employee_id'] is not null:
            # inserts resource_id, type_id, employee_id, notes, is_Decommissioned
            db.execute_query(f"INSERT INTO resources (resource_id, type_id, \
                             employee_id, notes, is_Decommissioned) \
                             VALUES ({resource['resource_id']}, 
                             {resource['type_id']}, 
                             {resource['employee_id']}, 
                             {resource['notes']}, 
                             {0})")
        else:
            # returns for invalid data
            return 400
    elif: resource['employee_id'] not null:

    # resource_id, type_id, location_id, employee_id, notes, is_Decommissioned

    return 200


def DeleteResource(user_position: str, resource: int) -> int:
    """
    Deletes the resource from the database.
    Args:
        user_position (str): the user's position
        resource (int): the resource to delete
    Returns:
        int: the status code
    """
    #TODO: implement
    pass


def UpdateResource(user_position: str, resource) -> int:
    """
    Updates the resource in the database.
    Args:
        user_position (str): the user's position
        resource (dict): the resource to update
    Returns:
        int: the status code
    """

    #TODO: implement
    pass


def GetResources() -> tuple[int, list]:
    """
    Gets the resources from the database.
    Args:
        None

    Returns:
        int: the status code
        list: the resources
    """
    #TODO: implement
    pass


def GetResourceTypes() -> tuple[int, list]:
    """
    Gets the resource types from the database.
    Args:
        None

    Returns:
        int: the status code
        list: the resource types
    """
    #TODO: implement
