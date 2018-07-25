from flask_jwt import JWT,jwt_required
from flask_restful import Resource,reqparse
from models.item import ItemModel


#Get items by name
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help = "Message': 'This can not be free!'"
    )
    parser.add_argument('store_id',
            type = int,
            required = True,
            help = "Message': 'store id required!'"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found!'}, 404

            
    #post,create item
    def post(self, name):
        if ItemModel.find_by_name(name):
            {'Message': 'item already exist'},400
        
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": 'error occured while trying to insert item'},500
            
        return item.json(),201

    #delete item != name
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted!'}

    #update or post
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        
        item.save_to_db()

        return item.json()
#Get all Items
class Item_list(Resource):
    def get(self): 
        return {'items': [item.json() for item in ItemModel.query.all()]}#get all the items in db