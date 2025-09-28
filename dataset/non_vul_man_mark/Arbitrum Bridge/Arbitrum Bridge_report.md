# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: MessageDelivered1, BridgeCallTriggered2
- **rel_chain**: SequencerBatchDelivered, NodeCreated, ChallengeStarted
- **det_chain**: OutBoxTransactionExecuted1, SendRootUpdated2
### src_chain: L1
- **事件**: MessageDelivered1
  - 函数: enqueueDelayedMessage
  - 关键操作: if (!allowedDelayedInboxesMap[msg.sender].allowed) revert NotDelayedInbox(msg.sender);, return addMessageToDelayedAccumulator(...);
- **事件**: BridgeCallTriggered2
  - 函数: executeCall
  - 关键操作: if (!allowedOutboxesMap[msg.sender].allowed) revert NotOutbox(msg.sender);, address prevOutbox = _activeOutbox;, _activeOutbox = msg.sender;, (success, returnData) = to.call{value: value}(data);, _activeOutbox = prevOutbox;, emit BridgeCallTriggered(...)
### rel_chain: Rollup
- **事件**: SequencerBatchDelivered
  - 函数: addSequencerL2BatchFromOrigin
  - 关键操作: if (msg.sender != tx.origin) revert NotOrigin();, require(isBatchPoster[msg.sender], "NotBatchPoster");, formDataHash(data, afterDelayedMessagesRead);, addSequencerL2BatchImpl(dataHash, afterDelayedMessagesRead, data.length);, emit SequencerBatchDelivered(...)
- **事件**: NodeCreated
  - 函数: createNewNode
  - 关键操作: require(assertion.afterState.machineStatus == MachineStatus.FINISHED || assertion.afterState.machineStatus == MachineStatus.ERRORED);, require(RollupLib.stateHash(assertion.beforeState, prevNodeInboxMaxCount) == memoryFrame.prevNode.stateHash);, newNodeHash = RollupLib.nodeHash(...);, getNodeStorage(prevNodeNum).childCreated(nodeNum);, emit NodeCreated(...)
- **事件**: ChallengeStarted
  - 函数: createChallenge
  - 关键操作: require(msg.sender == address(resultReceiver), "ONLY_ROLLUP_CHAL");, challenges[challengeIndex] = ChallengeLib.Challenge(...);, emit InitiatedChallenge(...), completeBisection(challengeIndex, 0, numBlocks, segments);
### det_chain: L2
- **事件**: OutBoxTransactionExecuted1
  - 函数: executeTransaction
  - 关键操作: recordOutputAsSpent(proof, index, userTx);, executeTransactionImpl(index, l2Sender, to, l2Block, l1Block, l2Timestamp, value, data);
- **事件**: SendRootUpdated2
  - 函数: updateSendRoot
  - 关键操作: if (msg.sender != rollup) revert NotRollup(...);, roots[root] = l2BlockHash;, emit SendRootUpdated(...)
---
