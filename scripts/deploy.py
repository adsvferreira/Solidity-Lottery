import time
from brownie import Lottery, config, network
from scripts.helpers import get_account, get_contract, fund_with_link


def deploy_lottery():
    # address _priceFeedAddress,
    # address _vrfCoordinator,
    # address _link_token_contract,
    # uint256 _fee,
    # bytes32 _keyHash
    account = get_account()
    price_feed_address = get_contract("eth_usd_price_feed").address
    vrf_coordinator_address = get_contract("vrf_coordinator").address
    link_token_address = get_contract("link_token").address
    fee = config["networks"][network.show_active()]["fee"]
    keyhash = config["networks"][network.show_active()]["keyhash"]
    lottery = Lottery.deploy(
        price_feed_address,
        vrf_coordinator_address,
        link_token_address,
        fee,
        keyhash,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Contract deployed to {lottery.address}")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started!!!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    print(f"EntranceFee {lottery.getEntranceFee()}")
    value = lottery.getEntranceFee() + 100000000
    print(f"EntranceAmount {value}")
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("One step closer to the win!!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract with LINK
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    # then end the lottery
    ending_tx = lottery.endLottery(
        {
            "from": account,
        }
    )
    ending_tx.wait(1)
    # Wait for ChainLink node to retrieve randomness:
    # Not going to work on local net - No active chainlink nodes
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()


# Firstt successfully deployed contract on Rinkeby: 0x964FF99Ff53DbAaCE609eB2dA09953F9b9CAeec3
