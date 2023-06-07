# P2P-trading
A peer-to-peer energy trading platform implementation using private Ethereum network configuration in Raspberry Pi’s and smart contracts. 
Platform allows energy users to trade energy between neighbors or within a microgrid. Consumers/prosumers have options to add energy offers, choose offers, pay for the offer, and perform trading. 3 nodes are configured in 3 Raspberry Pi 4 models.	

Steps:
Private network implementation (Node 1 in Raspberry Pi):
1)	Install Geth 
2)	Create node 1 directory. (mkdir node1)
3)	Create genesis file and accounts. 
4)	Initialize the genesis file. (geth init –datadir node1 genesis.json)
5)	Run the private network using Geth command (geth --datadir node1 --networkid 1234 --http --allow-insecure-unlock --nodiscover --port 30303 --http.port 8545).
6)	Open the geth console in another terminal (geth attach node1/geth.ipc)
For detailed commands follow (https://geth.ethereum.org/docs/fundamentals/private-network) .
Repeat the steps for node 2 and 3 in other Raspberry Pi. 
Note: The genesis file, network Id, http port should be same in all 3 nodes. 

To add the nodes as peers to each other:
1)	Find enodeID of each node using command – admin.nodeInfo (in geth console terminal of node1)
2)	Copy the enodeID
3)	Add node to the other nodes (in node2 terminal – admin.addPeer(“enodeID”))
4)	Repeat for other nodes.
5)	Check the peer count in all terminals (net.peerCount) – Should be 2 for all the nodes
Now the private network is formed.

Smart contract development and deployment:
Smart contract is written in solidity, compiled, and tested using Remix initially. 
To deploy to the private network, we used Brownie – python based smart contract deployment tool.
1.	Install brownie (https://eth-brownie.readthedocs.io/en/stable/)
2.	To add live network: brownie networks add live private host=http://127.0.0.1:8545 chainid=1234
3.	To add accounts: brownie accounts load account_name (you will be prompted for private key and password)
4.	Compile the scripts – brownie compile
5.	Create a deployment script to deploy the smart contract and call funtions
6.	To run the deployment script in development network (already existing ganache network and accounts): brownie run scripts/script_name.py 
This will create a development environment with 10 test accounts, where we can deploy and test our smart contract working.
7.	To run the deployment script in private network: brownie run scripts/script_name.py –network private
This will connect to the developed private network and accounts and opens the web interaction application for trading where we can deploy contract, add offers, choose offers, pay, start transfer and so on. 

Interaction platform development
	Interaction platform is developed using python flask and http programming. 
Web pages are written and coded which is called from the deployment script. All the scripts are added in the templates folder. 
