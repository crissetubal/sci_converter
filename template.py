#!/usr/bin/env python

import re

from module import Property,Module,SubModule

class Template:

    comment_pattern = re.compile(' *#.*')
    property_pattern = re.compile(' *\..+')
    submodule_pattern = re.compile(' *\*.+')
    module_pattern = re.compile(' *\*\*.+')
    value_pattern = re.compile('^ *[^\*\.#]')

    def __init__(self):
######hamiltonian
        self.levy_leblond    = Property('.LEVY-LEBLOND')
        self.urkbal          = Property('.URKBAL')
        self.lvcorr          = Property('.LVCORR')

        self.hamiltonian = Module('**HAMILTONIAN')
        self.hamiltonian.properties.update({'.LEVY-LEBLOND': self.levy_leblond})
        self.hamiltonian.properties.update({'.URKBAL': self.urkbal})
        self.hamiltonian.properties.update({'.LVCORR': self.lvcorr})
    ########dirac
        self.wave_function_prop  = Property('.WAVE FUNCTION')
        self.properties_prop     = Property('.PROPERTIES')
        self.inptest             = Property('.INPTEST')

        self.dirac = Module('**DIRAC')
        self.dirac.properties.update({'.WAVE FUNCTION'   :self.wave_function_prop})
        self.dirac.properties.update({'.PROPERTIES'      :self.properties_prop})
        self.dirac.properties.update({'.INPTEST'         :self.inptest})
    ##########wave function
        self.scf_prop    = Property('.SCF')
        self.evccnv      = Property('.EVCCNV')
        self.atomst      = Property('.ATOMST')

        self.scf = SubModule('*SCF')
        self.scf.properties.update({'.EVCCNV':self.evccnv})
        self.scf.properties.update({'.ATOMST':self.atomst})

        self.wave_function = Module('**WAVE FUNCTION')
        self.wave_function.properties.update({'.SCF':self.scf_prop})
        self.wave_function.submodules.update({'*SCF':self.scf})
    ############integrals submodule
        self.uncontract  = Property('.UNCONTRACT')
        self.readin      = SubModule('*READIN')
        self.readin.properties.update({'.UNCONTRACT':self.uncontract})

        self.screen = Property('.SCREEN')
        self.twoint      = SubModule('*TWOINT')
        self.twoint.properties.update({'.SCREEN':self.screen})

        self.integrals   = Module('**INTEGRALS')
        self.integrals.submodules.update({'*READIN':self.readin})
        self.integrals.submodules.update({'*TWOINT':self.twoint})
    ############# properties
        self.bzlao = Property('.BZLAO')
        self.bxlao = Property('.BXLAO')
        self.bylao = Property('.BYLAO')

        self.london = Property('.LONDON')
        self.doeprn = Property('.DOEPRN')
        self.intflg = Property('.INTFLG')

        self.nmr = SubModule('*NMR')
        self.nmr.properties.update({'.LONDON':self.london})
        self.nmr.properties.update({'.DOEPRN':self.doeprn})
        self.nmr.properties.update({'.INTFLG':self.intflg})

        self.prop_module  = Module('**PROPERTIES')
        self.prop_module.properties.update({'.BZLAO':self.bzlao})
        self.prop_module.properties.update({'.BXLAO':self.bxlao})
        self.prop_module.properties.update({'.BYLAO':self.bylao})
        self.prop_module.submodules.update({'*NMR':self.nmr})
    ############# visual
        self.jdia        = Property('.JDIA')
        self.j        = Property('.J')
        self.noreortho   = Property('.NOREORTHO')
        self.nodirect    = Property('.NODIRECT')
        self.two_d       = Property('.2D')
        self.two_d_int   = Property('.2D_INT')
        self.visual = Module('**VISUAL')
        self.visual.properties.update({'.JDIA'       :self.jdia})
        self.visual.properties.update({'.J'          :self.j})
        self.visual.properties.update({'.NOREORTHO'  :self.noreortho})
        self.visual.properties.update({'.NODIRECT'   :self.nodirect})
        self.visual.properties.update({'.LONDON'     :self.london})
        self.visual.properties.update({'.2D'         :self.two_d})
        self.visual.properties.update({'.2D_INT'     :self.two_d_int})

        #valid module names
        self.modules = {   '**HAMILTONIAN'       : self.hamiltonian,
                        '**DIRAC'           : self.dirac,
                        '**WAVE FUNCTION'   : self.wave_function,
                        '**INTEGRALS'       : self.integrals,
                        '**PROPERTIES'      : self.prop_module,
                        '**VISUAL'          : self.visual}
        #valid submodules names
        self.submodules = {  '*READIN'   :self.readin,
                        '*TWOINT'   :self.twoint,
                        '*SCF'      :self.scf,
                        '*NMR'      :self.nmr}
        #valid properties names
        self.properties = {  '.LEVY-LEBLOND' :self.levy_leblond,
                        '.URKBAL'       :self.urkbal,
                        '.LVCORR'       :self.lvcorr,
                        '.WAVE FUNCTION':self.wave_function_prop,
                        '.PROPERTIES'   :self.properties_prop,
                        '.INPTEST'      :self.inptest,
                        '.EVCCNV'       :self.evccnv,
                        '.ATOMST'       :self.atomst,
                        '.SCF'          :self.scf_prop,
                        '.UNCONTRACT'   :self.uncontract,
                        '.SCREEN'       :self.screen,
                        '.BZLAO'        :self.bzlao,
                        '.BXLAO'        :self.bxlao,
                        '.BYLAO'        :self.bylao,
                        '.LONDON'       :self.london,
                        '.DOEPRN'       :self.doeprn,
                        '.INTFLG'       :self.intflg,
                        '.JDIA'         :self.jdia,
                        '.J'            :self.j,
                        '.NOREORTHO'    :self.noreortho,
                        '.NODIRECT'     :self.nodirect,
                        '.2D'           :self.two_d,
                        '.2D_INT'       :self.two_d_int
                        }

    def is_module(self, name):
        return self.modules.get(name)

    def is_comment(self, line):
        m = re.match(self.comment_pattern, line)
        n = line.strip() == ''
        return m or n

    def is_property(self, line):
        return self.properties.get(line)

    def is_submodule(self, line):
        return self.submodules.get(line)

    def is_value(self, line):
        return re.match(self.value_pattern, line)
