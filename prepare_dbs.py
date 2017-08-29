#!/usr/bin/env python


import argparse
import subprocess


def makeBlastpDB(makeblastdb, fasta, outputdir, title):
	''' Produces a blast protein database from a fasta file
		
		makeblastdb: path to makeblastdb executable
		fasta: peptide fasta file
		outputdir: directory to which database will be written
		title: name of database
		
		No return value
	'''
	subprocess.call([makeblastdb, "-in", fasta, "-input_type", "fasta", "-dbtype", "prot", 
					"-title", outputdir+"/"+title, "-out", outputdir+"/"+title])
					

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--blastp', type=str, required=True,
            help='path to blastp executable'
        )
    parser.add_argument('-d', '--dbdir', type=str, required=True,
            help='path to output directory'
        )
    parser.add_argument('-h', '--humanFasta', type=str, required=True,
            help='path to human peptide fasta file from Ensembl'
        )
    parser.add_argument('-b', '--bacterialFasta', type=str, required=True,
            help='path to combined bacterial peptide fasta file derived from RefSeq release'
        )
    parser.add_argument('-v', '--viralFasta', type=str, required=True,
            help='path to combined viral peptide fasta file derived from RefSeq release'
        )
    args = parser.parse_args()
    
    # Create human, bacterial, and viral blast databases	
    makeBlastpDB(args.blastp, args.humanFasta, args.dbdir, "humanPepDB")
    makeBlastpDB(args.blastp, args.bacterialFasta, args.dbdir, "bacterialPepDB")
    makeBlastpDB(args.blastp, args.viralFasta, args.dbdir, "viralPepDB")