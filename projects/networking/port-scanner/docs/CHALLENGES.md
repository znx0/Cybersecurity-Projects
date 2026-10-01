# 🚀 Extension Challenges

The basic TCP port scanner is working. The next step is to gradually add features that make it more useful, reliable and closer to the functionality found in professional network scanning tools.

These challenges are ordered by difficulty. Start with the easier ones and build upon the previous functionality as the scanner evolves.

---

## 🟢 Easy Challenges

### Challenge 1: CSV Output

**What to build:**
Add an option to save scan results to a CSV file instead of displaying everything only in the terminal.

Example:
```bash
python3 port_scanner.py 127.0.0.1 1 1024 --output results.csv
```

**Why it's useful:**
Security teams need machine-readable output for feeding into other tools. CSV loads into Excel, imports to databases, and processes with Python/awk scripts for reporting.

**What you'll learn:**
- File I/O in Python (`open(..., 'w'`)
- Structured output formats
- Making CLI tools pipeline-friendly

**Hints:**
- Add an optional argument in `argparse`: `parser.add_argument("-o", "--output", help="Save results to a CSV file")`
- Open the file conditionally after validation and write the CSV header (`port,state,service,banner`).
- Write each open port result to both the console and the file.

**Test it works:**
```bash
python port_scanner.py scanme.nmap.org 1 1024 -o results.csv
cat results.csv
```

# Should output: port,state,service,banner followed by results

### Challenge 2: Progress Indicator

**What to build:**
Show percentage completion during scans so users know it's working and how long to wait.

**Why it's useful:**
Full TCP scans of 65535 ports take minutes. Without feedback, users think the tool hung. Progress bars reduce anxiety and support requests.

**What you'll learn:**
- Terminal control codes for overwriting lines
- Calculating completion percentage with concurrent workers
- Balancing UI updates with performance (don't update every port, batch it)

**Hints:**
- Inside your for loop, calculate percentage: percent = `COMPLETE`
- Print using sys.stdout.write(f"\r[+] Progress: {percent:.1f}%") and flush immediately with sys.stdout.flush().

**Test it works:**

```bash
python port_scanner.py 127.0.0.1 1 10000
# Should update smoothly in place: [+] Progress: 45.2%
```

### Challenge 3: Scan Multiple Hosts

**What to build:**
Accept multiple targets: `python3 port_scanner.py -i 192.168.1.1,192.168.1.2 -p 80,443`

**Why it's useful:**
Pentesting requires scanning entire subnets. Rerunning the tool 254 times for a /24 network is tedious. Batch scanning is essential.

**What you'll learn:**
- Parsing comma-separated values
- Managing multiple endpoint targets
- Coordinating async operations across different hosts

```bash
python3 port_scanner.py -i 1.1.1.1,8.8.8.8 -p 22
# Should show:
# 1.1.1.1	22 OPEN SSH ...
# 8.8.8.8	22 CLOSED SSH 
```

## Intermediate Challenges

### Challenge 4: JSON Output for Tool Integration

**What to build:**
Add an optional output flag (e.g., `-j` or `--json output.json`) to produce structured JSON output compatible with security tool chains and automation pipelines.

**Real-world application:**
CI/CD security pipelines run port scans and check results programmatically. JSON integrates seamlessly with Python security scripts, Splunk, ELK stack, or web dashboards, making your scanner suitable for automated infrastructure auditing.

**What you'll learn:**
- Data serialization using Python's built-in `json` module
- Nested data structures (dictionaries and lists) for representing scan results
- Handling optional file output flows alongside terminal output

**Implementation approach:**

1. **Add CLI Output Flag with `argparse`:**
   - Add an optional flag: `parser.add_argument("--json", help="Save results to a JSON file")`

2. **Collect Results During the Scan:**
   - Instead of only printing immediately to the terminal, append each discovered open port into a structured Python list or dictionary.

3. **Structure JSON Output:**
```json
{
  "target": "192.168.1.1",
  "scan_time": "2026-10-01T15:23:45Z",
  "ports_scanned": 1024,
  "results": [
    {"port": 22, "state": "open", "service": "ssh", "banner": "SSH-2.0-OpenSSH_..."},
    {"port": 80, "state": "open", "service": "http", "banner": "Apache/2.4.41"}
  ]
}
```

### Challenge 5: Advanced Service Version Detection

**What to build:**
Extend your existing HTTP banner-grabbing logic into a modular probe database that sends protocol-specific payloads for non-HTTP services (like FTP, SMTP, or SSH) to extract exact software versions.

**Real-world application:**
Many hardened servers disable default banners or hide versions (e.g., Apache configured with `ServerTokens Prod`). Active multi-step probing allows security auditors to query servers dynamically for accurate version and vulnerability assessment.

**What you'll learn:**
- Application layer protocols (SMTP `EHLO`, FTP `SYST`)
- Protocol-specific fingerprinting and multi-round-trip socket communication
- Designing extensible mapping structures in Python

**Implementation approach:**

1. **Create a Probe Dictionary / Database:**
   - Map standard ports or service types to specific request sequences:
     - **Port 21 (FTP):** Read initial banner, send `SYST\r\n`, and parse the operating system / server type.
     - **Port 25 (SMTP):** Read initial banner, send `EHLO scanner\r\n`, and parse supported capabilities.
     - **Port 80 (HTTP):** *(Already implemented)* Send `GET / HTTP/1.0\r\nHost: target\r\n\r\n` and parse the `Server:` header.

2. **Extend the Socket Interaction Flow:**
   - After a successful connection (`result == 0`), check if the port matches a defined protocol probe in your database.
   - Send the custom payload, read the response bytes, and decode/parse it cleanly.

**Hints:**
- Look at Nmap's `nmap-service-probes` file for inspiration on what strings specific protocols expect.
- Handle timeouts carefully (`s.settimeout()`) since multi-round-trip handshakes can take slightly longer.

**Extra credit:**
Implement version matching against a local database or CPE mapping to identify outdated, vulnerable software versions automatically.
