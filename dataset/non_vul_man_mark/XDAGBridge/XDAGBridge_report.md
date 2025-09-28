# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: CrossERC20XDAG1
- **det_chain**: AcceptedCrossTransfer1
### src_chain: Ethereum (or ERC20 Chain)
- **事件**: CrossERC20XDAG1
  - 函数: receiveTokens
  - 关键操作: BridgeToken(erc20XDAG).transferFrom(_msgSender(), address(this), amount), BridgeToken(erc20XDAG).burn(address(this), burnAmount)
### rel_chain: 
- 无事件
### det_chain: Destination Chain (e.g., XDAG)
- **事件**: AcceptedCrossTransfer1
  - 函数: acceptTransfer
  - 关键操作: require(receiver != NULL_ADDRESS, "Bridge: Receiver is null"), require(amount > 0, "Bridge: Amount 0"), require(blockHash != NULL_HASH, "Bridge: BlockHash is null"), require(transactionHash != NULL_HASH, "Bridge: Transaction is null"), require(!processed[compiledId], "Bridge: Already processed"), processed[compiledId] = true, BridgeToken(erc20XDAG).mint(receiver, amount)
---
