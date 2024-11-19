# rSDE-Bench: Requirement-Oriented Software Development Benchmark

[![paper](https://img.shields.io/badge/arXiv-Paper-<COLOR>.svg)](https://arxiv.org/abs/2410.16946)
[![project](https://img.shields.io/badge/project-Page-blue)](https://yuzhu-cai.github.io/rSDE-Bench/)

Code and data for paper "[Self-Evolving Multi-Agent Collaboration Networks for Software Development](https://arxiv.org/abs/2410.16946)".

## 👋 Overview
rSDE-Bench is a requirement-oriented benchmark designed to evaluate the ability of models to handle software-level coding tasks. Unlike instruction-based approaches, rSDE-Bench uses detailed software requirements as input, specifying each functionality and constraint of the software. The benchmark includes automatic evaluation through unit tests, providing a more realistic assessment aligned with real-world software development practices.

<img src="assets/figs/evaluation.jpg">


## 🚀 Set Up

Make sure to use python 3.8 or later:
```
conda create -n rsde_bench python=3.8
conda activate rsde_bench
```

Check out and install this repository:
```
git clone https://github.com/yuzhu-cai/rSDE-Bench.git
cd rSDE-Bench
pip install -r requirement.txt
```

## 💽 Usage
> [!WARNING]
> **Operating System:** Ensure that you are running this project on an operating system with a graphical user interface. Currently, **Windows** and **macOS** are supported.
> 
> **Dependencies:** Make sure all dependencies are correctly installed and the appropriate Python environment is activated.

Use the following command to generate the software included in `rSDE-Bench` using the GPT, Claude, or Gemini APIs. The generated code will be stored in the `codes` directory.

```bash
python run_infer.py
```

Evaluate the software code generated in the `codes` directory with the following command:

```bash
python run_eval.py
```

To aggregate the performance and differences of the software code generated under various settings, run:

```
python update_result.py
```


## ✍️ Citation

If you find our work helpful, please use the following citations.

```
@misc{hu2024selfevolvingmultiagentcollaborationnetworks,
      title={Self-Evolving Multi-Agent Collaboration Networks for Software Development}, 
      author={Yue Hu and Yuzhu Cai and Yaxin Du and Xinyu Zhu and Xiangrui Liu and Zijie Yu and Yuchen Hou and Shuo Tang and Siheng Chen},
      year={2024},
      eprint={2410.16946},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2410.16946}, 
}
```