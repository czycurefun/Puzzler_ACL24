# Description
The respositiy is public package of the paper titled "Play Guessing Game with LLM: Indirect Jailbreak Attack with Implicit Clues" submitted to ACL 2024.

Puzzler Architecture:  
![Image text](https://github.com/czycurefun/IJBR/blob/main/fig/final_artifactureV2.0.png)
- OMG.py is to generate offensive strategies  
- jailbreak.py is to jailbreak LLM

Updated Result:  
![Image text](https://github.com/czycurefun/IJBR/blob/main/fig/new_result.jpg)

![Image text](https://github.com/czycurefun/IJBR/blob/main/fig/new_defense_result.jpg)

# Experiment Setup  
We maintained the default configuration of GPT-3.5, GPT-4, and GPT-4 Turbo with temperature = 1 and top_n = 1

# Run the code
For a one-sample reproducible run:

```bash
export ANTCHAT_API_KEY="YOUR_REAL_KEY"
./run_reproduction.sh
```

Manual run:

```bash
python OMG.py --input data/harmful_behaviors_custom.xlsx --output data/reproduction/offense.real.json --overwrite --limit 1 --max-defenses 1 --model deepseek-v4-flash
python jailbreak.py --input data/reproduction/offense.real.json --output data/reproduction/jailbreak.real.json --overwrite --limit 1 --model deepseek-v4-flash
```

See `docs/reproduction.md` for the method summary, model configuration, and alternative provider usage.






