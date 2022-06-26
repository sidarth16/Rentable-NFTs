from brownie import ERC4907
from brownie import accounts, Wei
import brownie
import pytest
from web3.constants import ADDRESS_ZERO

deployer, user1, user2  = None, None, None
DAY = 1 * 24 * 60 * 60 

@pytest.fixture(scope="module")
def testNft():
    global deployer, user1, user2
    deployer, user1, user2 = accounts[0:3]

    testNft = ERC4907.deploy({"from":deployer})
    return testNft

def test_mint_nft(testNft):

    tx = testNft.nftMint({"from":user1})
    id1 = tx.return_value
    print(f'Minted NFT ( TokenId : {id1} )')
    
    tx = testNft.nftMint({"from":user2})
    id2 = tx.return_value
    print(f'Minted NFT ( TokenId : {id2} )')

    # check Nft Balance
    assert testNft.balanceOf(user1.address) == 1
    assert testNft.balanceOf(user2.address) == 1

    # check Owners
    assert testNft.ownerOf(1) == user1.address
    assert testNft.ownerOf(2) == user2.address

    # check Users
    assert testNft.userOf(1) == ADDRESS_ZERO
    assert testNft.userOf(2) == ADDRESS_ZERO


def test_renting(testNft):
    
    testNft.setUser(1, user2.address, 2*DAY, {"from":user1.address})
    testNft.setUser(2, user1.address, 2*DAY, {"from":user2.address})

    # check Owners
    assert testNft.ownerOf(1) == user1.address
    assert testNft.ownerOf(2) == user2.address

    # check Users
    assert testNft.userOf(1) == user2.address
    assert testNft.userOf(2) == user1.address 

def test_double_rent(testNft):

    # cannot rent to two users 
     with brownie.reverts():
        testNft.setUser(1, user2.address, 2*DAY, {"from":user1.address})         

