# 跨链桥合约分析报告
## 跨链桥: PolkaBridge
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: messageReceived
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: Ethereum
- **事件**: TokenDeposit1
  - 函数: deposit
  - 关键操作: require(block.timestamp >= pools[poolIndex].Begin && block.timestamp <= pools[poolIndex].End, "invalid time"), require(whitelist[pid][msg.sender].IsWhitelist && whitelist[pid][msg.sender].IsActived, "invalid user")
- **事件**: TokenRedeem2
  - 函数: claimToken
  - 关键操作: require(!whitelist[pid][msg.sender].IsClaimed, "user already claimed"), require(block.timestamp >= pools[poolIndex].End.add(pools[poolIndex].LockDuration), "not on time for claiming token")
### rel_chain: Polkadot
- **事件**: messageReceived
  - 函数: handleMessage
  - 关键操作: require(_msgSender() == owner(), "Only owner can call")
### det_chain: Ethereum
- **事件**: TokenWithdraw1
  - 函数: withdrawToken
  - 关键操作: pools[poolIndex].IDOToken.transfer(msg.sender, userBalance)
- **事件**: TokenMint2
  - 函数: mintNFT
  - 关键操作: _mint(recipient_, id_, amount_, '')
---
