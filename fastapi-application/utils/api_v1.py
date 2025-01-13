from uuid import UUID


def combine_dict_with_user_uuid(data:dict, user_uuid:UUID) -> dict:
    data.update({"user_id": user_uuid})
    return data