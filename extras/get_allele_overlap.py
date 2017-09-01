#!/usr/bin/env python

''' For a population-level set of neoepitope predictions, determine how often a random subset of alleles share epitope preference
    For 1000 random sets of 6 HLA alleles (2 HLA-A, 2 HLA-B, and 2 HLA-C; heterozygous pairs), overlap data is collected
    Count the number of epitopes that bind to 1, 2, 3, 4, 5, or 6 of the alleles

    Input to the script:
    infile: Path to file containing population level set of neoepitope predictions
    outfile: Path to results file
    alleles: Path to file containing a comma separated list of HLA alleles used in prediction
'''

import random
from optparse import OptionParser
p = OptionParser(usage = "python get_allele_overlap.py -i <infile> -o <outfile> -a <allele_file>")
p.add_option("-i", action="store", dest="infile", help="Path to input file")
p.add_option("-o", action="store", dest="outfile", help="Path to output file")
p.add_option("-a", action="store", dest="alleles", help="Path to allele file")
opts, args = p.parse_args()
infile = opts.infile
outfile = opts.outfile
allele_file = opts.alleles


# Parse the allele file to obtain the sets of HLA-A, HLA-B, and HLA-C alleles
allele_fh = open(allele_file, "r")
alleles = allele_fh.readline().strip("\n").split(",")
allele_fh.close()
a_alleles = []
for allele in alleles:
	if "HLA-A" in allele:
		a_alleles.append(allele)
b_alleles = []
for allele in alleles:
	if "HLA-B" in allele:
		b_alleles.append(allele)
c_alleles = []
for allele in alleles:
	if "HLA-C" in allele:
		c_alleles.append(allele)


# Create 1000 random sets of alleles
allele_sets = []
for i in range(0,1000):
	aset = random.sample(a_alleles, 2)
	bset = random.sample(b_alleles, 2)
	cset = random.sample(c_alleles, 2)
	set = aset + bset + cset
	allele_sets.append(set)


# Parse neoepitope prediction data to get overlap data
in_fh = open(infile, "r")
out_fh = open(outfile, "w")
for group in allele_sets:
	share_data = {}
	share_counts = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0}
	in_fh.seek(0)
	for line in in_fh:
		line = line.strip("\n").split("\t")
		if line[0] != "Disease":
			allele = line[1].strip('"')
			adj_allele = "HLA-" + allele[0] + "*" + allele[1:3] + ":" + allele[3:]
			if adj_allele in group:
				epitope = line[2].strip('"')
				tumor_aff = float(line[3].strip('"'))
				normal_aff = float(line[5].strip('"'))
				if tumor_aff < 500 and normal_aff > 500 and normal_aff >= (5*tumor_aff):
					immunogenic = True
				else:
					immunogenic = False
				if epitope not in share_data and immunogenic == True:
					share_data[epitope] = [adj_allele]
				elif epitope in share_data and adj_allele not in share_data[epitope] and immunogenic == True:
					share_data[epitope].append(adj_allele)
	this_set = ",".join(group)
	for peptide in share_data:
		num_alleles = len(share_data[peptide])
		share_counts[num_alleles] += 1
	outline = this_set + "\t" + str(share_counts[1]) + "\t" + str(share_counts[2]) + "\t" + str(share_counts[3]) + "\t" + str(share_counts[4]) + "\t" + str(share_counts[5]) + "\t" + str(share_counts[6]) + "\n"
	out_fh.write(outline)
in_fh.close()
out_fh.close()
