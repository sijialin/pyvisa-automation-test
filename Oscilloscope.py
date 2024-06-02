#!/usr/bin/env python
# coding: utf-8

# In[1]:
#This is wriiten based on Tektronix DPO4000 series Digital Oscilloscopes
import matplotlib.pyplot as plt
import pyvisa as visa
import time
import numpy as np
#from scipy.interpolate import interp1d
from typing import Literal

class Oscilloscope:
    def __init__(self,oscilloscope_path,channel_num=4):
        self.scope = visa.ResourceManager().open_resource(oscilloscope_path)
        self.scope.write("*RST")
        self.scope.encoding = 'latin_1'
        self.scope.read_termination = '\n'
        self.scope.write_termination = None
        self.channel_number=channel_num
        self.scope.timeout=10000

    def query(self, command):
        return self.scope.query(command)

    def write(self, command):
        self.scope.write(command)
        
    def read(self, command):
        return self.scope.read(command)
    
    '''
    Acquisition Command Group
    '''
    def set_acquire_mode(self,mode:Literal['SAMple', 'PEAKdetect', 'HIRes', 'AVErage', 'ENVelope']):
       self.write(f"ACQUIRE:MODE {mode}")

    def get_acquire_mode(self):
       self.write(f"ACQUIRE:MODE?")
    '''
    Horizontal Command Group
    '''
    def set_t_scale(self,new_scale):
        self.write(f'HORizontal:SCALE {new_scale}') 

    def get_t_scale(self):
        return float(self.query(f'HORizontal:SCALE?')) 

    '''
    Measurement Command Group
    '''
    def add_measurement(self,index,channel,TYPe:Literal['AMPlitude','AREa','BURst','CARea','CMEan','CRMs','DELay','DISTDUty',
                                                        'EXTINCTDB','EXTINCTPCT','EXTINCTRATIO','EYEHeight','EYEWidth','FALL',
                                                        'FREQuency','HIGH','HITs','LOW','MAXimum','MEAN','MEDian','MINImum','NCROss','NDUty',
                                                        'NOVershoot','NWIdth','PBASe','PCROss','PCTCROss','PDUty','PEAKHits','PERIod','PHAse',
                                                        'PK2Pk','PKPKJitter','PKPKNoise','POVershoot','PTOT','PWIdth','QFACtor','RISe','RMS',
                                                        'RMSJitter','PMSNoise','SIGMA1','SIGMA2','SIGMA3','SIXSigmajit','SNRatio','STDdev',
                                                        'UNDEFINED',' WAVEFORMS']
                                                        ,src2=None):
        self.write(f"SELECT: CH{channel} ON")
        time.sleep(0.05)
        self.write(f"MEASUREMENT:MEAS{index}:SOURCE1 CH{channel}")  
        self.write(f"MEASUREMENT:MEAS{index}:TYPe {TYPe}")
        self.write(f"MEASUREMENT:MEAS{index}:STATE ON")
        if src2!=None:
            self.write(f"MEASUREMENT:MEAS{index}:SOURCE2 CH{src2}")

    def get_measurement(self,index:Literal[1,2,3,4],value:Literal['MEAN','MINImum','MAXimum','STDdev','VALue']='VALUE'):
        return float(self.query(f"MEASUREMENT:MEAS{index}:{value}?"))

    def get_immed_value(self,channel:Literal[1,2,3,4],TYPe:Literal['AMPlitude','AREa','BURst','CARea','CMEan','CRMs','DELay','DISTDUty','EXTINCTDB','EXTINCTPCT',
                                          'EXTINCTRATIO','EYEHeight','EYEWidth','FALL','FREQuency','HIGH','HITs','LOW','MAXimum','MEAN',
                                          'MEDian','MINImum','PCROss','PCTCROss','PDUty','PEAKHits','PERIod','PHAse','PK2Pk','PKPKJitter',
                                          'PKPKNoise','POVershoot','PTOT','PWIdth','QFACtor','RISe','RMS','RMSJitter','PMSNoise','SIGMA1',
                                          'SIGMA2','SIGMA3','SIXSigmajit','SNRatio','STDdev',' UNDEFINED','WAVEFORMSNCROss',
                                          'NDUty','NOVershoot','NWIdth','PBASe']):
        self.write(f"MEASUrement:IMMed:TYPe {TYPe}")
        self.write(f"MEASUrement:IMMed:SOURCE CH{channel}")
        return float(self.query(f"MEASUrement:IMMed:Value?"))

    def set_measurement_source(self,meas_index,channel):
        self.write(f"MEASUrement:MEAS{meas_index}:SOURCE CH{channel}")

    '''
    Miscellaneous Command Group
    '''
    def autoset(self):
        self.write("AUTOset EXECUTE")
        
    def get_IDN(self):
        return self.query("*IDN?")    

    '''
    Trigger Command Group
    '''
    def set_trigger_a_edge_coupling(self,coupling:Literal['AC','DC','HFRej','LFRej','NOISErej']) :
        self.write(f"TRIGger:A:EDGE:COUPling {coupling}")   

    def get_trigger_a_edge_coupling(self) :
        return self.query(f"TRIGger:A:EDGE:COUPling?")  
    
    def set_trigger_a_edge_slope(self,slope:Literal['RISe','FALL']):
        self.write(f"TRIGGER:A:EDGE:SLOPE {slope}")

    def get_trigger_a_edge_slope(self):
        self.query(f"TRIGGER:A:EDGE:SLOPE?")   
    
    def set_trigger_a_edge_source(self,channel:Literal[1,2,3,4]):
        self.write(f"TRIGGER:A:EDGE:SOURCE CH{channel}")

    def get_trigger_a_edge_source(self):
        self.query("TRIGGER:A:EDGE:SOURCE?")
    '''
    Vertical Command Group
    '''
    def set_bandwidth(self,channel:Literal[1,2,3,4],mode:Literal['TWEnty','TWOfifty','FULl']):
        command = f"CH{channel}:BANDWIDTH {mode.upper()}"#{|<NR3>}
        self.write(command)

    def set_coupling(self,channel:Literal[1,2,3,4],mode):
        command = f"CH{channel}:COUPLING {mode.upper()}"
        self.write(command)

    def set_offset(self,channel,value):
        self.write(f'CH{channel}:OFFSET {value}') 

    def set_y_scale(self,channel,value):
        self.write(f'CH{channel}:SCALE {value}') 
    
    def get_y_scale(self,channel):
        return float(self.query(f'CH{channel}:SCALE?'))

    def channel_on(self,channel):
       self.write(f"SELECT:CH{channel} ON") 

    def channel_off(self,channel):
       self.write(f"SELECT:CH{channel} OFF")  

    '''
    Waveform Transfer Command Group
    '''
    def get_waveform(self,channel:Literal[1,2,3,4],plot_title=None):
        self.write(f"DATA:SOURCE CH{channel}")
        self.write("DATA:ENCdg ASCII")      
        # retrieve scaling factors
        tscale = float(self.query("WFMOUTPRE:XINcr?"))
        tstart = float(self.query('WFMOUTPRE:xzero?'))
        vscale = float(self.query('WFMOUTPRE:ymult?')) 
        voff = float(self.query('WFMOUTPRE:yzero?')) 
        vpos = float(self.query('WFMOUTPRE:yoff?')) 
        vunit=self.query("WFMOUTPRE:yunit?")
        tunit=self.query("WFMOUTPRE:xunit?")
        record = int(self.query('WFMOUTPRE:nr_pt?'))
        
        total_time=total_time = tscale * record
        tstop = tstart + total_time
        unscaled_ts=np.linspace(tstart,tstop,num=record,endpoint=False)
        
        bin_wave = self.scope.query_ascii_values('CURV?')
        unscaled_wave = np.array(bin_wave, dtype='double')  

        display_t_scale=float(self.query('HORIZONTAL:SCALE?'))
        display_t_scale,tunit,factor=self.convert_time_scale(display_t_scale)
        display_v_scale=float(self.query(f'CH{channel}:SCALE?'))
        display_v_scale,vunit,factor_v=self.convert_voltage_scale(display_v_scale)

        scaled_wave = (unscaled_wave - vpos) * vscale + voff
        time_space=unscaled_ts*factor 
        dispay_wave=scaled_wave*factor_v

        plt.figure(figsize=(10, 5))
        plt.xlim(min(time_space),max(time_space))
        plt.xticks(np.arange(min(time_space), max(time_space), display_t_scale))
        plt.ylim(-5*display_v_scale, 5*display_v_scale)
        plt.yticks(np.arange(-5*display_v_scale, 5*display_v_scale,display_v_scale))
        plt.grid(True)
        plt.plot(time_space,dispay_wave)
        plt.xlabel(tunit)
        plt.ylabel(vunit)
        if plot_title!=None:
            plt.title(plot_title)
        plt.show()
        return scaled_wave,unscaled_ts,plt.gcf()
    
    def get_waveform_data(self,channel):
        command = f"DATA:SOURCE CH{channel}"
        self.write(command)
        self.write("DATA:ENCdg ASCII")
        bin_wave = self.scope.query_ascii_values('CURV?')
        tscale = float(self.query("WFMOUTPRE:XINcr?"))
        tstart = float(self.query('WFMOUTPRE:xzero?'))
        vscale = float(self.query('WFMOUTPRE:ymult?')) 
        voff = float(self.query('WFMOUTPRE:yzero?')) 
        vpos = float(self.query('WFMOUTPRE:yoff?')) 
        record = int(self.query('WFMOUTPRE:nr_pt?'))
        
        total_time=total_time = tscale * record
        tstop = tstart + total_time
        time_space=np.linspace(tstart,tstop,num=record,endpoint=False)

        unscaled_wave = np.array(bin_wave, dtype='double')
        scaled_wave = (unscaled_wave - vpos) * vscale + voff
        return scaled_wave,time_space
    
    def get_waveform_all(self):
        active_channel_list=[]
        #Detect channel in use
        for i in range(self.channel_number):
            s=self.query(f"select:ch{i+1}?")
            if s=='1':
                active_channel_list.append(i+1)
        wave_data_list=[]
      
        for channel in active_channel_list:
            command = f"DATA:SOURCE CH{channel}"
            self.write(command)
            bin_wave = self.scope.query_ascii_values('CURV?')
            vscale = float(self.query('WFMOUTPRE:ymult?'))          
            voff = float(self.query('wfmoutpre:yzero?')) 
            vpos = float(self.query('WFMOUTPRE:yoff?')) 
            unscaled_wave = np.array(bin_wave, dtype='double')
            scaled_wave = (unscaled_wave - vpos) * vscale + voff
            display_v_scale=float(self.query(f'CH{channel}:SCALE?'))
            wave_data_list.append((channel,unscaled_wave,display_v_scale,scaled_wave))
          
        tunit=self.query("WFMOUTPRE:xunit?")
        record = int(self.query('WFMOUTPRE:nr_pt?'))
              
        tscale = float(self.query("WFMOUTPRE:XINcr?"))
        tstart = float(self.query('WFMOUTPRE:xzero?'))
        total_time = tscale * record
        tstop = tstart + total_time
        time_space=np.linspace(tstart,tstop,num=record,endpoint=False)
       
        display_t_scale=float(self.query('HORIZONTAL:SCALE?'))
        display_t_scale,tunit,factor=self.convert_time_scale(display_t_scale)     
        time_space=time_space*factor 

        plt.figure(figsize=(10, 5))
        plt.grid(True)
        for channel,bin_wave,display_v_scale,scaled_wave in wave_data_list:
            l=f"CH{channel} {display_v_scale}V/div "
            plt.plot(time_space,bin_wave,label=l)
        plt.xlabel(tunit)
        plt.yticks(range(-125, 126, 25))
        plt.tick_params(axis='y', labelleft=False)
        plt.axhline(0, color='black', linewidth=2)
        plt.legend(loc='upper left')
        plt.show()
        return wave_data_list,time_space,plt.gcf()

    '''
    Self defined commands
    '''
    def get_channel_number(self):
        return 4

    def nearest_v_scale(self,value):
        scales = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20]
        min_diff = float('inf')
        nearest_v_scale = 0.001
        for scale in scales:
            diff = value/2 - scale
            if diff >= 0 and diff < min_diff:
                min_diff = diff
                nearest_v_scale = scale
        return nearest_v_scale
    
    def nearest_t_scale(self,value):
        scales = [1, 2, 4]
        powers = [-9, -8, -7, -6, -5, -4, -3,-2,-1,0] 
        nearest_diff = float('inf')
        nearest_t_scale = None
        for scale in scales:
            for power in powers:
                scale_value = scale * 10 ** power
                diff = abs(value - scale_value)
                if diff < nearest_diff:
                    nearest_diff = diff
                    nearest_t_scale = scale_value
        return nearest_t_scale
    
    def auto_range_vertical(self,channel:Literal[1,2,3,4],reference:Literal['MEAN','PK2PK']='MEAN'):
        time.sleep(0.2)
        new_v_scale=self.nearest_v_scale( self.get_immed_value(channel,reference)/2 if reference=='PK2PK' else self.get_immed_value(channel,reference))  
        v=self.get_immed_value(channel,reference)
        current_v_scale=self.get_y_scale(channel)
        while (current_v_scale!=new_v_scale):
            self.set_y_scale(channel,new_v_scale)
            time.sleep(0.2)
            current_v_scale=new_v_scale
            new_v_scale=self.nearest_v_scale(self.get_immed_value(channel,reference)/2 if reference=='PK2PK' else self.get_immed_value(channel,reference)) 
            v=self.get_immed_value(channel,reference)
        
    def auto_range_horizontal(self,channel):
        new_t_scale=self.nearest_t_scale( 1/self.get_frequency(channel))  
        current_t_scale=self.get_t_scale()
        while (current_t_scale!=new_t_scale):
            self.set_t_scale(new_t_scale)
            time.sleep(0.1)
            current_t_scale=new_t_scale
            new_t_scale=self.nearest_t_scale(1/self.get_frequency(channel))

    def get_frequency(self,channel,fft=False,fig=False):
        math=fft
        if not fft:
            fre=[]
            for i in range(3):   
                self.write(f"MEASUrement:IMMed:SOURCE CH{channel}")
                self.write(f"MEASUrement:IMMed:TYPE FREQUENCY")
                fre.append(float(self.query("MEASUrement:IMMed:VALUE?")))
                median_freq = np.median(fre)
            max_diff = 0.2 * median_freq  
            if max(max(fre) - median_freq, median_freq - min(fre)) > max_diff:
                math = True
            else:
                return np.average(fre)
        
        if math:
            wave,t=self.get_waveform_data(channel)
            tscale = float(self.query("WFMoutpre:XINcr?"))        
            record = int(self.query('WFMoutpre:nr_pt?'))                     
            total_time = tscale * record          
            time_space=np.linspace(0,total_time,num=record,endpoint=False)               
            # fft
            fft_result = np.fft.fft(wave)
            freqs = np.fft.fftfreq(len(wave), tscale)
            fft_result[0]=0        
            num=3
            peaks = []
            sorted_indices = np.argsort(fft_result)[::-1]  
            for index in sorted_indices[:num]:
                peaks.append((freqs[index], fft_result[index]))
            main_freq = abs(min([freq for freq, _ in peaks]))
            if fig:
                for i, (freq, amp) in enumerate(peaks):
                    print(f"peak {i+1} freq {freq} Hz")
                # draw spectrum
                plt.figure(figsize=(10, 5))
                plt.plot(freqs[:len(freqs)//2], np.abs(fft_result)[:len(freqs)//2])
                plt.xlabel('Frequency (Hz)')
                plt.ylabel('Magnitude')
                plt.title('Frequency Spectrum ')
                plt.xscale('log')  
                plt.yscale('log')  
                plt.xlim(0, main_freq*1000)  
                plt.grid(True)
                plt.show()
            return abs(main_freq) 

    def convert_time_scale(self,scale):
        if  scale >= 1e-2:
            return scale, 's',1
        elif scale >= 1e-5:
            return scale * 1e3, 'ms',1e3
        elif scale >= 1e-8:
            return scale * 1e6, 'us',1e6
        else:
            return scale*1e9, 'ns',1e9
        
    def convert_voltage_scale(self,scale):
        if  scale >= 1e-2:
            return scale, 'V',1
        elif scale >= 1e-5:
            return scale * 1e3, 'mV',1e3
        else:
            return scale * 1e6, 'uV',1e6
        
    def conver_freq_scale(self,freq):
        if freq>1E6:
            return freq/1000000.00,'MHz'
        elif freq>1E3:
            return freq/1000.00,'KHz'
        else:
            return freq,"Hz"
    
    def measure_ripple(self,channel,window_size=None):
        if window_size==None:
            window_size = int(200/len(str(int(self.get_frequency(3,False)))))
        bin_wave,t=self.get_waveform_data(channel)
        smooth_bin_wave = np.convolve(bin_wave, np.ones(window_size)/window_size, mode='same')
        smooth_max = np.max(smooth_bin_wave)
        smooth_min = np.min(smooth_bin_wave)
        vpp = smooth_max - smooth_min
        print(f"Vpp：{vpp:.2f}V")     

        plt.figure(figsize=(10, 5))
        plt.plot(t, bin_wave, label='Original Signal')
        plt.plot(t, smooth_bin_wave, label='Filtered Signal')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Original vs Smoothed Signal')
        plt.legend()
        plt.grid(True)
              
        plt.hlines([smooth_max, smooth_min], t[0], t[-1], colors='r', linestyles='dashed')
        plt.annotate(f'{smooth_max:.4f}V', (t[len(t)//2], smooth_max), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='r')
        plt.annotate(f'{smooth_min:.4f}V', (t[len(t)//2], smooth_min), textcoords="offset points", xytext=(0,0), ha='center', fontsize=8, color='r')
        plt.show()
        return vpp
    # %%
       