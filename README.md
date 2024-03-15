
# Online Shopping Platform Communication

## Overview

This assignment involves using gRPC to implement an Online Shopping Platform, simulating the interaction between buyers, sellers, and a central market platform. The implementation will leverage Google Cloud VM instances for deploying the components, utilizing Protocol Buffers for data serialization, and gRPC for the communication framework.

## Learning Resources

Before starting, you should familiarize yourself with the following technologies:

- **Google Cloud**: Understanding how to create and manage Virtual Machines (VMs) and updating Firewall Rules.
- **Protocol Buffers**: Data interchange format that can be used across multiple programming languages.
- **gRPC**: Google's open-source Remote Procedure Call ([gRPC](grpc.io)) framework that uses Protocol Buffers (grpc.io).

It is recommended to implement the examples provided in the gRPC tutorial.

## Requirements

- Python 3.7 or higher.
- Familiarity with creating VMs on Google Cloud and setting VPC firewall rules for gRPC communication.
- Installation of gRPC and Protocol Buffers compiler.

## Project Structure

### Part 1: Platform Components

- **Market (Central Platform)**: Acts as the intermediary between buyers and sellers.
- **Seller (Client)**: Manages items and transactions with the Market.
- **Buyer (Client)**: Searches for and purchases items through the Market.

### Part 2: RPC Implementation

Implement RPC calls for various functionalities such as registering sellers, posting items for sale, searching for items, and purchasing items. Ensure all communications utilize Protocol Buffers.

### Additional Information

- Use Python for the implementation. Python is preferred for cross-platform compatibility.
- The assignment requires setting up notification servers for both buyers and sellers for real-time updates.
- Detailed RPC interactions and functionalities are described in the assignment document.

## Setup Instructions

Before starting with the assignment, ensure your development environment is set up correctly. Here's how you can prepare your environment for Python. If you're using C++, please refer to the gRPC documentation for similar setup instructions tailored to C++.

### Python Environment Setup

1. **Install Python 3.7+**

   Ensure Python 3.7 or higher is installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Upgrade pip**

   Make sure pip is updated to version 9.0.1 or higher:

   ```bash
   python -m pip install --upgrade pip
   ```

   If you cannot upgrade pip due to a system-owned installation, consider using a virtual environment:

   ```bash
   python -m pip install virtualenv
   virtualenv venv
   source venv/bin/activate
   python -m pip install --upgrade pip
   ```

3. **Install gRPC**

   Install the gRPC package:

   ```bash
   python -m pip install grpcio
   ```

   Optionally, to install gRPC system-wide (might require administrator/sudo privileges):

   ```bash
   sudo python -m pip install grpcio
   ```

4. **Install gRPC Tools**

   Python's gRPC tools include the protocol buffer compiler `protoc` and the plugin for generating server and client code from `.proto` service definitions. Install the gRPC tools with:

   ```bash
   python -m pip install grpcio-tools
   ```

### Download Example Code

As part of this assignment, you might need to work with example code. Here's how to obtain it:

```bash
git clone -b v1.62.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
cd grpc/examples/python/helloworld
```

### Running a gRPC Application

To test your setup, navigate to the `helloworld` example directory and run the server:

```bash
python greeter_server.py
```

In another terminal, run the client:

```bash
python greeter_client.py
```

You should see the client receiving greetings from the server, indicating that your gRPC setup is correct.

### Update the gRPC Service

As part of this assignment, you will need to modify and extend the gRPC service definitions. Refer to the gRPC documentation and tutorials for guidance on defining your services in `.proto` files and generating server and client stubs.

### License
This project is licensed under the MIT License - see the `LICENSE` file for details.
