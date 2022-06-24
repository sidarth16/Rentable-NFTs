from brownie import ERC4907
from brownie import accounts, Wei
import pytest
# from brownie.convert import EthAddress

deployer, user1, user2  = None, None, None

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
    print("testNft.userOf(1) : ",testNft.userOf(1))
    assert testNft.userOf(1) == "0x0000000000000000000000000000000000000000"
    assert testNft.userOf(2) == "0x0000000000000000000000000000000000000000"


# contract("test", async accounts => {

#     it("should set user to Bob", async () => {
#         // Get initial balances of first and second account.
#         const Alice = accounts[0];
#         const Bob = accounts[1];

#         const instance = await ERC4907Demo.deployed("T", "T");
#         const demo = instance;

#         await demo.mint(1, Alice);
#         let expires = Math.floor(new Date().getTime()/1000) + 1000;
#         await demo.setUser(1, Bob, BigInt(expires));

#         let user_1 = await demo.userOf(1);

#         assert.equal(
#             user_1,
#             Bob,
#             "User of NFT 1 should be Bob"
#         );

#         let owner_1 = await demo.ownerOf(1);
#         assert.equal(
#             owner_1,
#             Alice ,
#             "Owner of NFT 1 should be Alice"
#         );
#     });
# });

