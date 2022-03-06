import http
import re
from telnetlib import WONT
from web3 import Web3
import json

ganache_url = "HTTP://127.0.0.1:7545"

web = Web3(Web3.HTTPProvider(ganache_url))

abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"candidatesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"end","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"hello","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalVote","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')
address = "0xA2d8A75392CD97D6307B43F52C53826992f42637"
bytecode = "0x608060405260016000806101000a81548160ff02191690831515021790555060006004553480156200003057600080fd5b5033600060016101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550620000b86040518060400160405280600781526020017f4b415649594120000000000000000000000000000000000000000000000000008152506200014a60201b60201c565b620000fe6040518060400160405280600581526020017f44455649200000000000000000000000000000000000000000000000000000008152506200014a60201b60201c565b620001446040518060400160405280600581526020017f524f5345200000000000000000000000000000000000000000000000000000008152506200014a60201b60201c565b6200036c565b600360008154809291906200015f90620002c0565b9190505550604051806060016040528060035481526020018281526020016000815250600260006003548152602001908152602001600020600082015181600001556020820151816001019080519060200190620001bf929190620001d0565b506040820151816002015590505050565b828054620001de906200028a565b90600052602060002090601f0160209004810192826200020257600085556200024e565b82601f106200021d57805160ff19168380011785556200024e565b828001600101855582156200024e579182015b828111156200024d57825182559160200191906001019062000230565b5b5090506200025d919062000261565b5090565b5b808211156200027c57600081600090555060010162000262565b5090565b6000819050919050565b60006002820490506001821680620002a357607f821691505b60208210811415620002ba57620002b96200033d565b5b50919050565b6000620002cd8262000280565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8214156200030357620003026200030e565b5b600182019050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b610a23806200037c6000396000f3fe608060405234801561001057600080fd5b50600436106100885760003560e01c80638da5cb5b1161005b5780638da5cb5b14610117578063a3ec138d14610135578063efbe1c1c14610165578063f1cea4c71461016f57610088565b80630121b93f1461008d57806319ff1d21146100a95780632d35a8a2146100c75780633477ee2e146100e5575b600080fd5b6100a760048036038101906100a29190610567565b61018d565b005b6100b1610356565b6040516100be919061073c565b60405180910390f35b6100cf610360565b6040516100dc919061073c565b60405180910390f35b6100ff60048036038101906100fa9190610567565b610366565b60405161010e93929190610757565b60405180910390f35b61011f610418565b60405161012c9190610686565b60405180910390f35b61014f600480360381019061014a919061053a565b61043e565b60405161015c91906106a1565b60405180910390f35b61016d61045e565b005b61017761050a565b604051610184919061073c565b60405180910390f35b600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161561021a576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610211906106bc565b60405180910390fd5b60008111801561022c57506003548111155b61026b576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610262906106dc565b60405180910390fd5b60008054906101000a900460ff166102b8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016102af906106fc565b60405180910390fd5b60018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055506002600082815260200190815260200160002060020160008154809291906103369061085e565b91905055506004600081548092919061034e9061085e565b919050555050565b6000600454905090565b60035481565b600260205280600052604060002060009150905080600001549080600101805461038f9061082c565b80601f01602080910402602001604051908101604052809291908181526020018280546103bb9061082c565b80156104085780601f106103dd57610100808354040283529160200191610408565b820191906000526020600020905b8154815290600101906020018083116103eb57829003601f168201915b5050505050908060020154905083565b600060019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60016020528060005260406000206000915054906101000a900460ff1681565b600060019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146104ee576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016104e59061071c565b60405180910390fd5b60008060006101000a81548160ff021916908315150217905550565b60045481565b60008135905061051f816109bf565b92915050565b600081359050610534816109d6565b92915050565b6000602082840312156105505761054f610905565b5b600061055e84828501610510565b91505092915050565b60006020828403121561057d5761057c610905565b5b600061058b84828501610525565b91505092915050565b61059d816107b1565b82525050565b6105ac816107c3565b82525050565b60006105bd82610795565b6105c781856107a0565b93506105d78185602086016107f9565b6105e08161090a565b840191505092915050565b60006105f8600d836107a0565b91506106038261091b565b602082019050919050565b600061061b6011836107a0565b915061062682610944565b602082019050919050565b600061063e600e836107a0565b91506106498261096d565b602082019050919050565b60006106616013836107a0565b915061066c82610996565b602082019050919050565b610680816107ef565b82525050565b600060208201905061069b6000830184610594565b92915050565b60006020820190506106b660008301846105a3565b92915050565b600060208201905081810360008301526106d5816105eb565b9050919050565b600060208201905081810360008301526106f58161060e565b9050919050565b6000602082019050818103600083015261071581610631565b9050919050565b6000602082019050818103600083015261073581610654565b9050919050565b60006020820190506107516000830184610677565b92915050565b600060608201905061076c6000830186610677565b818103602083015261077e81856105b2565b905061078d6040830184610677565b949350505050565b600081519050919050565b600082825260208201905092915050565b60006107bc826107cf565b9050919050565b60008115159050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b60005b838110156108175780820151818401526020810190506107fc565b83811115610826576000848401525b50505050565b6000600282049050600182168061084457607f821691505b60208210811415610858576108576108d6565b5b50919050565b6000610869826107ef565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82141561089c5761089b6108a7565b5b600182019050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600080fd5b6000601f19601f8301169050919050565b7f416c726561647920766f74656400000000000000000000000000000000000000600082015250565b7f496e76616c69642063616e646964617465000000000000000000000000000000600082015250565b7f456c656374696f6e20656e646564000000000000000000000000000000000000600082015250565b7f204f4e4c59204f574e45522043414e20454e4400000000000000000000000000600082015250565b6109c8816107b1565b81146109d357600080fd5b50565b6109df816107ef565b81146109ea57600080fd5b5056fea26469706673582212202363701d0181c6f8a6a8b9fd8d582197b577925a0ffbe28ae3eea52e4d2883ee64736f6c63430008070033"



def deploy(owner , signature):
    election = web.eth.contract(abi=abi , bytecode=bytecode)
    
    transaction_body = {
        'nonce':web.eth.get_transaction_count(owner),
        'gas'   :1728712,
        'gasPrice':web.toWei(8 , 'gwei')
    }
    
    deployment = election.constructor().buildTransaction(transaction_body)
    signed_transaction = web.eth.account.sign_transaction(deployment , signature)
    result = web.eth.send_raw_transaction(signed_transaction.rawTransaction)
    tx_receipt = web.eth.wait_for_transaction_receipt(result)

    return tx_receipt.contractAddress

owner = "0x18Ac764ACf55E9b76E4B17fe02ecDFB1e71Ca442"
signature = "3659e6e278282cd0a19c6847fba3ded24186e7bf13ccd6cf59f8b10f511c5ab6"
# address = deploy(owner , signature)
# owner = "0x18f05b101391aE1d64B0F854C952473358874ed0"
# signature = "e803a3c1dd8ff3fceb841a42bb0a49175525a0ff6804e3429496a8c24b31b74a"

contract = web.eth.contract(address="0xA2d8A75392CD97D6307B43F52C53826992f42637" , abi=abi)

transaction_body = {
    'nonce':web.eth.get_transaction_count(owner),
    'gas'   :1728712,
    'gasPrice':web.toWei(8 , 'gwei')
}

v = contract.functions.vote(1).buildTransaction(transaction_body)
signed_transaction = web.eth.account.sign_transaction(v , signature)
result = web.eth.send_raw_transaction(signed_transaction.rawTransaction)


r1 = contract.caller().candidatesCount()
r = contract.caller().candidates(0+1)[2]

print(result , r)
