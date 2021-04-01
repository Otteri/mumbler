#!/usr/bin/env python3

"""
Reads text coming from a pipe and lets agent to generate reply
"""

from typing import Optional
from parlai.core.params import ParlaiParser
from parlai.core.opt import Opt
from parlai.core.agents import Agent
from parlai.core.message import Message
from parlai.utils.misc import display_messages, load_cands
from parlai_internal.mumbler import config as cfg
import os

PIPE = cfg.PIPE_DISCORD2AGENT
MSG_LENGTH = cfg.MSG_LENGTH # NN model can take in max ~300 char sequences
# Let writer close and handle fifo

class LocalHumanAgent(Agent):
    @classmethod
    def add_cmdline_args(
        cls, parser: ParlaiParser, partial_opt: Optional[Opt] = None
    ) -> ParlaiParser:
        agent = parser.add_argument_group('Local Human Arguments')
        return parser

    def __init__(self, opt, shared=None):
        super().__init__(opt)
        self.id = 'localHuman'
        self.episodeDone = False
        self.finished = False
        self.fixedCands_txt = load_cands(self.opt.get('local_human_candidates_file'))
        self.p = os.open(PIPE, os.O_RDONLY)

    def epoch_done(self):
        return self.finished

    def observe(self, msg):
        print(
            display_messages(
                [msg],
                add_fields=self.opt.get('display_add_fields', ''),
                prettify=self.opt.get('display_prettify', False),
                verbose=self.opt.get('verbose', False),
            )
        )

    def act(self):
        reply = Message()
        reply['id'] = self.getID()
        content_length = 0
        try:         
            while content_length == 0:
                # Poll pipe
                text = str(os.read(self.p, MSG_LENGTH).decode("utf8"))
                content_length = len(text)
                print(f"Processing captured text: {text}")
        except EOFError:
            self.finished = True
            return {'episode_done': True}

        reply_text = text.replace('\\n', '\n')
        reply['episode_done'] = False
        reply['label_candidates'] = self.fixedCands_txt
        reply['text'] = reply_text
        return reply

    def episode_done(self):
        return self.episodeDone