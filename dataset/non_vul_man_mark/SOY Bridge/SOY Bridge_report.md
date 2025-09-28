# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Deposit1, BridgeToContract1
- **rel_chain**: claim, claimToContract
- **det_chain**: Claim1, ClaimToContract1
### src_chain: source_chain
- **事件**: Deposit1
  - 函数: depositTokens
  - 关键操作: require(receiver != address(0), "Incorrect receiver address"), require(functionMapping & 1 == 0, "locked"), tokenDeposits[token] += value, token.safeTransferFrom(msg.sender, address(this), value)
- **事件**: BridgeToContract1
  - 函数: bridgeToContract
  - 关键操作: require(functionMapping & 2 == 0, "locked"), require(receiver != address(0), "Incorrect receiver address")
### rel_chain: relay_chain
- **事件**: claim
  - 函数: claim
  - 关键操作: require(!isTxProcessed[fromChainId][txId], "Transaction already processed"), tokenDeposits[token] -= value, token.safeTransfer(to, value)
- **事件**: claimToContract
  - 函数: claimToContract
  - 关键操作: require(!isTxProcessed[fromChainId][txId], "Transaction already processed"), tokenDeposits[token] -= value
### det_chain: destination_chain
- **事件**: Claim1
  - 函数: claim
  - 关键操作: require(!isTxProcessed[fromChainId][txId], "Transaction already processed"), tokenDeposits[token] -= value, token.safeTransfer(to, value)
- **事件**: ClaimToContract1
  - 函数: claimToContract
  - 关键操作: require(!isTxProcessed[fromChainId][txId], "Transaction already processed"), tokenDeposits[token] -= value
---
