# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenSent1, ContractCall2, ContractCallWithToken3
- **rel_chain**: execute
- **det_chain**: Executed1, ContractCallApproved2, ContractCallApprovedWithMint3
### src_chain: source_chain
- **事件**: TokenSent1
  - 函数: sendToken
  - 关键操作: _burnTokenFrom(msg.sender, symbol, amount)
- **事件**: ContractCall2
  - 函数: callContract
- **事件**: ContractCallWithToken3
  - 函数: callContractWithToken
  - 关键操作: _burnTokenFrom(msg.sender, symbol, amount)
### rel_chain: relay_chain
- **事件**: execute
  - 函数: execute
  - 关键操作: bool allowOperatorshipTransfer = IAxelarAuth(AUTH_MODULE).validateProof(messageHash, proof), if (chainId != block.chainid) revert InvalidChainId(), if (commandsLength != commands.length || commandsLength != params.length) revert InvalidCommands()
### det_chain: destination_chain
- **事件**: Executed1
  - 函数: burnToken
  - 关键操作: address tokenAddress = tokenAddresses(symbol), if (tokenAddress == address(0)) revert TokenDoesNotExist(symbol)
- **事件**: ContractCallApproved2
  - 函数: approveContractCall
  - 关键操作: _setContractCallApproved(commandId, sourceChain, sourceAddress, contractAddress, payloadHash)
- **事件**: ContractCallApprovedWithMint3
  - 函数: approveContractCallWithMint
  - 关键操作: _setContractCallApprovedWithMint(commandId, sourceChain, sourceAddress, contractAddress, payloadHash, symbol, amount)
---
