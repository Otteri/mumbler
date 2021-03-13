from parlai.scripts.train_model import TrainModel

# Fine tuning parameters are given in:
# https://parl.ai/projects/recipes/

TrainModel.main(
    task='blended_skill_talk,wizard_of_wikipedia,convai2:normalized', 
    model='transformer/generator',
    multitask_weights='1,3,3,3', # string?
    
    # initialize with a pretrained model
    #init_model='zoo:tutorial_transformer_generator/model',     #'internal:vainamoinen_90M',
    #dict_file='zoo:tutorial_transformer_generator/model.dict', #'internal:vainamoinen_90M.dict',

    init_model='/app/ParlAI/parlai_internal/models/vainamoinen_90M.checkpoint',     #'internal:vainamoinen_90M',
    dict_file='/app/ParlAI/parlai_internal/models/vainamoinen_90M.checkpoint.dict', #'internal:vainamoinen_90M.dict',

    # These must match with pretrained model (see link)
    embedding_size=512,
    n_layers=8,
    ffn_size=2048,
    dropout=0.1,
    n_heads=16,
    learn_positional_embeddings=True,
    n_positions=512,
    variant='xlm',
    activation='gelu',
    skip_generation=True, # speds up validation, must be turned off
    fp16=True,
    text_truncate=512,
    label_truncate=128,
    dict_tokenizer='bpe',
    dict_lower=True,
    lr=1e-06,
    optimizer='adamax',
    lr_scheduler='reduceonplateau',
    gradient_clip=0.1,
    veps=0.25,
    betas='0.9,0.999', # string?
    update_freq=1,
    attention_dropout=0.0,
    relu_dropout=0.0,
    vp=15,
    stim=60,
    vme=20000,
    batchsize=12,
    validation_metric='ppl',
    vmm='min',
    save_after_valid=True,
    model_file="/app/ParlAI/parlai_internal/models/vainamoinen_90M",
)
