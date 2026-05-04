import sys
import os
import numpy as np
from pathlib import Path
script_abs = Path(__file__).resolve()
project_root = script_abs.parent.parent
sys.path.insert(0, str(project_root))
from eptransk.hdf5editor import HDF5_Editor

def gaussian(x, sigma):
        return np.exp(-0.5*(x/sigma)**2) / (sigma * np.sqrt(2*np.pi))

def calculate_energy_dependent_relaxation_time(read_hdf5filename):
    FC=HDF5_Editor()
    completed_inverse_relaxation_time = FC.read_hdf5('/Mobility_0/inverse_relaxation_time/array/data',read_hdf5filename)
    eigen_values = FC.read_hdf5('/Mobility_0/eigenvalues_k/array/data',read_hdf5filename)
    fermi_level = FC.read_hdf5('/Mobility_0/fermi_level/array/data',read_hdf5filename)
    velocities = FC.read_hdf5('/Mobility_0/velocities_k/array/data',read_hdf5filename)
    HARTREE_TO_EV = 27.211386245988
    energies_relative = eigen_values[0]* HARTREE_TO_EV-fermi_level* HARTREE_TO_EV
    scattering_rates_total = np.sum(completed_inverse_relaxation_time[0], axis=0)
    relaxation_time_total = np.where(scattering_rates_total > 0, 1.0 / scattering_rates_total, 1e20)
    velocities_sq = np.sum(velocities**2, axis=2)
    Nk, Nb = eigen_values[0].shape
    energies_flat = energies_relative.reshape(-1)
    relaxation_time_flat = relaxation_time_total.reshape(-1)
    velocities_sq_flat = velocities_sq.reshape(-1)
    weights_flat = np.ones(Nk * Nb)
    Emin = np.min(energies_flat) - 0.5
    Emax = np.max(energies_flat) + 0.5
    dE = 0.01
    sigma = 0.05
    Egrid = np.arange(Emin, Emax, dE)
    nbins = len(Egrid)
    transport_dos_weighted = np.zeros(nbins)   # 分母: Σ w * v^2 * δ
    tau_weighted_sum = np.zeros(nbins)         # 分子: Σ w * τ * v^2 * δ
    for e, tau, v_sq, w in zip(energies_flat, relaxation_time_flat, velocities_sq_flat, weights_flat):
        if tau == 0 or v_sq == 0:
            continue
        delta = Egrid - e
        gauss = gaussian(delta, sigma)
        transport_dos_weighted += w * v_sq * gauss
        tau_weighted_sum += w * tau * v_sq * gauss

    nonzero = transport_dos_weighted > 1e-12
    energy_dependent_relaxation_time = np.zeros(nbins)
    energy_dependent_relaxation_time[nonzero] = tau_weighted_sum[nonzero] / transport_dos_weighted[nonzero]
    # 保存
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'energy_dependent_relaxation_time.dat')

    np.savetxt(output_path, 
            np.column_stack((Egrid, energy_dependent_relaxation_time)),
            header='Energy - E_F (eV)   Energy_Dependent_Relaxation_Time (fs)')
    print("File 'energy_dependent_relaxation_time.dat' written to current folder.")

def calculate_carrier_average_relaxation_time(read_hdf5filename, T, kweights=None):
    kB = 8.617333262145e-5
    HARTREE_TO_EV = 27.211386245988
    FC=HDF5_Editor()
    completed_inverse_relaxation_time = FC.read_hdf5('/Mobility_0/inverse_relaxation_time/array/data',read_hdf5filename)
    eigen_values = FC.read_hdf5('/Mobility_0/eigenvalues_k/array/data',read_hdf5filename)
    fermi_level = FC.read_hdf5('/Mobility_0/fermi_level/array/data',read_hdf5filename)
    scattering_rates_total = np.sum(completed_inverse_relaxation_time[0], axis=0)  
    Nk, Nb = eigen_values[0].shape
    if kweights is None:
        kweights = np.ones(Nk)
    else:
        kweights = np.asarray(kweights).ravel()
        if len(kweights) != Nk:
            raise ValueError(f"kweights length {len(kweights)} != Nk {Nk}")
    kweights_expanded = kweights[:, np.newaxis]
    epsilon_rel = eigen_values[0]* HARTREE_TO_EV - fermi_level* HARTREE_TO_EV
    # 费米-狄拉克分布导数: -∂f/∂ε = f*(1-f)/kT
    kT = kB * T
    x = epsilon_rel / kT
    # 避免指数溢出（np.exp 处理大负数/正数自动饱和）
    f = 1.0 / (1.0 + np.exp(-x))
    fermi_deriv = f * (1 - f) / kT
    weight = kweights_expanded * fermi_deriv
    mask_electron = (epsilon_rel > 0)
    mask_hole     = (epsilon_rel < 0)

    def average_relaxation_time_for_mask(mask):
        if not np.any(mask):
            return np.nan
        rates = scattering_rates_total[mask]
        w = weight[mask]
        sum_w = np.sum(w)
        if sum_w == 0:
            return np.nan
        avg_rate = np.sum(rates * w) / sum_w
        return 1.0 / avg_rate
    relaxation_time_e = average_relaxation_time_for_mask(mask_electron)
    relaxation_time_h = average_relaxation_time_for_mask(mask_hole)
    return {'electron': relaxation_time_e, 'hole': relaxation_time_h}

read_hdf5filename = r'mobility_hdf5filename.hdf5'
Temperature = 300

calculate_energy_dependent_relaxation_time(read_hdf5filename)
print(calculate_carrier_average_relaxation_time(read_hdf5filename,Temperature))
