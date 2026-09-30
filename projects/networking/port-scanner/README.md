# 🔎 Port Scanner

![Port Scanner Demo](assets/port-scanner.png)<br>
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)

A simple TCP port scanner written in Python, built as part of my cybersecurity learning journey.

This project is focused on learning the fundamentals of **Python networking, TCP connections and port scanning**.

---

## 🎯 Objectives

* Learn Python networking fundamentals (`socket` library)
* Understand how TCP connections work
* Learn how ports and services are identified
* Build a basic but functional port scanner from scratch
* Gradually improve the scanner with additional features

---

## 🚀 Features

* [x] Scan a single TCP port
* [x] Scan a range of TCP ports
* [x] Detect open vs closed ports
* [x] Handle connection timeouts gracefully
* [x] Add command-line arguments (argparse)
* [ ] Multi-threaded scanning for better performance
* [ ] Scan results logging

---

## 🛠️ Technologies

* **Python**
* **TCP/IP Protocol**
* **Socket Programming**
* **Argparse Module**

---

## 📚 What I Learned

* Python fundamentals
* Network sockets and TCP connections
* IP adresses and port management
* Error handling and timeouts
* Command-line interfaces with `argparse`
* Service identification and banner grabbin concepts

---

## ▶️ Usage

```bash
python3 port_scanner.py <target> <start_port> <end_port>
```
# Example

Scan ports `1` to `1024` on localhost:

```bash
python3 port_scanner.py 127.0.0.1 1 1024
```
You cal also scan a hostname:

```bash
python3 port_scanner.py example.com 1 1024
```
# 🧪Testing with a Local Server

To test the scanner safely, you can create a single HTTP server using Python:
```bash
python3 -m http.server 8080
```
In another terminal, run the scanner:
```bash
python3 port_scanner.py 127.0.0.1 1000 8100
```

The scanner should detect port `8080` as open:

```bash
8080 OPEN http
```

This is useful for testing because the server is running locally on your own machine, without scanning externas systems.

Press `Ctrl+C` in the server terminal to stop the HTTP server when finished.
More usage instructions will be added as the project evolves.

---

#Limitations

This is a basic TCP port scanner and currently has some limitations:

* Scanning is performed sequentially
* No multi-threading support
* Service identification is based on known port assignments
* Banner grabbing depends on the protocol being used
* UDP scanning is not supported
* Scan results cannot currently be saved to files

---
## 📜 License

This project is licensed under the MIT License.
