import numpy as np
from spec import GalaxySEDAnalyzer

# 1. Initialize the Analyzer
# This sets up the cosmology and the output folders
analyzer = GalaxySEDAnalyzer(
    filter_dir='suppliments/filters', 
    output_dir='outputs'
)

# 2. Setup your parameters
# Usually, you would load these from a file
try:
    redshifts = np.loadtxt('suppliments/outputs.txt')
    galId = 1
    snap = 110
    
    # Check if snap exists in your redshift file
    if snap < len(redshifts):
        z = redshifts[int(snap)][1]
    else:
        z = 0.5  # Fallback example redshift
        print("Snap index out of range, using fallback redshift.")

    # 3. Define the path to your specific SED file
    sed_file_path = "suppliments/sed_flux1_1.txt"

    # 4. Run the Pipeline
    # This extracts fluxes, fits the model, saves .dat files, and saves the .png plot
    print(f"Starting analysis for Galaxy {galId} (Snap {snap})...")
    
    lir, temp = analyzer.run_analysis(
        galId=galId, 
        snap=snap, 
        z=z, 
        sed_file=sed_file_path
    )

    print("-" * 30)
    print("Analysis Successful!")
    print(f"L_IR (solar): 10^{np.log10(lir):.2f}")
    print(f"Dust Temp: {temp:.2f} K")
    print(f"Files saved in: {analyzer.output_dir}/")

except Exception as e:
    print(f"An error occurred: {e}")