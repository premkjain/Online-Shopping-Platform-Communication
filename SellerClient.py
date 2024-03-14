import grpc
from concurrent import futures
from hashport import hashport
import socket
from uuid import uuid5, NAMESPACE_DNS
import market_pb2_grpc as market_pb2_grpc
import market_pb2 as pb2


class SellernotifyicationServicer(market_pb2_grpc.SellernotifyicationServicer):
    def __init__(self):
        pass

    def notifyyConnection(self, request, context):
        print('\nNew notifyication:\n' + str(request))
        return pb2.Response(status=True, message="notifyication received")

    def notifyyItemBought(self, request, context):
        print('\nNew notifyication:')
        print('Item bought notifyication:\n', str(request))
        return pb2.Response(status=True, message="notifyication received")

def ServerIsOffline():
    print(f'\nServer is Offline\n')
    exit(1)


def connect(server_address, seller_uuid, ip, port):
    try:
        channel = grpc.insecure_channel(server_address)
        stub = market_pb2_grpc.MarketStub(channel)
        stub.CheckConnection(pb2.PingRequest(message="Connection Request from Seller"))
    except:
        ServerIsOffline()
    return stub


def RegisterSeller(stub, seller_uuid, ip, port):
    seller = pb2.Seller(uuid=seller_uuid, notify_server_address=ip+':'+str(port))
    try:
        response = stub.RegisterSeller(seller)
        print(f'Response: {response.message}')
    except:
        ServerIsOffline()


def SellItem(stub, seller_uuid):
    print("Enter the following details: ")
    item_name = str(input("Enter the name of the item: "))
    item_price = int(input("Enter the price of the item: "))
    item_quantity = int(input("Enter the quantity of the item: "))
    item_category = str(input("Enter the category of the item: "))
    item_description = str(input("Enter the description of the item: "))
    new_item = pb2.Item(item_id = '-1', seller_uuid = seller_uuid, name = item_name, price = item_price, category = item_category, 
                    quantity = item_quantity, rating = 0.0, description = item_description)
    
    try:
        response = stub.SellItem(new_item)
        print(f'Response: {response.message}')
        if(response.status == True):
            print(f'Assigned Item ID = {response.Item_id}')
    except:
        ServerIsOffline()


def UpdateItem(stub, seller_uuid):
    print("Enter the following details: ")
    item_id = input("Enter the item ID: ")
    item_name = input("Enter the new item name: ")
    item_price = int(input("Enter the new price of the item: "))
    item_quantity = int(input("Enter the new quantity of the item: "))
    item_category = str(input("Enter the new category of the item: "))
    item_description = str(input("Enter the new description of the item: "))
    new_item = pb2.Item(item_id = item_id, seller_uuid = seller_uuid, name = item_name, price = item_price, category = item_category, 
                               quantity = item_quantity, rating = 0.0, description = item_description)
    updateRequest = pb2.UpdateItemRequest(Item_id = item_id, new_Item = new_item, seller_uuid = seller_uuid)
    try:
        response = stub.UpdateItem(updateRequest)
        print(f'Response: {response.message}')
    except:
        ServerIsOffline()


def DeleteItem(stub, seller_uuid):
    print("Enter the following details: ")
    item_id = input("Enter the item ID: ")
    delRequest = pb2.DeleteItemRequest(Item_id = item_id, seller_uuid = seller_uuid)
    try:
        response = stub.DeleteItem(delRequest)
        print(f'\nResponse: {response.message}\n')
    except:
        ServerIsOffline()


def ShowItems(stub, seller_uuid):
    showRequest = pb2.ShowItemRequest(seller_uuid = seller_uuid)
    print("\nAll the Items of this seller are as follows: ")
    response = stub.showItems(showRequest)
    try:
        for item in response:
            print(str(item))
    except:
        ServerIsOffline()


def run(server_address, seller_uuid, ip, port):
    print(seller_uuid)
    stub = connect(server_address, seller_uuid, ip, port)
    print('\nConnected to server\n')

    RegisterSeller(stub, seller_uuid, ip, port)

    print("1. Sell Item")
    print("2. Update Item")
    print("3. Delete Item")
    print("4. Display Seller Items")
    print("5. To end")
    while True:
        fu = int(input("Enter function choice: "))
        if fu == 1:
            SellItem(stub, seller_uuid)
        elif fu == 2:
            UpdateItem(stub, seller_uuid)
        elif fu == 3:
            DeleteItem(stub, seller_uuid)
        elif fu == 4:
            ShowItems(stub, seller_uuid)
        else:
            break



    

def mainFunc():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print("Seller IP Address:", ip)
    server_ip = input("Enter market server's IP address: ")
    server_port = input("Enter market server's Port Number: ")
    server_address = server_ip + ':' + server_port

    username = input("Enter username: ")
    port = hashport(username)
    print(f'Port: {port}')

    seller_uuid = uuid5(NAMESPACE_DNS, username).hex
    print(f'Seller UUID: {seller_uuid}')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_SellernotifyicationServicer_to_server(
        SellernotifyicationServicer(), server)
    server.add_insecure_port('[::]:'+str(port))
    server.start()
    print(f'Seller notifyication server started on port {port}\n')
    # server.wait_for_termination()
    run(server_address=server_address, seller_uuid=seller_uuid, ip=ip, port=port)



mainFunc()