# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: MessageDispatched1, NewMMRRoot1
- **rel_chain**: Message
- **det_chain**: Locked1, Created1
### src_chain: Ethereum
- **事件**: MessageDispatched1
  - 函数: submit
  - 关键操作: vault.withdraw(message.origin, payable(msg.sender), reward), if (gasleft() < gasToForward + GAS_BUFFER) { revert NotEnoughGas(); }
- **事件**: NewMMRRoot1
  - 函数: submitFinal
  - 关键操作: latestMMRRoot = newMMRRoot, latestBeefyBlock = commitment.blockNumber
### rel_chain: Polkadot Relay Chain
- **事件**: Message
  - 函数: submit
  - 关键操作: nonce[dest] = nonce[dest] + 1, vault.deposit{value: msg.value}(dest)
### det_chain: Substrate-based Parachain
- **事件**: Locked1
  - 函数: lock
  - 关键操作: vault.deposit(msg.sender, token, amount)
- **事件**: Created1
  - 函数: create
  - 关键操作: require(msg.value >= createTokenFee, 'NoFundsforCreateToken')
---
