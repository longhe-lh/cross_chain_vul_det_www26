# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TransactionEnqueued1
- **rel_chain**: TransactionBatchAppended
- **det_chain**: RelayedMessage1
### src_chain: L1
- **事件**: TransactionEnqueued1
  - 函数: enqueue
  - 关键操作: require(_data.length <= MAX_ROLLUP_TX_SIZE, 'Transaction data size exceeds maximum for rollup transaction.'), require(_gasLimit <= maxTransactionGasLimit, 'Transaction gas limit exceeds maximum for rollup transaction.'), require(_gasLimit >= MIN_ROLLUP_TX_Gas, 'Transaction gas limit too low to enqueue.'), if (_gasLimit > enqueueL2GasPrepaid) { ... }, queueElements.push(...)
### rel_chain: Relay
- **事件**: TransactionBatchAppended
  - 函数: appendSequencerBatch
  - 关键操作: require(shouldStartAtElement == getTotalElements(), 'Actual batch start index does not match expected start index.'), require(msg.sender == resolve('OVM_Sequencer'), 'Function can only be called by the Sequencer.'), require(nextQueueIndex <= queueElements.length, 'Attempted to append more elements than are available in the queue.')
### det_chain: L2
- **事件**: RelayedMessage1
  - 函数: relayMessage
---
