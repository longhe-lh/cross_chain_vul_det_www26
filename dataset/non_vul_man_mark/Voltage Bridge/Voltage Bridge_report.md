# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: UserRequestForAffirmation1, FailedMessageFixed2
- **rel_chain**: RelayedMessage
- **det_chain**: TokensBridged1, FailedMessageFixed2
### src_chain: HomeChain
- **事件**: UserRequestForAffirmation1
  - 函数: requireToPassMessage
  - 关键操作: require(messageId() == bytes32(0)), require(_gas >= getMinimumGasUsage(_data) && _gas <= maxGasPerTx())
- **事件**: FailedMessageFixed2
  - 函数: fixFailedMessage
  - 关键操作: require(!messageFixed(_messageId))
### rel_chain: RelayChain
- **事件**: RelayedMessage
  - 函数: executeSignatures
  - 关键操作: Message.hasEnoughValidSignatures(_data, _signatures, validatorContract(), true), require(_isMessageVersionValid(messageId)), require(_isDestinationChainIdValid(chainIds[1])), require(!relayedMessages(messageId))
### det_chain: ForeignChain
- **事件**: TokensBridged1
  - 函数: handleBridgedTokens
  - 关键操作: require(isTokenRegistered(_token)), _handleBridgedTokens(_token, _recipient, _value)
- **事件**: FailedMessageFixed2
  - 函数: fixFailedMessage
  - 关键操作: require(!messageFixed(_messageId))
---
