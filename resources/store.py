from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import JWT,jwt_required

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": 'store was not found'},404
        
    @classmethod
    def post(cls, name):
        if StoreModel.find_by_name(name):
            return {'message': 'store already exist'}
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": 'error occured while trying to insert store'},500
        return store.json(),201


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'store deleted!'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]} #get everything in the store.