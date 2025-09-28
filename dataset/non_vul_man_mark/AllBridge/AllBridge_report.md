# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokensSent1
- **rel_chain**: MessageSent, MessageReceived
- **det_chain**: Received1
### src_chain: source_chain
- **事件**: TokensSent1
  - 函数: sendTokens
  - 关键操作: require(destinationChainId != sourceChainId, "Bridge: wrong destination chain"), require(otherBridgeTokens[destinationChainId][receiveToken], "Bridge: unknown chain or token"), sstore(key, true)
### rel_chain: relay_chain
- **事件**: MessageSent
  - 函数: publishMessage
  - 关键操作: sentMessages[messageWithSender] = true
- **事件**: MessageReceived
  - 函数: receiveMessage
  - 关键操作: receivedMessages[messageWithSender] = true
### det_chain: destination_chain
- **事件**: Received1
  - 函数: receiveTokens
  - 关键操作: require(otherBridges[sourceChainId] != bytes32(0), "Bridge: source not registered"), sstore(key, true), require(this.hasReceivedMessage(messageWithSender, messenger), "Bridge: no message")
---
