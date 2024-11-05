# Base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    software-properties-common

# Install Golang
RUN wget https://go.dev/dl/go1.21.1.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.21.1.linux-amd64.tar.gz && \
    rm go1.21.1.linux-amd64.tar.gz

# Set Go environment variables
ENV PATH=$PATH:/usr/local/go/bin
ENV GOPATH=/go
ENV PATH=$PATH:$GOPATH/bin

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Clone the Go Ethereum repository and checkout the specific commit
RUN git clone https://github.com/ethereum/go-ethereum.git && \
    cd go-ethereum && \
    git checkout 2bd6bd01

# Build Geth
RUN cd go-ethereum && \
    make geth

# Build bootnode and place it in /go-ethereum/build/bin
RUN cd go-ethereum/cmd/bootnode && \
    go build -o /go-ethereum/build/bin/bootnode

# Create the directory for red-crypto
RUN mkdir /red-crypto

# Copy the entire contents of the current directory into /red-crypto in the container
COPY . /red-crypto/

# Make the scripts executable
RUN chmod +x /red-crypto/start-bootnode.sh
RUN chmod +x /red-crypto/start-node1.sh
RUN chmod +x /red-crypto/start-node2.sh

# Set environment variables
ENV PATH=$PATH:/go-ethereum/build/bin

# Set the working directory to /red-crypto
WORKDIR /red-crypto

# Default command to run bootnode
#CMD ["/bin/bash", "/red-crypto/start-bootnode.sh"]