import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import constants as co
# Feedback: When you want to use classes from external modules
# it is better to import the entire module.
# For example: import astropy
# Then use astropy.cosmology.LambdaCDM
# This helps to differentiate external classes, from internal
# classes of your own module.
from astropy.cosmology import LambdaCDM
# Same here: import scipy
from scipy.interpolate import interp1d
from scipy.integrate import quad
from scipy.optimize import curve_fit
import os

# Feedback: the name of this file is not great.
# spec.py doesn't really indicate what is the content of the file.
# I would suggest to rename the file to galaxy_sed_analyzer.py
class GalaxySEDAnalyzer:
    """
    A comprehensive tool for Galaxy SED analysis, band extraction, 
    FIR modeling, and automated visualization.
    """

    # Feedback: are the filters something that the user should set,
    # or are those filters something which you always have to use? 
    def __init__(self, filter_dir='suppliments/filters', output_dir='outputs'):
        self.filter_dir = filter_dir
        self.output_dir = output_dir
        self.cosmo = LambdaCDM(H0=70, Om0=0.3, Ode0=0.7)
        self.lsun = np.log10(3.828e26)
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Global plotting style
        plt.rc('font', family='serif')
        plt.rcParams['font.size'] = 14

    def load_filters(self):
        """Returns the filter transmission dictionary."""
        f = self.filter_dir
        return {
            "u": np.loadtxt(f"{f}/CFHT_u.dat"),
            "B": np.loadtxt(f"{f}/SUBARU_B.dat"),
            "g": np.loadtxt(f"{f}/MCam_g.dat"),
            "V": np.loadtxt(f"{f}/SUBARU_V.dat"),
            "r": np.loadtxt(f"{f}/MCam_r.dat"),
            "i_new": np.loadtxt(f"{f}/i_prime.dat"),
            "irac1": np.loadtxt(f"{f}/IRAC1.dat"),
            "irac2": np.loadtxt(f"{f}/IRAC2.dat"),
            "irac3": np.loadtxt(f"{f}/IRAC3.dat"),
            "PACS_blue": np.loadtxt(f"{f}/PACS_blue.dat"),
            "PACS_green": np.loadtxt(f"{f}/PACS_green.dat"),
            "PACS_red": np.loadtxt(f"{f}/PACS_red.dat"),
            "PSW": np.loadtxt(f"{f}/PSW.dat"),
            "PMW": np.loadtxt(f"{f}/PMW.dat"),
            "PLW": np.loadtxt(f"{f}/PLW.dat"),
            "SCUBA850": np.loadtxt(f"{f}/SCUBA850.dat"),
        }

    def extract_flux_in_band(self, wav, flux, band_wave, band_trans):
        """Convolution of SED with filter transmission."""
        ind = np.where((wav > band_wave.min()) & (wav < band_wave.max()))[0]
        if len(ind) == 0: return np.nan

        # Feedback: split code intp multiple lines
        ftrans_interp = interp1d(band_wave, band_trans, bounds_error=False, fill_value=0.0)
        trans_interp = ftrans_interp(wav[ind])

        # Feedback: in newer numpy versions, the routine trapz has been renamed to np.trapezoid.
        # you need to make sure that the user gets the right numpy version by specifying it in
        # pyproject.toml and/or sed-env.yml. For example, when I installed your conda environment, I got 
        # numpy 2.4.2 which has trapezoid, and the lines below resulted in an error for me. 
        numerator = np.trapz(flux[ind] * trans_interp, wav[ind])
        denominator = np.trapz(trans_interp, wav[ind])
        return numerator / denominator if denominator != 0 else np.nan

    # Feedback: here it would be good to add to the docstrings
    # what x, n, t, z are.
    # Another good idea is to write the reference and equation in a comment
    # (not sure if it is the case for this model, it's more of a general comment)
    def catlin_model(self, x, n, t, z):
        """Modified Blackbody model for FIR fitting."""
        beta, alpha = 1.96, 2.3
        xx = (10.0**x) * (1+z)
        c = 3.0e8
        wav2 = c / xx 
        l = ((26.68 + 6.246*alpha)**-2 + (1.905e-4 + 7.243e-5*alpha)*t)**-1
        lc2 = (3.0/4.0 * l) * 1e-6
        l02 = 200.0e-6
        h, k = 6.62607015e-34, 1.380649e-23
       
        # Feedback: split into multiple lines (you can use reformat using 
        # ruff or yapf).
        # It would also be good to add comments regarding what you are
        # specifically calculating  
        npl = (1.0-np.exp(-(l02/lc2)**beta)) * (c/lc2)**3 / (np.exp(h*c/(lc2*k*t))-1.0) * lc2**(-alpha)
        f1 = (1.0-np.exp(-(l02/wav2)**beta)) * (c/wav2)**3 / (np.exp(h*c/(wav2*k*t))-1.0)
        f2 = wav2**alpha * np.exp(-(wav2/lc2)**2)
        return n - 36.5 + np.log10(f1 + npl * f2)

    # Feedback: would be good to add a short description of the parameters
    # in the docstrings.
    def run_analysis(self, galId, snap, z, sed_file):
        """Main execution loop for one galaxy SED."""
        # 1. Load SED
        wav_raw, flux = np.genfromtxt(sed_file, usecols=(0, 1), unpack=True)
        wav_obs = wav_raw * (1 + z)

        # 2. Extract Band Fluxes & Prepare Plot
        bands = self.load_filters()
        band_fluxes = {}
        
        fig, ax = plt.subplots(figsize=(15, 10))
        # Feedback: split into multiple lines
        ax.loglog(wav_obs, flux, color='black', label="SED Spectrum", linewidth=1.5, alpha=0.8)

        # Data logging for fluxes
        flux_path = f'{self.output_dir}/gal_no_{galId}_snap_{snap}_fluxes.dat'
        with open(flux_path, 'w') as f_out:
            f_out.write('# id\t redshift\t ' + '\t '.join(bands.keys()) + '\n')
            f_out.write(f'{galId}\t {z}\t')
            
            for name, data in bands.items():
                b_wav = data[:, 0] * 1e-4 # Å to μm
                f_band = self.extract_flux_in_band(wav_obs, flux, b_wav, data[:, 1])
                band_fluxes[name] = f_band
                f_out.write(f'{f_band:.5e}\t {f_band*0.05:.5e}\t')
                
                # Plot band points
                if not np.isnan(f_band):
                    eff_wave = np.sum(b_wav * data[:,1]) / np.sum(data[:,1])
                    ax.errorbar(eff_wave, f_band, yerr=0.1*f_band, fmt='o', 
                                label=f'{name}', markersize=10, mec='k')

        # 3. FIR Fitting 
        fir_bands = ['PACS_blue','PACS_green','PACS_red','PSW','PMW','PLW','SCUBA850']
        obs_wavs = np.array([70, 100, 160, 250, 350, 500, 850]) * 1e-6
        obs_freqs = co.c.value / obs_wavs
        fir_fl = np.array([band_fluxes[b] for b in fir_bands])
        
        mask = ~np.isnan(fir_fl)
        popt, _ = curve_fit(lambda x, n, t: self.catlin_model(x, n, t, z), 
                            np.log10(obs_freqs[mask]), np.log10(np.abs(fir_fl[mask])), 
                            p0=[1.0, 20.0], bounds=([-4.0, 10.0], [5.0, 100.0]))

        # 4. Physical Properties & Integration
        dis = self.cosmo.luminosity_distance(z).to('m').value
        nu1, nu2 = (co.c.value/1000.0e-6)/(1+z), (co.c.value/8.0e-6)/(1+z)
        
        lbol_raw, _ = quad(lambda x: 10.0**(self.catlin_model(np.log10(x/(1+z)), *popt, z)) 
                           * 1e-29 * 4 * np.pi * dis**2 / (1+z), nu1*(1+z), nu2*(1+z))
        l_ir_solar = 10**(np.log10(lbol_raw) - self.lsun)

        # Write physical properties
        prop_path = f'{self.output_dir}/gal_no_{galId}_snap_{snap}_physical_properties.dat'
        with open(prop_path, 'w') as f_prop:
            f_prop.write('# id\t redshift\t LIR\t Temperature / K \n')
            f_prop.write(f'%.2f\t %.2f\t %.2f\t %.2f\n' % (galId, z, np.log10(l_ir_solar), popt[1]))

        # 5. Finalize Plot
        ax.set_title(f'Galaxy {galId} (Snap {snap}) | Redshift: {z:.2f}')
        ax.set_ylabel('Flux [mJy]')
        ax.set_xlabel(r'Wavelength [$\mu$m]')
        ax.set_xlim(1e-1, 3e3)
        ax.set_ylim(1e-5, 50)
        ax.grid(True, which='both', linestyle='--', alpha=0.5)
        ax.legend(loc='lower right', fontsize=10, ncol=2)
        
        plt.tight_layout()
        fig.savefig(f'{self.output_dir}/best_sed_{galId}_s{snap}.png')
        plt.close(fig) # Close to free memory during loops

        return l_ir_solar, popt[1]
