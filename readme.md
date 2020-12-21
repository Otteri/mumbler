# Mumbler

Start bot with `$ python3 bot.py`



## Installation
`Docker build .`

## NLP module
nlp has been implemented as a python module. Calls must be done outside the module.
nlp package defines following callable functions

Example call:
`$ python3 train.py --path "profile1/" --load --useGpu --epochs 10000 `

### Profiles

Currently the NN input and output layer dimensions have direct relation to number of training inputs.
Neural net must be trained again if training vocabulary size changes.
Therefore, it is recommended to store NN weigths and training data into same directory,
so it is easy to track what data was used to train certain weights.
```
profile1/
├─ econder.pt
├─ decoder.pt
├─ vocabulary1.txt
└─ vocabulary2.txt
```


Note for myself:
profile1/ is eng -> fin
profile2/ is eng -> kalevala (google translated sentences)

Steps to crate a new profile.
Obtain a file at leas with one translation.
Train for a while to produce encoder & decoder files.
Now profile can be used normally and it is possible to add more words to text files.

### NLP interface

It can be either a human or bot calling the NLP. For bot to be able to succesfully
utilize the nlp functionality, a clear interface must be defined. Hence, a few interface classes have been implemented.

```
TrainingSettings
        self.data_path = data_path
        self.load_model = load_model
        self.device = device
        self.epochs = epochs
        self.save_every = save_every
```

For convience, a couple scripts mapping args to class inputs have been defined. User can easily use the nlp with these helper scripts.
