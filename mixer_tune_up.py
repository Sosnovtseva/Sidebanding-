from pulse_building.simple_sideband_readout_template import create_sideband_template_element
from qdev_wrappers.customised_instruments.spectrum_analyser_add_on import SpectrumAnalyserSidebandingHelper
from analysis_scripts.optimisation_basic import do_optimisation_sweep

#%% Imitialising what you need for the functions, here you can also change important parameters

fc = 5e9 #carrier frequency
band_freq = 20e6 #Sidebanding frequency
small_span= 0.25e6
plot_span= 100e6

cavity.frequency(fc)
cavity.print_readable_snapshot(update=True) #Gives snapshot of all parameters
ps.awg.awg.ch1_offset(0)
ps.awg.awg.ch2_offset(0)

spectrum_analyser_helper = SpectrumAnalyserSidebandingHelper(sh, fc, band_freq)

ideal_settings = {'sideband_amplitude_difference': 0,
                  'sideband_phase_offset': 0, 
                  'sideband_I_offset': 0,
                  'sideband_Q_offset': 0,
                  'cavity_power': -20,
                  'awg_ch_amp': 0.4}

default_context = {'readout_duration': 1e-6,
                   'base_sideband_amplitude': 0.5,
                   'sideband_frequency': band_freq,
                   **ideal_settings}
#%%

n_phases = 20
n_amps = 10
n_offs = 10
n_cav_pows = 5
n_awg_amps = 10

phases = np.linspace(-20, 20, n_phases)
amps = np.linspace(-0.2, 0.2, n_amps)
offs = np.linspace(-0.3, 0.3, n_offs)
cavity_powers = np.linspace(-25, -15, n_cav_pows)
awg_amps = np.linspace(0.1, 0.5, n_awg_amps)

phase_setpoints = ('sideband_phase_offset', phases)
amplitude_setpoints = ('sideband_amplitude_difference', amps)
I_offset_setpoints = ('sideband_I_offset', offs)
Q_offset_setpoints = ('sideband_Q_offset', offs)


#%% All settings to ideal

sideband_template_element = create_sideband_template_element()
updated_context = new_dict = {**default_context, **ideal_settings}

ps.set_template(sideband_template_element,
                inner_setpoints = ('sideband_amplitude_difference', [ideal_settings['sideband_amplitude_difference']]),
                context=updated_context)

ps.repeat_mode('element')

ps.awg.awg.ch1_amp(ideal_settings['awg_ch_amp'])
ps.awg.awg.ch2_amp(ideal_settings['awg_ch_amp'])
cavity.power(ideal_settings['cavity_power'])

#%% Full scan settings
sh.avg(4)
sh.frequency(fc)
sh.span(plot_span)
sh.configure()

#%% Take a full scan

do0d(sh.trace)

#%% awg parameter optimisation sweep
sweep_setpoints = phase_setpoints
cost_parameter = spectrum_analyser_helper.upper_lower_sideband_difference

updated_context = new_dict = {**default_context, **ideal_settings}

ps.set_template(sideband_template_element,
                inner_setpoints = sweep_setpoints,
                context=updated_context)
sh.span(small_span)
sh.configure()

parameter_to_sweep = getattr(ps.repeat, sweep_setpoints[0])

do_optimisation_sweep(parameter_to_sweep, sweep_setpoints[1], ideal_settings, cost_parameter)


#%% non awg parameter sweep

# TODO, dumb version below

do1d(cavity.power, cavity_powers[0], cavity_powers[-1], n_cav_pows, 5, sh.trace)

#%%

ideal_settings['cavity_power'] = #TODO

#%%
sh.avg(4)
sh.frequency(fc)
sh.span(plot_span)
sh.configure()


do1d(cavity.power, cavity_powers[0], cavity_powers[-1], n_cav_pows, sh.trace)

#%%

ideal_settings['cavity_power'] = #TODO
#%%
print(ideal_settings)
        

    
