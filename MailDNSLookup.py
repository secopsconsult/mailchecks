#!/usr/bin/env python
import dns.resolver
import optparse
import re

def emailtxtrecords(host,nameserver):
	lookup = dns.resolver.Resolver()
	if nameserver is not None:
		dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
		dns.resolver.default_resolver.nameservers = [nameserver]
		print "[+] Using nameserver: %s " % nameserver

	print "[+] TXT Records for %s" % host
	records = 0
	try:
		for txtrecord in dns.resolver.query(host,'TXT'):
			if (re.search('v=spf1',txtrecord.to_text().lower())):
				records = 1
				print "[+] --> " + txtrecord.to_text()
	except:
		records = 1
		print "[-] No Records found"

	if records == 0:
		print "[-] No Records found"

	dmarchost = "_dmarc." + host
	print "[+] TXT Records for %s" % dmarchost
	try:
		for txtrecord in dns.resolver.query(dmarchost,'TXT'):
			print "[+] --> " + txtrecord.to_text()
	except:
		print "[-] No Records found"

def main():
	parser = optparse.OptionParser('usage %prog '+ '-d <domain>')
	parser.add_option('-d', dest='domain', type='string', help='specify hostname to examine')
	parser.add_option('-s', dest='nameserver', type='string', help='specify nameserver to examine')

	(options, args) = parser.parse_args()

	host=options.domain
	nameserver=options.nameserver

	if (host == None):
		print parser.usage
		exit(1)

	print "[+] Looking up records for %s" % host
	emailtxtrecords(host,nameserver)


if __name__ == '__main__':
	main()

