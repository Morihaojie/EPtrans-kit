import sys
import os
import numpy as np
from pathlib import Path
script_abs = Path(__file__).resolve()
project_root = script_abs.parent.parent
sys.path.insert(0, str(project_root))
from eptransk.hdf5editor import HDF5_Editor

def fermi_dirac(energy, fermi_level, beta):
    """费米-狄拉克分布"""
    x = beta * (energy - fermi_level)
    x = np.clip(x, -500, 500)
    return 1.0 / (np.exp(x) + 1.0)

def delta_lorentz(x, half_width):
    """洛伦兹展宽"""
    return (half_width / np.pi) / (x**2 + half_width**2)

def delta_gaussian(x, sigma):
    """高斯展宽"""
    return np.exp(-0.5 * (x / sigma)**2) / (np.sqrt(2.0 * np.pi) * sigma)

# ==================== 主计算函数 ====================
def calculate_phonon_electron_scattering_rates(read_hdf5filename, temperature_K=300, broadening_width=0.01, broadening_type='lorentz'):
    """
    参数
    ----------
    read_hdf5filename : str
        HDF5 文件名或路径
    temperature_K : float
        温度 (K)
    broadening_width : float
        展宽宽度 (eV)。洛伦兹时为半高半宽，高斯时为标准差 σ
    broadening_type : str
        展宽类型，'lorentz' 或 'gaussian'

    返回
    -------
    phonon_electron_scattering_rates : np.ndarray, 形状 (nq, nmodes)
    """
    FC=HDF5_Editor()
    hbar = 6.582e-16      # eV·s
    kB = 8.6173e-5        # eV/K
    HARTREE_TO_EV = 27.211386245988
    e_k_all = FC.read_hdf5('/ElectronPhononCoupling_0/eigenvalues_k/array/data', read_hdf5filename)[0]* HARTREE_TO_EV
    nk, nbands = e_k_all.shape
    phonon_frequencies = FC.read_hdf5('/ElectronPhononCoupling_0/eigenvalues_ph/array/data', read_hdf5filename)*0.001 
    nmodes, nq = phonon_frequencies.shape
    fermi_level = FC.read_hdf5('/ElectronPhononCoupling_0/fermi_level/array/data', read_hdf5filename)*HARTREE_TO_EV
    if np.ndim(fermi_level) > 0:
        fermi_level = fermi_level.flat[0]

    # ---------- 准备物理常数 ----------
    beta = 1.0 / (kB * temperature_K)
    if broadening_type == 'lorentz':
        delta_func = lambda x: delta_lorentz(x, broadening_width)
    elif broadening_type == 'gaussian':
        delta_func = lambda x: delta_gaussian(x, broadening_width)
    else:
        raise ValueError("broadening_type must be 'lorentz' or 'gaussian'")

    # ---------- 预计算初态费米分布 ----------
    fermi_initial_all = fermi_dirac(e_k_all, fermi_level, beta)   # (nk, nbands)

    # ---------- 初始化结果数组 ----------
    scattering_rates = np.zeros((nq, nmodes))

    # ---------- 主循环：遍历所有声子模式、能带对 ----------
    for imode in range(nmodes):
        for n_band in range(nbands):
            e_k_n = e_k_all[:, n_band]
            f_k_n = fermi_initial_all[:, n_band]

            for m_band in range(nbands):
                # 读取当前 (imode, m_band, n_band) 的耦合矩阵 (nk, nq)
                g_mn_kq = FC.read_electron_phonon_coupling_matrix_part(imode, m_band, n_band, read_hdf5filename)
                # 读取当前末态能带 m_band 的 e_kplusq 和 e_kminusq
                e_kplusq_m = FC.read_eigen_values_k_plus_q_part(m_band, read_hdf5filename)
                e_kminusq_m = FC.read_eigen_values_k_minus_q_part(m_band, read_hdf5filename)
                # 对每个 q 点求和 k 点贡献
                for iq in range(nq):
                    phonon_freq = phonon_frequencies[imode, iq]
                    # ----- 吸收过程 -----
                    e_kplusq_m_iq = e_kplusq_m[:, iq]
                    f_kplusq = fermi_dirac(e_kplusq_m_iq, fermi_level, beta)
                    delta_abs = e_kplusq_m_iq - e_k_n - hbar * phonon_freq
                    g2_abs = np.abs(g_mn_kq[:, iq]) ** 2
                    contrib_abs = np.sum(g2_abs * (f_k_n - f_kplusq) * delta_func(delta_abs))
                    # ----- 发射过程（对称性近似）-----
                    e_kminusq_m_iq = e_kminusq_m[:, iq]
                    f_kminusq = fermi_dirac(e_kminusq_m_iq, fermi_level, beta)
                    delta_emi = e_kminusq_m_iq - e_k_n + hbar * phonon_freq
                    g2_emi = np.abs(g_mn_kq[:, iq]) ** 2        # 复用相同矩阵元
                    contrib_emi = np.sum(g2_emi * (1.0 - f_k_n + f_kminusq) * delta_func(delta_emi))

                    scattering_rates[iq, imode] += (2.0 * np.pi / hbar) * (contrib_abs + contrib_emi)

    return scattering_rates

def save_scattering_rates(rates, filename, save_format='npy', header=None, output_dir='.'):
    """
    保存到指定目录。

    参数
    ----------
    scattering_rates       : (nq, nmodes) 数组
    filename    : 文件名（不含扩展名）
    save_format : 'npy' 或 'dat'
    header      : 仅 dat 格式的文件头注释
    output_dir  : 如果 output_dir 为 None，则保存到脚本所在目录。
    """
    if output_dir is None:
        try:
            output_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            output_dir = os.getcwd()
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)

    if save_format == 'npy':
        np.save(f"{full_path}.npy", rates)
        print(f"Saved as {full_path}.npy")
    elif save_format == 'dat':
        np.savetxt(f"{full_path}.dat", rates, fmt='%.6e', delimiter=' ',
                   header=header if header else '', comments='')
        print(f"Saved as {full_path}.dat")
    else:
        raise ValueError("save_format must be 'npy' or 'dat'")

read_hdf5filename = r'electron_phonon_coupling_hdf5filename.hdf5'
temperature_K = 300
output_prefix = 'scattering_rates'

# 计算散射几率（洛伦兹展宽）
broadening_width=0.01
scattering_rates_lorentz = calculate_phonon_electron_scattering_rates(read_hdf5filename, temperature_K, broadening_width, broadening_type='lorentz')
lorentz_filename = f"{output_prefix}_lorentz"
save_scattering_rates(scattering_rates_lorentz, lorentz_filename, save_format='dat',
            header=f"# Lorentz broadening, width={broadening_width} eV, T={temperature_K} K")

# # 计算散射几率（高斯展宽）
broadening_width=0.01
scattering_rates_gauss = calculate_phonon_electron_scattering_rates(read_hdf5filename, temperature_K, broadening_width, broadening_type='gaussian')
gauss_filename = f"{output_prefix}_gaussian"
save_scattering_rates(scattering_rates_gauss, gauss_filename, save_format='npy',
            header=f"# Gaussian broadening, sigma={broadening_width} eV, T={temperature_K} K")