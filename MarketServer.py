import grpc
from concurrent import futures
import market_pb2 as pb2
import market_pb2_grpc as pb2_grpc
import statistics


class MarketServicer(pb2_grpc.MarketServicer):
    def __init__(self):
        self.seller_list = {}
        self.Item_list = {}
        self.buyer_list = {}
        self.wishlist_buyer = {}
        self.rating_item = {}

    def CheckConnection(self, request, context):
        print('Connection request:\n', str(request))
        print('Accepted\n')
        return pb2.Response(status=True, message="Connection successful")

    # Seller methods
    def RegisterSeller(self, request, context):
        print('Seller registration request:')
        print(str(request))
        
        if request.uuid in self.seller_list:
            print('Rejected\n')
            reqc = pb2.Response(status=False, message="Seller already registered")
            return reqc
        else:
            try:
                channel = grpc.insecure_channel(request.notify_server_address)
                stub = pb2_grpc.SellernotifyicationStub(channel)
                stub.notifyyConnection(pb2.PingRequest(message="Connected"))
            except:
                print('\nnotifyication server offline\n')
                res = pb2.Response(status=False, message="notifyication server offline")
                return res
            print("Connected to seller's notifyication server")

            self.seller_list[request.uuid] = {'notify_server_address': request.notify_server_address, 'Items': [], 'stub': stub}

            print('Accepted\n')
            req = pb2.Response(status=True, message="Seller registered successfully")
            return req


    def SellItem(self, request, context):
        print('Item sale request:\n', str(request))
        
        if request.seller_uuid not in self.seller_list:
            print('REJECTED')
            res = pb2.RegisterItemResponse(status=False, message="Seller not registered", Item_id='-1')
            return res
        else:
            item_id = '0'
            if len(self.Item_list):
                max_key = max(map(int, self.Item_list.keys()), default=0) + 1
                result = str(max_key)
                item_id = result
            self.Item_list[item_id] = request
            self.Item_list[item_id].item_id = item_id
            self.seller_list[request.seller_uuid]['Items'].append(item_id)

            print('Accepted\n')
            res = pb2.RegisterItemResponse(status=True, message="Item registered successfully", Item_id=item_id)
            return res


    def UpdateItem(self, request, context):
        print('Item update request:\n', str(request))
        
        if request.Item_id not in self.Item_list:
            print("Rejected\n")
            return pb2.Response(status=False, message="Item not found")
        else:
            if request.seller_uuid != self.Item_list[request.Item_id].seller_uuid:
                print("Rejected\n")
                res = pb2.Response(status=False, message="You are not authorized to perform this operation")
                return res
            
            else:
                rating = self.Item_list[request.Item_id].rating
                self.Item_list[request.Item_id] = request.new_Item
                self.Item_list[request.Item_id].rating = rating

                # notifyy buyers
                for buyer_uuid in self.wishlist_buyer.get(request.Item_id, []):
                    stub = self.buyer_list[buyer_uuid]['stub']
                    req = pb2.ItemUpdatednotifyication(new_Item=pb2.ItemForDisplay(rating = rating, cat = request.new_Item.cat,
                                                                            name = request.new_Item.name, price = request.new_Item.price, 
                                                                            item_id = request.new_Item.item_id, description = request.new_Item.description))
                    stub.notifyyItemUpdated(req)

                print("ACCEPTED")
                res = pb2.Response(status=True, message="Item updated successfully")
                return res 
            

    def DeleteItem(self, request, context):
        print('Item delete request:\n', str(request))
        

        if request.Item_id not in self.Item_list:
            print("Rejected\n")
            resp = pb2.Response(status=False, message="Item not found")
            return resp
        else:
            if request.seller_uuid == self.Item_list[request.Item_id].seller_uuid:
                del self.wishlist_buyer[request.Item_id]
                del self.Item_list[request.Item_id]
                del self.rating_item[request.Item_id]
                self.seller_list[request.seller_uuid]['Items'].remove(request.Item_id)

                for buyer in self.buyer_list:
                    if request.Item_id not in self.buyer_list[buyer]['wishlist']:
                        pass
                    else:
                        self.buyer_list[buyer]['wishlist'].remove(request.Item_id)

                print("ACCEPTED")
                resp = pb2.Response(status=True, message="Item deleted successfully")
                return resp 
            else:
                print("Rejected\n")
                resp = pb2.Response(status=False, message="Seller not authorized")
                return resp 



    def showItems(self, request, context):
        print('Show Item request:\n', str(request))
        
        if request.seller_uuid not in self.seller_list:
            print("REJECTED")
            return []
        else:
            print("ACCEPTED")
            for item_id in self.seller_list[request.seller_uuid]['Items']:
                yield (self.Item_list[item_id])



    # Buyer methods
    def RegisterBuyer(self, request, context):
        print('Buyer registration request:\n', str(request))
        
        if request.uuid in self.buyer_list:
            print('REJECTED')
            resp = pb2.Response(status=False, message="Buyer already registered")
            return resp
        else:
            try:
                channel = grpc.insecure_channel(request.notify_server_address)
                stub = pb2_grpc.BuyernotifyicationStub(channel)
                stub.notifyyConnection(pb2.PingRequest(message="Connected"))
            except:
                print('\nnotifyication server offline\n')
                resp = pb2.Response(status=False, message="notifyication server offline")
                return resp
            print("Connected to buyer server")
            self.buyer_list[request.uuid] = {'notify_server_address': request.notify_server_address, 'stub': stub, 'wishlist': []}

            print('ACCEPTED')
            resp = pb2.Response(status=True, message="Buyer registered successfully")
            return resp
        

    def SearchItem(self, request, context):
        print('Browse Items request:\n', str(request))

        Items = []
        if request.Item_name:
            Items = [self.Item_list[item_id]
                        for item_id in self.Item_list if request.Item_name in self.Item_list[item_id].name]
        elif request.item_category:
            Items = [self.Item_list[item_id]
                        for item_id in self.Item_list if request.item_category in self.Item_list[item_id].cat]
        else:
            Items = list(self.Item_list.values())

        print("ACCEPTED")

        for itemi in Items:
            if itemi.quantity > 0:
                resp = pb2.ItemForDisplay(item_id=itemi.item_id, name=itemi.name, price=itemi.price, cat=itemi.cat, rating=itemi.rating, description=itemi.description)
                yield resp


    def buyItem(self, request, context):
        print('Buy Item request:\n')
        print(str(request))
        
        if request.Item_id not in self.Item_list:
            print("Rejected\n")
            resp = pb2.Response(status=False, message="Item not found")
            return resp
        else:
            if request.quantity<= self.Item_list[request.Item_id].qty:
                print("ACCEPTED")
                self.Item_list[request.Item_id].quantity-= request.qty

                seller_uuid = self.Item_list[request.Item_id].seller_uuid
                stub = self.seller_list[seller_uuid]['stub']
                req = pb2.ItemBoughtnotifyication(qty=request.qty, Item_id=request.Item_id)
                stub.notifyyItemBought(req)
                resp = pb2.Response(status=True, message="Item bought successfully")
                return resp 
            else:
                resp = pb2.Response(status=False, message="Quantity insufficient")
                print("REJECTED")
                return resp
            


    def addToWishlist(self, request, context):
        print('Add to wishlist request:\n', str(request))
        
        if request.Item_id not in self.Item_list:
            resp = pb2.Response(status=False, message="Item not found")
            print("Rejected\n")
            return resp
        else:
            if not self.wishlist_buyer.get(request.Item_id, None):
                self.wishlist_buyer[request.Item_id] = []
            self.wishlist_buyer[request.Item_id].append(request.buyer_uuid)
            self.buyer_list[request.buyer_uuid]['wishlist'].append(request.Item_id)

            resp = pb2.Response(status=True, message="Item added to wishlist successfully")
            print("ACCEPTED")
            return resp


    def rateItem(self, request, context):
        print('Rate Item request: ')
        print(str(request))
        
        if request.Item_id not in self.Item_list:
            resp = pb2.Response(status=False, message="Item not found")
            print("Rejected\n")
            return resp
        else:
            if not self.rating_item.get(request.Item_id, None):
                self.rating_item[request.Item_id] = dict()
            self.rating_item[request.Item_id][request.buyer_uuid] = request.rating
            val = statistics.mean(self.rating_item[request.Item_id].values())
            self.Item_list[request.Item_id].rating = val

            print("ACCEPTED")
            print("item: ", self.rating_item[request.Item_id])
            print("Rating: ", self.Item_list[request.Item_id].rating)
            print()
            resp = pb2.Response(status=True, message="Item rated successfully")
            return resp


def MainFunction():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MarketServicer_to_server(
        MarketServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Market Server has started")
    server.wait_for_termination()


MainFunction()