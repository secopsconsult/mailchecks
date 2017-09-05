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
				if (re.search('-all',txtrecord.to_text().lower())):
					print "\033[92m[+] --> " + txtrecord.to_text() + "\033[0m"
				else:
					print "\033[93m[+] --> " + txtrecord.to_text() + "\033[0m"

	except:
		records = 1
		print "\033[91m[-] No Records found\033[0m"

	if records == 0:
		print "\033[91m[-] No Records found\033[0m"

	dmarchost = "_dmarc." + host
	print "[+] TXT Records for %s" % dmarchost
	try:
		for txtrecord in dns.resolver.query(dmarchost,'TXT'):
			if (re.search('p=none',txtrecord.to_text().lower())):
				print "\033[93m[+] --> " + txtrecord.to_text() + "\033[0m"
			else:
				print "\033[92m[+] --> " + txtrecord.to_text() + "\033[0m"
	except:
		print "\033[91m[-] No Records found\033[0m"

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

