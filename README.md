# TeamViewHCMUS
TeamViewHCMUS is a simple TeamViewer clone project that allows remote screen sharing and control between two computers.

# How to Run the Project
To run the project, follow these steps:

1. Set Up the Environment
Make sure you have Python installed on both computers. The project requires the following Python packages, which can be installed using pip:

`pip install package1 package2 package3`
or
`pip install -r requirements.txt`

2. Start the Server
On one computer, open a terminal or command prompt and navigate to the project's directory. Then, run the following command to start the server:

`python server.py`
The server will wait for the client to connect.

3. Start the Client
On the other computer, open a terminal or command prompt and navigate to the project's directory. Then, run the following command to start the client:

`python client.py`
The client will connect to the server.

4. Establish Connection
Once the client has connected to the server, you should see a message indicating a successful connection. You can now begin screen sharing and control between the two computers.

# Features
- Remote screenshot
- Key press tracing.
- Processing handling
- Application handling

# Troubleshooting
If you encounter any issues while running the project, consider the following troubleshooting steps:

Make sure both computers are connected to each other.
Double-check that you have installed all the required packages as mentioned in the setup section.
In the server.py, change the host into your own server address (i let defaul as 127.0.0.1).
Make sure the port number in the client.py and server.py is the same.
