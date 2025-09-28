# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: NewPortal1
- **det_chain**: DestinationPortalOpened1, DestinationTransferFinalized1
### src_chain: source_chain
- **事件**: NewPortal1
  - 函数: initPortal
  - 关键操作: require(tokenContract.allowance(msg.sender, address(this)) >= _amount, "Error: Insuficient allowance"), _hasActiveTransferOut[msg.sender] = true, _transfersOut[msg.sender] = Transfer(_commitment, msg.sender, _receiver, _tokenContract, _amount, _hashLock, block.timestamp + 1 hours), tokenContract.transferFrom(msg.sender, address(this), _amount)
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: DestinationPortalOpened1
  - 函数: portalFromOtherChain
  - 关键操作: require(contractToContract[_tokenContract] != address(0x0), "Error: Token contract doesn't have a match in this chain"), _transfersIn[_receiver] = Transfer(_commitment, _sender, _receiver, contractToContract[_tokenContract], _amount, _hashLock, _timeLock)
- **事件**: DestinationTransferFinalized1
  - 函数: finalizeInterPortalTransferDest
  - 关键操作: require(hashThis(abi.encode(_secretKey)) == transfer.hashLock, "Error: hash lock does not match"), require(block.timestamp <= transfer.timeLock, "Error: transfer wasn't finalized within time"), require(tokenContract.balanceOf(address(this)) >= transfer.amount, "Error: not enough liquidity to bridge funds"), tokenContract.transfer(_receiver, transfer.amount)
---
