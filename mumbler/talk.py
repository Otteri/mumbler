#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Basic script which allows local human keyboard input to talk to a trained model.
## Examples
```shell
parlai interactive -m drqa -mf "models:drqa/squad/model"
```
When prompted, enter something like: `Bob is Blue.\\nWhat is Bob?`
Input is often model or task specific, but in drqa, it is always
`context '\\n' question`.
"""
from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from parlai.core.script import ParlaiScript, register_script
from parlai_internal.mumbler.agents.agent import LocalHumanAgent
from parlai_internal.mumbler import config as cfg
import random
import os

pipe = os.open(cfg.PIPE_AGENT2DISCORD, os.O_SYNC | os.O_CREAT | os.O_RDWR)

# Some info of opts can be found from:
# https://www.parl.ai/docs/core/params.html
# and tutorial_tipsntricks.md
def setup_args(parser=None):
    if parser is None:
        parser = ParlaiParser(
            True, True, 'Interactive chat with a model on the command line'
        )
    parser.set_defaults(interactive_mode=True, task='interactive_talk', interactive_task=True, include_personas=True)
    LocalHumanAgent.add_cmdline_args(parser)
    return parser


def interactive_talk(opt):
    # Create model and assign it to the specified task
    agent = create_agent(opt, requireModelExists=True)
    agent.opt.log()
    human_agent = LocalHumanAgent(opt)

    # set up world logger
    world = create_task(opt, [human_agent, agent])

    # Main loop, wait text from the agent and forward to the pipe
    while not world.epoch_done():
        world.parley()
        for a in world.acts:
            if a['id'] != 'localHuman': # Do not process user inputs
                text = a['text']
                os.write(pipe, f"{text}".encode("utf8")) # convert to b'
                if world.epoch_done():
                    print('EPOCH DONE')
                    break

@register_script('interactive_talk', aliases=['i'])
class Interactive(ParlaiScript):
    @classmethod
    def setup_args(cls):
        return setup_args()

    def run(self):
        return interactive_talk(self.opt)


if __name__ == '__main__':
    random.seed(404)
    Interactive.main()
