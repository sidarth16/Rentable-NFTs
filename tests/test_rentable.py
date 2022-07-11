from brownie import ERC4907
from brownie import accounts, Wei, chain
import brownie
import pytest
from web3.constants import ADDRESS_ZERO

deployer, owner1, owner2  = None, None, None
user1, user2 = None, None
DAY = 1 * 24 * 60 * 60 

@pytest.fixture(scope="module")
def testNft():
    global deployer, owner1, owner2, user1, user2
    deployer, owner1, owner2, user1, user2 = accounts[0:5]

    testNft = ERC4907.deploy({"from":deployer})
    return testNft

def test_mint(testNft):

    tx = testNft.nftMint({"from":owner1})
    id1 = tx.return_value
    print(f'Minted NFT ( TokenId : {id1} )')
    
    tx = testNft.nftMint({"from":owner2})
    id2 = tx.return_value
    print(f'Minted NFT ( TokenId : {id2} )')

    # check Nft Balance
    assert testNft.balanceOf(owner1.address) == 1
    assert testNft.balanceOf(owner2.address) == 1

    # check Owners
    assert testNft.ownerOf(1) == owner1.address
    assert testNft.ownerOf(2) == owner2.address

    # check Users
    assert testNft.userOf(1) == ADDRESS_ZERO
    assert testNft.userOf(2) == ADDRESS_ZERO


def test_renting(testNft):
    
    rent_expire_time = chain.time() + 2*DAY

    testNft.setUser(1, user1.address, rent_expire_time, {"from":owner1.address})
    testNft.setUser(2, user2.address, rent_expire_time, {"from":owner2.address})

    # check Owners
    assert testNft.ownerOf(1) == owner1.address
    assert testNft.ownerOf(2) == owner2.address

    # check Users
    assert testNft.userOf(1) == user1.address
    assert testNft.userOf(2) == user2.address 

    # Check expires
    assert testNft.userExpires(1)==rent_expire_time
    assert testNft.userExpires(2)==rent_expire_time


def test_double_renting(testNft):

    # Owner cannot rent a NFT to not more than 1 users 
     with brownie.reverts("User already assigned"):
        testNft.setUser(1, user1.address, chain.time() + 1*DAY, {"from":owner1.address})         
        testNft.setUser(2, user2.address, chain.time() + 1*DAY, {"from":owner2.address})         

def test_user_nft_transfer(testNft) :

    # User should not be able to transfer NFTs 
     with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
        testNft.safeTransferFrom(owner1.address, user1.address, 1, {"from":user1.address})         
        testNft.safeTransferFrom(owner1.address, user2.address, 2, {"from":user2.address})

def test_renting_expired(testNft):

    # After 2 days 
    chain.sleep(2*DAY + 1)
    chain.mine(1)

     # Check expires
    assert testNft.userExpires(1) < chain.time()
    assert testNft.userExpires(2) < chain.time()

    # check Users
    assert testNft.userOf(1) == ADDRESS_ZERO
    assert testNft.userOf(2) == ADDRESS_ZERO 


