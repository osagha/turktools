
python helper_scripts/csv_to_items.py
python lister.py stimuli/prior-items.txt filler 1 0 6 no
python lister.py stimuli/posterior-items.txt filler 1 0 30 no
python lister.py stimuli/relevance-items.txt filler 1 0 30 no
python lister.py stimuli/helpfulness-items.txt filler 1 0 30 no

python templater.py html/skeletons/prior.skeleton.html 15 HEDGEHOG_OLYMPICS
python templater.py html/skeletons/posterior.skeleton.html 15 HEDGEHOG_OLYMPICS
python templater.py html/skeletons/relevance.skeleton.html 15 HEDGEHOG_OLYMPICS
python templater.py html/skeletons/helpfulness.skeleton.html 15 HEDGEHOG_OLYMPICS

mv html/skeletons/*HEDGEHOG_OLYMPICS* html/templates