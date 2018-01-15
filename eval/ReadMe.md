# The most important remark, that we assume meteor-1.5,terecom-0.7.25, OpenNMT-py-master folders are in the main directory Evaluation, with all the following folders. 

# the file (ExtendedSystem_Seen_Unseen.md) explain how to prepare for evaluating the whole seen\unseen dataset according to our extended system for the three model: flat, str1, str2.

# preds --> contains all the predictions for the extended system for the three model: flat,str1,str2, for seen\unseen dataset

# ref --> contains all references for the extended system for seen\unseen dataset

# We divided each model according to dataset type into the following folders:

# baselineSeen --> contain all files and scripts for evalauting seen dataset according to the modified baseline, where the file seen_instruction.md in it explain the preprocessing steps and the associated commands 

# flatSeen -->  contain all files and scripts for evalauting seen dataset according to the model (flat) of our extended system

# str1Seen -->  contain all files and scripts for evalauting seen dataset according to the model (structure1) of our extended system

# str1Seen -->  contain all files and scripts for evalauting seen dataset according to the model (structure2) of our extended system

# seenScore --> contain all the score files for: modified-baseline, flat, str1, str2 for seen dataset, also the script (generateLxtable.py) for generating latex tables for seen.

# baselineunSeen --> contain all files and scripts for evalauting Unseen dataset according to the modified baseline, where the file unseen_instruction.md in it explain the preprocessing steps and the associated commands

# flatUnseen -->  contain all files and scripts for evalauting unseen dataset according to the model (flat) of our extended system

# str1Unseen -->  contain all files and scripts for evalauting unseen dataset according to the model (structure1) of our extended system

# str1Unseen -->  contain all files and scripts for evalauting unseen dataset according to the model (structure2) of our extended system

# unseenScore --> contain all the score files for: modified-baseline, flat, str1, str2 for seen dataset, also the script (generateLxtable.py) for generating latex tables for unseen.

# tripleBaselineSeen --> contain all files and scripts for evalauting seen dataset according to different triple-size for the modified-baseline, where the file instruction.md in it explain the preprocessing steps and the associated commands 

# tripleFlatSeen --> contain all files and scripts for evalauting seen dataset according to different triple-size for flat model, where the file (flat_Triple_Size.md) in it explain the evalauting steps and the associated commands 

# tripleSeenScore --> contain all the score files for: modified-baseline, flat for seen dataset according to different triple size, where the script (generateLxtable_Triple.py) generate latex tables for them.


# Category_Baseline_Seen --> contain all files and scripts for evalauting seen dataset according to different DBpedia categories for the modified-baseline, where the file (Instruction.md) in it explain the preprocessing steps and the associated commands

# Category_Flat_Seen --> contain all files and scripts for evalauting seen dataset according to different DBpedia categories for flat model, where the file (Seen_Category_Evaluation.md) in it explain the evalauting steps and the associated commands

# Category_Seen_Score --> contain all the score files for: modified-baseline, flat for seen dataset according to different DBpedia categories, where the script (generateLxtable_Category.py) generate latex tables.

# triple_baseline_Unseen -->  contain all files and scripts for evalauting unseen dataset according to different triple-size for the modified-baseline, where the file Instruction.md in it explain the preprocessing steps and the associated commands 

# triple_flat_Unseen --> contain all files and scripts for evalauting unseen dataset according to different triple-size for flat model, where the file (flat_TripleSize_Unseen.md) in it explain the evalauting steps and the associated commands 

# triple_unseenScore --> contain all the score files for: modified-baseline, flat for unseen dataset according to different triple size, where the script (generateLxtable_Triple.py) generate latex tables.

# Category_Baseline_unseen --> contain all files and scripts for evalauting unseen dataset according to different DBpedia categories for the modified-baseline, where the file (category_Unseen.md) in it explain the preprocessing steps and the associated commands

# Category_Flat_unseen --> contain all files and scripts for evalauting unseen dataset according to different DBpedia categories for flat model, where the file (unseen_Category_Evaluation.md) in it explain the evalauting steps and the associated commands

# Category_unseen_Score --> contain all the score files for: modified-baseline, flat for unseen dataset according to different DBpedia categories, where the script (generateLxtable_Category.py) generate latex tables for them.
