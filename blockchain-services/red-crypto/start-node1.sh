geth init --datadir /red-crypto/node1 genesis.json
geth --datadir node1 --port 30306 --bootnodes enode://f3696ad0b13d5dfb03547fa4ff8392cb4e17a1adc956761ecb8a1fb8199a8f3b7807e7c13f9ba2e3b3c48c57180b152ac53748c43068940026c59dfd40fc635d@127.0.0.1:0?discport=30305 --networkid 41124321 --unlock 0x5d92B0501Dee5C6da7129C7D71C606Cd4FBd6e40 --password node1/password.txt --authrpc.port 8551 --mine --miner.etherbase 0x5d92B0501Dee5C6da7129C7D71C606Cd4FBd6e40 --http --http.port 8545 --http.addr 0.0.0.0 --http.corsdomain '*' --http.api 'web3,eth,net,debug,personal' --http.vhosts='*' --allow-insecure-unlock --miner.gasprice 0

#geth --datadir /red-crypto/node1 --port 30306 --bootnodes enode://f3696ad0b13d5dfb03547fa4ff8392cb4e17a1adc956761ecb8a1fb8199a8f3b7807e7c13f9ba2e3b3c48c57180b152ac53748c43068940026c59dfd40fc635d@127.0.0.1:0?discport=30305 --networkid 41124321 --unlock 0x5d92B0501Dee5C6da7129C7D71C606Cd4FBd6e40 --password node1/password.txt --authrpc.port 8551 --mine --miner.etherbase 0x5d92B0501Dee5C6da7129C7D71C606Cd4FBd6e40