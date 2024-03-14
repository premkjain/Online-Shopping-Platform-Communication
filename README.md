# Online-Shopping-Platform-Communication
The shopping platform will have the following components/nodes:
  Market (Central Platform): The Market serves as the central platform that connects sellers and buyers. Buyers and sellers don’t communicate with each other directly.
  Seller: The Seller is a client interacting with the Central Platform to manage their items and transactions.
  Buyer: The Buyer is another client interacting with the Central Platform to search for and purchase items.
  
All these nodes will reside on different virtual machine instances (at Google Cloud) and can communicate with each other through their external IP addresses.
