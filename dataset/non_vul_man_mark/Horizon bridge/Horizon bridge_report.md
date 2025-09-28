# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Locked1, Locked2, Locked3
- **rel_chain**: mint, withdraw
- **det_chain**: Unlocked1, Unlocked2, Unlocked3
### src_chain: Ethereum
- **事件**: Locked1
  - 函数: lockToken
  - 关键操作: require(recipient != address(0), "EthManager/recipient is a zero address"), require(amount > 0, "EthManager/zero token locked"), busd_.transferFrom(msg.sender, address(this), amount), _actualAmount = _balanceBefore.sub(_balanceAfter)
- **事件**: Locked2
  - 函数: lockToken
  - 关键操作: require(recipient != address(0), "EthManager/recipient is a zero address"), require(amount > 0, "EthManager/zero token locked"), ethToken.safeTransferFrom(msg.sender, address(this), amount), _actualAmount = _balanceBefore.sub(_balanceAfter)
- **事件**: Locked3
  - 函数: lockToken
  - 关键操作: require(recipient != address(0), "EthManager/recipient is a zero address"), require(amount > 0, "EthManager/zero token locked"), link_.transferFrom(msg.sender, address(this), amount), _actualAmount = _balanceBefore.sub(_balanceAfter)
### rel_chain: RelayChain
- **事件**: mint
  - 函数: increaseSupply
- **事件**: withdraw
  - 函数: decreaseSupply
### det_chain: Harmony
- **事件**: Unlocked1
  - 函数: unlockToken
  - 关键操作: require(!usedEvents_[receiptId], "EthManager/The burn event cannot be reused"), usedEvents_[receiptId] = true, busd_.transfer(recipient, amount)
- **事件**: Unlocked2
  - 函数: unlockToken
  - 关键操作: require(!usedEvents_[receiptId], "EthManager/The burn event cannot be reused"), usedEvents_[receiptId] = true, ethToken.safeTransfer(recipient, amount)
- **事件**: Unlocked3
  - 函数: unlockToken
  - 关键操作: require(!usedEvents_[receiptId], "EthManager/The burn event cannot be reused"), usedEvents_[receiptId] = true, link_.transfer(recipient, amount)
---
