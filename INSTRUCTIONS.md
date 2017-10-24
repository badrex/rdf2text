# Instructions


## Linearisation, tokenisation, delexicalisation

    python3 webnlg_baseline_input.py -i <data-directory>


## Training a model and generating verbalisations

### STEP1: Preprocess the data

With OpenNMT and Torch :

    th preprocess.lua -train_src <data-directory>/train-webnlg-all-delex.triple -train_tgt <data-directory>/train-webnlg-all-delex.lex -valid_src <data-directory>/dev-webnlg-all-delex.triple -valid_tgt <data-directory>/dev-webnlg-all-delex.lex -src_seq_length 70 -tgt_seq_length 70 -save_data baseline

With OpenNMT-py and Pytorch:

    python3 -train_src <data-directory>\train-webnlg-all-delex.triple -train_tgt <data-directory>\train-webnlg-all-delex.lex -valid_src <data-directory>\dev-webnlg-all-delex.triple -valid_tgt <data-directory>\dev-webnlg-all-delex.lex -src_seq_length 70 -tgt_seq_length 70 -save_data baseline

### STEP2: Train the model

With OpenNMT and Torch :

    th train.lua -data baseline-train.t7 -save_model baseline

With OpenNMT-py and Pytorch:

    python3 train.py -data baseline -save_model baseline-model

### STEP3: Translate

With OpenNMT and Torch :

    th translate.lua -model baseline_epoch13_*.t7 -src <data-directory>/dev-webnlg-all-delex.triple -output baseline_predictions.txt

With OpenNMT-py and Pytorch:

    python3 translate.py -model baseline-model_acc_69.57_ppl_3.56_e13.pt -src <data-directory>\dev-webnlg-all-delex.triple -output baseline_pred.txt


## Relexicalisation

    python3 webnlg_relexicalise.py -i <data-directory> -f <OpenNMT-directory>/baseline_predictions.txt

(all-notdelex-source.triple and dev-webnlg-all-notdelex.triple must already be in the directory)


## Evaluating on a development set

    ./calculate_bleu_dev.sh