# OTA-FL: Over-the-Air Federated Learning with USRPs

This repository provides the codebase to implement **Over-the-Air Federated Learning (OTA-FL)** on real wireless testbeds using **NI USRP devices**.  
OTA-FL enables **analog aggregation of model updates directly over the air** using OFDM-based transmissions with synchronization and channel estimation.

---

## Features
- End-to-end OTA-FL implementation on USRPs  
- Compatible with **any ML framework** (TensorFlow, PyTorch, etc.)  
- Export local model weights as binary (`.bin`) files  
- Transmission of weights via **GNU Radio 3.10 + UHD ≥ 4.3**  
- OFDM waveform generation with adaptive precoding  
- Wireless aggregation of model updates  
- **Frame synchronization** using Zadoff-Chu sequences  
- **DMRS pilot-based channel estimation**  
- Global model reconstruction and redistribution  
- Iterative training until convergence  

---

## Requirements
- **GNU Radio**: 3.10  
- **UHD**: ≥ 4.3  
- **Python**: 3.10  
- **TensorFlow**: 2.15 (default; works with other ML frameworks)  
- NI USRP hardware (tested with X310, B210, etc.)  

---

## Workflow
1. **Local Training**  
   Train models on clients with TensorFlow (or another ML framework) and extract weights as `.bin` files.  

2. **Over-the-Air Transmission**  
   Convert weights into OFDM frames and transmit via USRP using GNU Radio with adaptive precoding.  

3. **Aggregation**  
   Model updates are aggregated directly in the wireless medium.  

4. **Reception & Processing**  
   Perform frame sync with Zadoff-Chu and channel estimation with DMRS pilots to recover aggregated weights.  

5. **Global Model Update**  
   Feed global weights back into TensorFlow (or other ML frameworks) and distribute to clients.  

6. **Iteration**  
   Repeat until the global model converges.  

---

---

## 📖 Citation
If you use this repository in your research, please cite:

[1] S. Pradhan, A. Koc, D. Muruganandham, M. Arfaoui, P. Pietraski, G. Zhang, J. Kaewell, K. R. Chowdhury, 
**"Deploying Over-the-air Federated Learning in Real-world Multi-antenna Systems’"**,
IEEE Conference on Computer Communications (INFOCOM), May 2026.

[2] S. Pradhan, A. Koc, K. Alemdar, M. Arfaoui, P. Pietraski, F. Periard, G. Zhang, M. Hudon, K. R. Chowdhury,  
**"Experimental Demonstration of Over the Air Federated Learning for Cellular Networks"**,  
accepted, *IEEE International Conference on Machine Learning for Communication and Networking (ICMLCN)*, 2025.
