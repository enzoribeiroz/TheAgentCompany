# TheAgentCompany Experiments
This repository contains the trajectories and jsonl files for the experiments conducted by The Agent Company.

The repository is organized as follows:
```
experiments/
├── evaluation/
│ ├── 1.0.0/
|   ├── <date>_<model>
│   │ ├── README.md
│   │ ├── results/<task_id>.json (Evaluator records, checkpoint Scores)
│   │ ├── screenshots/<task_id>/<step>.png (Screenshot Logs)
│   │ └── trajectories/<task_id>.json.gz (Compressed Agent Trajectries)
│   └── ...
```

The `evaluation/` folder is organized such that the top level directories are different versions of TheAgentCompany (currently only 1.0.0).

Data for models that were run on that corresponding version are included as subfolders.
Each subfolder contains all the evaluation results for each task with detailed evaluator records, checkpoint scores, agent execution logs, and screenshots (if applicable, e.g. using browser).

These logs are publicly accessible and meant to enable greater reproducibility and transparency of the experiments.


## 🏆 Leaderboard Participation

If you are interested in submitting your model to the [The Agent Company Leaderboard](https://the-agent-company.com/#/leaderboard), please do the following:
1. Fork this repository.
1. Clone your fork.
1. Run evaluation and submit the results, under the version that you evaluate on (currently there's only 1.0.0), create a new folder with the submission date and the model name (e.g. 20241217_OpenHands-0.14.2-gemini-1.5-pro).
1. Within the folder, please include the following **required** assets, one of the best ways to understand the files is to look at the existing experiment files from other folders:
      * results/: eval*.json, one for each task
      * trajectories/: Reasoning trace reflecting how your system solved the problem. Submit one reasoning trace per task instance. The reasoning trace should show all of the steps your system took while solving the task. If your system outputs thoughts or comments during operation, they should be included as well. The reasoning trace can be represented with any text based file format (e.g. md, json, yaml). Ensure the task instance ID is in the name of the corresponding reasoning trace file. For an example, see OpenHands + Claude 3.5 Sonnet. If the file is too big due to long trajectory, you can use gzipped (.gz) files. 
      * screenshots/: if applicable, e.g. the screenshots of tasks using browser.
      * README.md: The model name, version, result summary, and any other relevant information. Include anything you'd like to share about your model here!
1. Create a pull request to this repository with the new folder.

Please check out this [doc](https://github.com/TheAgentCompany/TheAgentCompany?tab=readme-ov-file#quick-start) to run evaluation.

## ✅ Result Verification

If you are interested in receiving the "verified" checkmark ✓ on your submission, please do the following:

1. Create an issue
2. In the issue, provide us instructions on how to run your model on TheAgentCompany.
3. We will run your model on a random subset of TheAgentCompany and verify the results.

## 📞 Contact
Questions? Please create an issue. Otherwise, you can also contact fangzhex@cs.cmu.edu, yufans@alumni.cmu.edu, boxuanli@alumni.cmu.edu

## ✍️ Citation
```
@misc{xu2024theagentcompanybenchmarkingllmagents,
      title={TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks}, 
      author={Frank F. Xu and Yufan Song and Boxuan Li and Yuxuan Tang and Kritanjali Jain and Mengxue Bao and Zora Z. Wang and Xuhui Zhou and Zhitong Guo and Murong Cao and Mingyang Yang and Hao Yang Lu and Amaad Martin and Zhe Su and Leander Maben and Raj Mehta and Wayne Chi and Lawrence Jang and Yiqing Xie and Shuyan Zhou and Graham Neubig},
      year={2024},
      eprint={2412.14161},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2412.14161}, 
}
```
