import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from gentariumd import GentariumDaemon
from gentarium_config import GentariumConfig


def test_gentariumd():
    config_text = GentariumConfig.slurp_config_file(config.gentarium_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000ebdf1f5d60db781cf3d826a81eaceb33746c22739245e0ef0b4a0316747'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000009e88bb6c7e27da3bb9b9a986b37950be4b5acb6fd7cc19faed35bb6578a'

    creds = GentariumConfig.get_rpc_creds(config_text, network)
    gentariumd = GentariumDaemon(**creds)
    assert gentariumd.rpc_command is not None

    assert hasattr(gentariumd, 'rpc_connection')

    # Gentarium testnet block 0 hash == 0x000009E88BB6C7E27DA3BB9B9A986B37950BE4B5ACB6FD7CC19FAED35BB6578A
    # test commands without arguments
    info = gentariumd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert gentariumd.rpc_command('getblockhash', 0) == genesis_hash
