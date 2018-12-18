# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 16:17:55 2018

@author: T5_1
"""

import numpy as np
from broadbean import Element
from broadbean.atoms import sine

def create_sideband_template_element():
   
    sI = sine(duration='readout_duration', frequency='sideband_frequency', amplitude='base_sideband_amplitude', offset='sideband_I_offset',  phase=0 )
    sQ = sine(duration='readout_duration', frequency='sideband_frequency', amplitude='adjusted_sideband_amplitude', offset='sideband_Q_offset',  phase='sideband_Q_phase')
    def my_transformation(context):
        context['adjusted_sideband_amplitude'] = context['base_sideband_amplitude'] +  context['sideband_amplitude_difference']
        context['sideband_Q_phase'] = np.pi * (0.5 + context['sideband_phase_offset'] / 180)
    #The order in which the template elements are uploaded
    elem = Element({1:sI, 2:sQ},
                   transformation=my_transformation)
    return elem