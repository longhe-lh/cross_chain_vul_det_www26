# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Locked1
- **rel_chain**: unlock
- **det_chain**: Unlocked1
### src_chain: source_chain
- **事件**: Locked1
  - 函数: lock
  - 关键操作: require(_amount > 0, "The amount of the lock must not be zero"), (bool found,) = indexOfChainId(_toChainId), require(found, "ChainId not allowed"), require(erc20Time.allowance(_msgSender(), address(this)) >= _amount, "Not enough allowance"), erc20Time.safeTransferFrom(_msgSender(), address(this), _amount)
### rel_chain: relay_chain
- **事件**: unlock
  - 函数: unlock
  - 关键操作: require(!burnIdsUsed[_fromChainId][_burnId], "Burn id already used"), bytes32 messageHash = keccak256(abi.encodePacked(_msgSender(), _fromChainId, block.chainid, _burnId, _amount)), require(checkSignatures(messageHash, _signatures), "Incorrect signature(s)"), burnIdsUsed[_fromChainId][_burnId] = true
### det_chain: destination_chain
- **事件**: Unlocked1
  - 函数: unlock
  - 关键操作: erc20Time.safeTransfer(_msgSender(), _amount)
---
