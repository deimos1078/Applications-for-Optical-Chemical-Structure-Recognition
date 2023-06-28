import sys
import os
from rdkit import Chem

def comparemolfiles(inputdirectory, referencedirectory):
	'''This function checks if the molecules in a set of mol-files are identical to the molecules in a second set of mol-files using Standard InChI.
	(assuming the files have the same names)'''


	dirlist = os.listdir(inputdirectory)										# returns a list of filenames for the given directory

	for subset in dirlist:
		target_dir = str(inputdirectory + "/" + subset)
		with open(str(target_dir + '_results_report.txt'), 'w+') as output:		# create empty output.txt
			score = 0
			for i in range(1, 130):												# Loop over inputdirectory
				try:
					input = Chem.SDMolSupplier(str(target_dir + '/' + str(i) + ".mol"))		# read mol-file with molecule to be checked (mol)
				except:
					output.write('Not able to read molfile: ' + target_dir + '/' + str(i) + ".mol")
					continue
				input2 = Chem.SDMolSupplier(str(referencedirectory + '/' + str(i) + ".mol"))	# read reference mol-file / ADAPT ENDING ACCORDING TO FILES
				for compound in input:
					if not compound:
						inchi1 = ""
						continue
						output.write('Not able to read molfile: ' + inputdirectory+'/'+file)
					inchi1 = Chem.inchi.MolToInchi(compound)						# generate standard Inchi
					for compound in input2:
						if not compound:
							inchi2 = ""											
							continue
							output.write('Not able to read molfile: ' + referencedirectory+'/' + file)
						inchi2 = Chem.inchi.MolToInchi(compound)						# generate (canonical) SMILES
					if inchi1 == inchi2:
						print(target_dir + '/' + str(i) + ".mol" + ' contains the right structure: \n' + str(inchi1) + ' vs. \n' + str(inchi2) + '(Reference)\n')
						output.write(target_dir + '/' + str(i) + ".mol" + ' contains the right structure: \n' + str(inchi1) + '(Reference) vs. \n' + str(inchi2) + '\n')
						score +=1
					else: 
						print(target_dir + '/' + str(i) + ".mol"+ ' does not contain the right structure: \n' + str(inchi1) + ' vs. \n' + str(inchi2) + '(Reference)\n')
						output.write(target_dir + '/' + str(i) + ".mol" + ' does not contain the right structure: \n' + str(inchi1) + '(Reference) vs. \n' + str(inchi2) + '\n')
			output.write(str(score) + ' mol-files contain the right structure.')
			output.write('Resulting score: ' + str(score) + ' correct out of 129 ->' + str(score/129*100) + '%')
			print('List of standard InChI sucessfully crated and saved in ' + str(target_dir + 'results_report.txt'))
			print('Resulting score: ' + str(score) + ' correct out of 129 ->' + str(score/129*100) + '%')
	return

def main():
	if len(sys.argv) != 3:
		print("\"Usage of this function: comparemolfileswithstandardinchi.py directory-with-mol-files directory-with-reference-molfiles ")
	if len(sys.argv) == 3:
		comparemolfiles(sys.argv[1], sys.argv[2])
	sys.exit(1)

if __name__ == '__main__':
	main()