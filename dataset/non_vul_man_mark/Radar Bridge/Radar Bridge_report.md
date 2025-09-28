# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokensBridged1
- **det_chain**: TokensClaimed1
### src_chain: source_chain
- **事件**: TokensBridged1
  - 函数: bridgeTokens
  - 关键操作: require(isSupportedToken[_token], "Token not supported"), require(IERC20(_token).balanceOf(msg.sender) >= _amount, "Not enough tokens"), require(_destChain != CHAIN, "Cannot send to same chain")
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: TokensClaimed1
  - 函数: claimTokens
  - 关键操作: require(_token != address(0) && isSupportedToken[_token], "Token not supported."), require(_destChain == CHAIN, "Claiming tokens on wrong chain"), require(doubleSpendingProtection[message] == false, "Double Spending"), require(nonceDoubleSpendingProtection[_nonce] == false, "Nonce Double Spending"), require(SignatureLibrary.verify(message, _signature, idToRouter[_tokenId]) == true, "Router Signature Invalid")
---
