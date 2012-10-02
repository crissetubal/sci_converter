#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        job
# Purpose:  Creates a Dirac job script based on data that comes from the mol.mol
# file
#
# Author:      ezequiel
#
# Created:     29/09/2012
# Copyright:   (c) ezequiel 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

class Job():
    def __init__(self, scf_file_name, mol_file_name, output_files, molecule):
        self.scf_file_name      = scf_file_name
        self.mol_file_name      = mol_file_name
        self.london_file_name   = output_files[0].name
        self.j_dia_file         = output_files[1].name
        self.j_para_file        = output_files[2].name
        self.j_total_file       = output_files[3].name
        self.int_dia_file       = output_files[4].name
        self.int_para_file      = output_files[5].name
        self.int_total_file     = output_files[6].name
        self.molecule           = molecule

    def write_job(self):
#print the #atomic start
        printable = '\n#atomic start\n\n'
        for atom in self.molecule.atoms:
            printable += 'pam --mpi=8 --global-scratch-disk --noarch --mb=1200'
            printable += ' --inp=' + atom.symbol.lower() + '.inp'
            printable += ' --mol=' + atom.symbol.lower() + '.mol'
            printable += ' --get="DFACMO"'
            printable += '\n'
            symbol = (atom.symbol + '_') if len(atom.symbol) < 2 else atom.symbol
            printable += 'cp DFACMO ' +  symbol  + 'COEF'
            printable += '\n'
        printable += '\n'#end the previous section
#print the #scf
        printable += '\n#scf\n\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.scf_file_name
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'cp DFCOEF DFCOEF_scf'
        printable += '\n'
        printable += 'cp PAMXVC PAMXVC_scf'
        printable += '\n'
#print the #london
        printable += '\n#london\n\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200 --incmo'
        printable += ' --inp=' + self.london_file_name
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'cp DFCOEF DFCOEF_l'
        printable += '\n'
        printable += 'cp PAMXVC PAMXVC_l'
        printable += '\n'
        printable += 'cp TBMO TBMO_l'
        printable += '\n'
#print the #currents
        printable += '\n#currents\n\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.j_dia_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="plot.2d.vector"'
        printable += ' --put="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'cp plot.2d.vector plot.2d.vector.dia'
        printable += '\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.j_para_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="plot.2d.vector"'
        printable += ' --put="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'cp plot.2d.vector plot.2d.vector.para'
        printable += '\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.j_total_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="plot.2d.vector" --put="DFCOEF PAMXVC TBMO"'
        printable += 'cp plot.2d.vector plot.2d.vector.total'
        printable += '\n'
#print the #integration
        printable += '\n#integration\n\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.int_total_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --put="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.int_para_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --put="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.int_dia_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --put="DFCOEF PAMXVC TBMO"'
        return printable
