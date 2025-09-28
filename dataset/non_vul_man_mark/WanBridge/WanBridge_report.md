# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokenMint1, TokenClaim1
- **det_chain**: Transfer1, claimTokens1
### src_chain: Ethereum
- **事件**: TokenMint1
  - 函数: buyWanCoin
  - 关键操作: require(receipient != 0x0);, require(msg.value >= 0.1 ether);, require(!isContract(msg.sender));, buyEarlyAdopters(receipient);, buyNormal(receipient);
- **事件**: TokenClaim1
  - 函数: claimTokens
  - 关键操作: wanToken.claimTokens(receipent);
### rel_chain: 
- 无事件
### det_chain: Ethereum
- **事件**: Transfer1
  - 函数: transfer
  - 关键操作: if (balances[msg.sender] >= _value) { balances[msg.sender] -= _value; balances[_to] += _value; return true; } else { return false; }
- **事件**: claimTokens1
  - 函数: claimTokens
  - 关键操作: balances[receipent] = balances[receipent].add(lockedBalances[receipent]);, lockedBalances[receipent] = 0;
---
