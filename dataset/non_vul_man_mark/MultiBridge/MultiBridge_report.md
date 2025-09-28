# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: MessageDispatched1, MessageDispatched2
- **rel_chain**: ContractCall, sendMessage, executeMessage
- **det_chain**: MessageIdExecuted1, MessageIdExecuted2
### src_chain: Ethereum
- **事件**: MessageDispatched1
  - 函数: dispatchMessage
  - 关键操作: if (receiverAdapter == address(0)) { revert Error.ZERO_RECEIVER_ADAPTER(); }, msgId = _getNewMessageId(_toChainId, _to);, bytes memory payload = abi.encode(AdapterPayload(msgId, msg.sender, receiverAdapter, _to, _data));, gateway.callContract(destinationChain, receiverAdapterInString, payload);
- **事件**: MessageDispatched2
  - 函数: dispatchMessage
  - 关键操作: if (_toChainId == 0) { revert Error.ZERO_CHAIN_ID(); }, address receiverAdapter = receiverAdapters[_toChainId];, if (receiverAdapter == address(0)) { revert Error.ZERO_RECEIVER_ADAPTER(); }, msgId = _getNewMessageId(_toChainId, _to);, bytes memory payload = abi.encode(AdapterPayload(msgId, msg.sender, receiverAdapter, _to, _data));, IMessageBus(msgBus).sendMessage{value: msg.value}(receiverAdapter, _toChainId, payload);
### rel_chain: RelayChain
- **事件**: ContractCall
  - 函数: execute
  - 关键操作: if (keccak256(bytes(sourceChain)) != keccak256(bytes(senderChain))) { revert Error.INVALID_SENDER_CHAIN_ID(); }, if (!gateway.validateContractCall(commandId, sourceChain, sourceAddress, keccak256(payload))) { revert Error.NOT_APPROVED_BY_GATEWAY(); }, if (sourceAddress.toAddress() != senderAdapter) { revert Error.INVALID_SENDER_ADAPTER(); }, if (commandIdStatus[commandId] || isMessageExecuted[msgId]) { revert MessageIdAlreadyExecuted(msgId); }, if (decodedPayload.finalDestination != gac.getMultiMessageReceiver(block.chainid)) { revert Error.INVALID_FINAL_DESTINATION(); }, isMessageExecuted[msgId] = true;, commandIdStatus[commandId] = true;
- **事件**: sendMessage
  - 函数: sendMessage
  - 关键操作: if (_srcChainId != senderChain) { revert Error.INVALID_SENDER_CHAIN_ID(); }, if (_srcContract != senderAdapter) { revert Error.INVALID_SENDER_ADAPTER(); }, bytes32 msgId = decodedPayload.msgId;, if (isMessageExecuted[msgId]) { revert MessageIdAlreadyExecuted(msgId); }, isMessageExecuted[decodedPayload.msgId] = true;, if (decodedPayload.finalDestination != gac.getMultiMessageReceiver(block.chainid)) { revert Error.INVALID_FINAL_DESTINATION(); }
- **事件**: executeMessage
  - 函数: executeMessage
  - 关键操作: if (_srcChainId != senderChain) { revert Error.INVALID_SENDER_CHAIN_ID(); }, if (_srcContract != senderAdapter) { revert Error.INVALID_SENDER_ADAPTER(); }, bytes32 msgId = decodedPayload.msgId;, if (isMessageExecuted[msgId]) { revert MessageIdAlreadyExecuted(msgId); }, isMessageExecuted[decodedPayload.msgId] = true;, if (decodedPayload.finalDestination != gac.getMultiMessageReceiver(block.chainid)) { revert Error.INVALID_FINAL_DESTINATION(); }
### det_chain: DestinationChain
- **事件**: MessageIdExecuted1
  - 函数: executeMessage
  - 关键操作: if (block.timestamp > _execData.expiration) { revert Error.MSG_EXECUTION_PASSED_DEADLINE(); }, if (isExecuted[msgId]) { revert Error.MSG_ID_ALREADY_EXECUTED(); }, isExecuted[msgId] = true;, if (messageVotes[msgId] < quorum) { revert Error.INVALID_QUORUM_FOR_EXECUTION(); }
- **事件**: MessageIdExecuted2
  - 函数: executeTransaction
  - 关键操作: if (_eta > block.timestamp) { revert Error.TX_TIMELOCKED(); }, if (block.timestamp > _eta + GRACE_PERIOD) { revert Error.TX_EXPIRED(); }, if (msg.value != _value) { revert Error.INVALID_MSG_VALUE(); }, isExecuted[_txId] = true;, (bool status,) = _target.call{value: _value}(_data);, if (!status) { revert Error.EXECUTION_FAILS_ON_DST(); }
---
