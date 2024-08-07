from fastapi import HTTPException
from src.service.impl.content_service import filter_by_content_type
from src.db.database import getDB, saveDB

class WatchListService:
    @staticmethod
    def add_to_category_list(username: str, category_id: str, content_id: str, content_type: str):
        db = getDB()
        user_ind = next((u for u, user in enumerate(db["user"]) if user["username"] == username), -1)

        contents = filter_by_content_type(db["contents"], content_type)
        for content in contents:
            if content["id"] == content_id:
                if content not in db["user"][user_ind][category_id]:
                    db["user"][user_ind][category_id].append(content)
                    saveDB(db)
                else:
                    raise HTTPException(status_code=422, detail="This movie is already in the category")
                return content
        
        raise HTTPException(status_code=404, detail="No movie with this ID found in the database")
    
    @staticmethod
    def add_to_category_list_by_title(username: str, category_id: str, title: str, content_type: str):
        db = getDB()
        user_ind = next((u for u, user in enumerate(db["user"]) if user["username"] == username), -1)
        
        contents = filter_by_content_type(db["contents"], content_type)
        for content in contents:
            if content["title"] == title:
                if content not in db["user"][user_ind][category_id]:
                    db["user"][user_ind][category_id].append(content)
                    saveDB(db)
                else:
                    raise HTTPException(status_code=422, detail="This movie is already in the category")
                return content
        
        raise HTTPException(status_code=404, detail="No movie with this ID found in the database")

    @staticmethod
    def get_category_list(username: str, category_id: str):
        db = getDB()
        user_ind = next((u for u, user in enumerate(db["user"]) if user["username"] == username), -1)

        return db["user"][user_ind][category_id]

    @staticmethod
    def get_categories_list(username: str):
        db = getDB()

        user_ind = next((u for u, user in enumerate(db["user"]) if user["username"] == username), -1)
        categories_list = {}

        category_list = db["user"][user_ind]["assistidos"]
        for i in range(len(db["user"][user_ind]["assistidos"])):
            categories_list[category_list[i]["id"]] = "assistidos"
        
        category_list = db["user"][user_ind]["quero_assistir"]
        for i in range(len(db["user"][user_ind]["quero_assistir"])):
            categories_list[category_list[i]["id"]] = "quero_assistir"
        
        category_list = db["user"][user_ind]["abandonados"]
        for i in range(len(db["user"][user_ind]["abandonados"])):
            categories_list[category_list[i]["id"]] = "abandonados"
        
        return categories_list
    
    @staticmethod
    def delete_of_category_list(username: str, category_id: str, content_id: str):
        db = getDB()
        user_ind = next((u for u, user in enumerate(db["user"]) if user["username"] == username), -1)

        for i in range(len(db["user"][user_ind][category_id])):
            if db["user"][user_ind][category_id][i]["id"] == content_id:
                deleted_content = db["user"][user_ind][category_id].pop(i)
                saveDB(db)
                return deleted_content

        raise HTTPException(status_code=404, detail="No movie with this ID found in this category")

    @staticmethod
    def delete_of_category_list_by_title(username: str, category_id: str, title: str):
        db = getDB()
        user_ind = next((u for u, user in enumerate(db["user"]) if user["username"] == username), -1)

        for i in range(len(db["user"][user_ind][category_id])):
            if db["user"][user_ind][category_id][i]["title"] == title:
                deleted_content = db["user"][user_ind][category_id].pop(i)
                saveDB(db)
                return deleted_content
                break

        raise HTTPException(status_code=404, detail="No movie with this ID found in this category")
