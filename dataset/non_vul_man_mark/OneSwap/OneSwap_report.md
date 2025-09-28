# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Locksend1, Unlock2
- **rel_chain**: rel_event_name
- **det_chain**: Unlock1, Locksend2
### src_chain: LockSend
- **事件**: Locksend1
  - 函数: lockSend
  - 关键操作: require(amount != 0, "LockSend: LOCKED_AMOUNT_SHOULD_BE_NONZERO"), _safeTransferToMe(token, msg.sender, amount), lockSendInfos[key] = lockSendInfos[key].add(amount)
- **事件**: Unlock2
  - 函数: unlock
  - 关键操作: require(amount != 0, "LockSend: UNLOCK_AMOUNT_SHOULD_BE_NONZERO"), delete lockSendInfos[key], _safeTransfer(token, to, amount)
### rel_chain: RelayChain
- **事件**: rel_event_name
  - 函数: relayFunction
### det_chain: DestinationChain
- **事件**: Unlock1
  - 函数: unlock
  - 关键操作: require(amount != 0, "LockSend: UNLOCK_AMOUNT_SHOULD_BE_NONZERO"), delete lockSendInfos[key], _safeTransfer(token, to, amount)
- **事件**: Locksend2
  - 函数: lockSend
  - 关键操作: require(amount != 0, "LockSend: LOCKED_AMOUNT_SHOULD_BE_NONZERO"), _safeTransferToMe(token, msg.sender, amount), lockSendInfos[key] = lockSendInfos[key].add(amount)
---
