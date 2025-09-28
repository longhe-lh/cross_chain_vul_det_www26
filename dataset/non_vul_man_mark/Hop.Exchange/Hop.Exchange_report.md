# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TransferSentToL21, TransferRootBonded2
- **rel_chain**: setTransferRoot, distribute
- **det_chain**: Withdrew1, WithdrawalBonded2
### src_chain: Ethereum Mainnet (L1)
- **事件**: TransferSentToL21
  - 函数: sendToL2
  - 关键操作: _transferToBridge(msg.sender, amount), chainBalance[chainId] = chainBalance[chainId].add(amount)
- **事件**: TransferRootBonded2
  - 函数: bondTransferRoot
  - 关键操作: _distributeTransferRoot(rootHash, destinationChainId, totalAmount)
### rel_chain: Relay Chain (Layer-2 Communication)
- **事件**: setTransferRoot
  - 函数: setTransferRoot
  - 关键操作: require(_transferRoots[transferRootId].total == 0, "BRG: Transfer root already set"), require(totalAmount > 0, "BRG: Cannot set TransferRoot totalAmount of 0"), _transferRoots[transferRootId] = TransferRoot(totalAmount, 0, block.timestamp), emit TransferRootSet(rootHash, totalAmount)
- **事件**: distribute
  - 函数: _distributeTransferRoot
  - 关键操作: chainBalance[chainId] = chainBalance[chainId].add(totalAmount), messengerWrapper.sendCrossDomainMessage(setTransferRootMessage)
### det_chain: Layer-2 Network (e.g., Arbitrum, Optimism)
- **事件**: Withdrew1
  - 函数: withdraw
  - 关键操作: require(rootHash.verify(transferId, transferIdTreeIndex, siblings, totalLeaves), "BRG: Invalid transfer proof"), _addToAmountWithdrawn(transferRootId, amount), _fulfillWithdraw(transferId, recipient, amount, uint256(0))
- **事件**: WithdrawalBonded2
  - 函数: bondWithdrawal
  - 关键操作: _bondWithdrawal(transferId, amount), _fulfillWithdraw(transferId, recipient, amount, bonderFee)
---
