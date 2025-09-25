import sys
import dns.message
import dns.query
import dns.rdatatype

if len(sys.argv) > 2:
    host = sys.argv[1]
    query = sys.argv[2].upper()
else:
    print("Please provide a host name and query type.")
    sys.exit(1)

qtype_map = {"A": dns.rdatatype.A, "AAAA": dns.rdatatype.AAAA, "CNAME": dns.rdatatype.CNAME}
if query not in qtype_map:
    print("Unsupported query type. Use A, AAAA, or CNAME.")
    sys.exit(1)

print("Preparing DNS query..")
q = dns.message.make_query(host, qtype_map[query])

print("Contacting DNS server..")
try:
    response = dns.query.udp(q, "8.8.8.8", timeout=2)
    print("DNS response received.")
    print("Processing DNS response..")
except Exception as e:
    print(f"Query failed: {e}")
    sys.exit(1)


print(f"header.ID = {response.id}")
print(f"header.QR = {int(response.flags & dns.flags.QR > 0)}")
print(f"header.OPCODE = {response.opcode()}")
print(f"header.AA = {int(response.flags & dns.flags.AA > 0)}")
print(f"header.TC = {int(response.flags & dns.flags.TC > 0)}")
print(f"header.RD = {int(response.flags & dns.flags.RD > 0)}")
print(f"header.RA = {int(response.flags & dns.flags.RA > 0)}")
print(f"header.Z = {(response.flags >> 4) & 0x7}")
print(f"header.RCODE = {response.rcode()}")
print(f"header.QDCOUNT = {len(response.question)}")
print(f"header.ANCOUNT = {len(response.answer)}")
print(f"header.NSCOUNT = {len(response.authority)}")
print(f"header.ARCOUNT = {len(response.additional)}")

for q in response.question:
    print(f"question.QNAME = {q.name}")
    print(f"question.QTYPE = {q.rdtype}")
    print(f"question.QCLASS = {q.rdclass}")

if response.answer:
    rrset = response.answer[0]
    for rr in rrset:
        print(f"answer.NAME = {rrset.name}")
        print(f"answer.TYPE = {rr.rdtype}")
        print(f"answer.CLASS = {rr.rdclass}")
        print(f"answer.TTL = {rrset.ttl}")
        print(f"answer.RDATA = {rr.to_text()}")
else:
    print("No answers in response.")
