A primarily Python-based, yet platform-independent, peer-to-peer system for deploying commands to a cluster of hosts using UDP and sockets.

The basic principle is that a relaying host within a network will ask an external server for commands to execute on other hosts within the network. Other hosts on the network are listening for instructions from the relay.

When the Python runs, a relay host is automatically chosen. If the relay is disconnected, a new one within the network will be chosen randomly and begin requesting commands from the external botmaster. Other hosts will then listen to the new relay for instructions.