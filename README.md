# Retweet Us, We Will Retweet You: Spotting Collusive Retweeters Involved in Blackmarket Services

This is the code and the dataset for the paper titled 

>[Retweet Us, We Will Retweet You: Spotting Collusive Retweeters Involved in Blackmarket Services. *Hridoy Sankar Dutta, Aditya Chetan\*, Brihi Joshi\*, Tanmoy Chakraborty*](https://arxiv.org/abs/1806.08979)

accepted at [The IEEE/ACM International Conference on Social Networks Analysis and Mining (ASONAM 2018)](http://asonam.cpsc.ucalgary.ca/2018/).

If you end up using this code or the data, please cite the following paper - 
```
@misc{1806.08979,
Author = {Hridoy Sankar Dutta and Aditya Chetan and Brihi Joshi and Tanmoy Chakraborty},
Title = {Retweet Us, We Will Retweet You: Spotting Collusive Retweeters Involved in Blackmarket Services},
Year = {2018},
Eprint = {arXiv:1806.08979},
}
```

# Quick Start

## Requirements

- Python 2.7.x
To install the dependencies used in the code, you can use the __requirements.txt__ file as follows -

```
pip install -r requirements.txt
```

## Running the code

First ```cd code``` and then run the ```classifiers.py``` as follows - 

```
python classifiers.py -b
```
This will generate results for binary classification as mentioned in the paper.
For generating results for the multi-class scenario, use __-m__ instead of __-b__.

# License 

Copyright (c) 2018 Hridoy Sankar Dutta, Aditya Chetan, Brihi Joshi, Tanmoy Chakraborty

For license information, see [LICENSE](LICENSE) or http://mit-license.org
