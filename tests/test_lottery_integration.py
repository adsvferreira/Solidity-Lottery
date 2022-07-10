import pytest, time
from scripts.deploy import deploy_lottery
from brownie import Lottery, accounts, config, network
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link, get_contract


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    # Act
    lottery.endLottery({"from": account})
    time.sleep(60)  # wait for link node response
    # Assert
    assert lottery.recentWinner == account
    assert lottery.balance() == 0
