# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: RetryableTicketCreated1, L2ToL1TxSubmitted1
- **rel_chain**: MessageDelivered, SentMessage
- **det_chain**: L2ToL1TxSubmitted1, RetryableTicketCreated1
### src_chain: Arbitrum L1 / Optimism L1
- **事件**: RetryableTicketCreated1
  - 函数: _sendCrossChainMessage
  - 关键操作: ticketId = ArbitrumL1_Inbox(delayedInbox).createRetryableTicket{value: params.depositValue}(...)
- **事件**: L2ToL1TxSubmitted1
  - 函数: _sendCrossChainMessage
  - 关键操作: IL1StandardBridge(bridge).depositETHTo{value: params.depositValue}(destination, params.gasLimit, data), ICrossDomainMessenger(messenger).sendMessage(destination, data, params.gasLimit)
### rel_chain: Arbitrum Relay / Optimism Relay
- **事件**: MessageDelivered
  - 函数: deliverMessageToInbox
- **事件**: SentMessage
  - 函数: sendMessage
### det_chain: Arbitrum L2 / Optimism L2
- **事件**: L2ToL1TxSubmitted1
  - 函数: _sendCrossChainMessage
  - 关键操作: crossChainTxId = ArbitrumL2_Bridge(arbsys).sendTxToL1{value: params.depositValue}(destination, data)
- **事件**: RetryableTicketCreated1
  - 函数: _sendCrossChainMessage
  - 关键操作: IL2StandardBridge(bridge).withdrawTo(..., params.depositValue, params.gasLimit, data), ICrossDomainMessenger(messenger).sendMessage(destination, data, params.gasLimit)
---
