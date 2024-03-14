import grpc
from concurrent import futures
from hashport import hashport
import socket
from uuid import uuid5, NAMESPACE_DNS

import market_pb2 as pb2
import market_pb2_grpc as pb2_grpc


class BuyernotifyicationServicer(pb2_grpc.BuyernotifyicationServicer):
    def __init__(self):
        pass

    def notifyyConnection(self, request, context):
        print('\nNew notifyication:\n' + str(request))
        return pb2.Response(status=True, message="notifyication received")

    def notifyyItemUpdated(self, request, context):
        print('\nNew notifyication:')
        print('Item updated notifyication:\n', str(request))
        return pb2.Response(status=True, message="notifyication received")

def ServerIsOffline():
    print(f'\nServer is Offline\n')
    exit(1)

def RegisterBuyer(stub, buyer_uuid, ip, port):
    buyerR = pb2.Buyer(uuid = buyer_uuid, notify_server_address = (ip + ':' + str(port)))
    try:
        response = stub.RegisterBuyer(buyerR)
        print(f'Response: {response.message}')
    except:
        ServerIsOffline()


def SearchItem(stub, buyer_uuid):
    print("Enter the following details: ")
    item_name = input("Enter the Item name: ")
    item_category = input("Enter the Item category: ")
    request = pb2.DisplayItemRequest(Item_name = item_name, Item_category = item_category, buyer_uuid = buyer_uuid)
    try:
        print(f'List of items: ')
        response = stub.SearchItem(request)
        cnt = 0
        for item in response:
            cnt = cnt + 1
        
        if (cnt == 0):
            print("No available item")
        else:
            for item in response:
                print(str(item))
    except:
        ServerIsOffline()


def BuyItem(stub, buyer_uuid):
    print("Enter the following details: ")
    item_id = input("Enter the item ID: ")
    item_quantity = int(input("Enter the item quantity: "))
    requestB = pb2.BuyItemRequest(buyer_uuid = buyer_uuid, Item_id = item_id, quantity = item_quantity)
    try:
        response = stub.buyItem(requestB)
        print(f'Response: {response.message}')
    except:
        ServerIsOffline()


def AddToWishList(stub, buyer_uuid):
    print("Enter the following details: ")
    item_id = input("Enter the item ID: ")
    requestA = pb2.WishListRequest(buyer_uuid = buyer_uuid, Item_id = item_id)
    try:
        response = stub.addToWishlist(requestA)
        print(f'Response: {response.message}')
    except:
        ServerIsOffline()


def Connection(server_address, buyer_uuid, ip, port):
    try:
        # Create a gRPC channel to connect to the server
        channel = grpc.insecure_channel(server_address)
        # Create a stub for the Market service
        stub = pb2_grpc.MarketStub(channel)
        stub.CheckConnection(pb2.PingRequest(message="Connection Request from Buyer"))
    except:
        ServerIsOffline()
    return stub


def RateItem(stub, buyer_uuid):
    print("Enter the following details: ")
    item_id = input("Enter the Item ID: ")
    item_rating = float(input("Enter the Item Rating: "))
    requestR = pb2.RateItemRequest(rating = item_rating, buyer_uuid = buyer_uuid, Item_id = item_id)
    try:
        response = stub.rateItem(requestR)
        print(f'Response: {response.message}')
    except:
        ServerIsOffline()


def run(server_address, buyer_uuid, ip, port):
    stub = Connection(server_address, buyer_uuid, ip, port)
    print('\nConnected to server\n')

    RegisterBuyer(stub, buyer_uuid, ip, port)

    print("Connected to server")
    print("1. Search Item")
    print("2. Buy Item")
    print("3. Add To WishList")
    print("4. Rate Item")
    print("5. To end")
    while True:
        fu = int(input("Enter function choice: "))
        if fu == 1:
            SearchItem(stub, buyer_uuid)
        elif fu == 2:
            BuyItem(stub, buyer_uuid)
        elif fu == 3:
            AddToWishList(stub, buyer_uuid)
        elif fu == 4:
            RateItem(stub, buyer_uuid)
        elif fu == 5:
            break




def MainFunction():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    username = input("Enter username: ")
    port = hashport(username)
    server_port = input("Enter market server's Port Number: ")
    server_ip = input("Enter market server's IP address: ")
    server_addr = server_ip + ':' + server_port

    print("Buyer IP Address:", ip)
    print(f'Port: {port}')

    buyer_uuid = uuid5(NAMESPACE_DNS, username).hex
    print(f'Buyer UUID: {buyer_uuid}')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_BuyernotifyicationServicer_to_server(
        BuyernotifyicationServicer(), server)
    server.add_insecure_port('[::]:'+str(port))
    server.start()
    print(f'Buyer notifyication Server started on port {port}\n')
    # server.wait_for_termination()
    run(server_address=server_addr, buyer_uuid=buyer_uuid, ip=ip, port=port)


MainFunction()