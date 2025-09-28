# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TransferToNearInitiated1, Deposited2
- **rel_chain**: ConsumedProof, BlockHashAdded
- **det_chain**: NearToEthTransferFinalised1, Withdrawn2
### src_chain: Ethereum
- **事件**: TransferToNearInitiated1
  - 函数: transferToNear
  - 关键操作: _burn(msg.sender, _amount), emit TransferToNearInitiated(...)
- **事件**: Deposited2
  - 函数: depositToEVM
  - 关键操作: require(fee < msg.value), emit Deposited(...)
### rel_chain: RelayChain
- **事件**: ConsumedProof
  - 函数: _parseAndConsumeProof
  - 关键操作: require(prover.proveOutcome(...)), require(fullOutcomeProof.block_header_lite.inner_lite.height >= minBlockAcceptanceHeight), usedProofs[receiptId] = true, require(keccak256(...) == keccak256(...)), require(!status.failed), require(!status.unknown)
- **事件**: BlockHashAdded
  - 函数: addLightClientBlock
  - 关键操作: require(nearBlock.next_bps.hash == nearBlock.inner_lite.next_bp_hash), untrustedSignatureSet |= 1 << i, lastValidAt = block.timestamp.add(lockDuration)
### det_chain: Ethereum
- **事件**: NearToEthTransferFinalised1
  - 函数: finaliseNearToEthTransfer
  - 关键操作: _mint(result.recipient, result.amount), emit NearToEthTransferFinalised(...)
- **事件**: Withdrawn2
  - 函数: withdraw
  - 关键操作: payable(result.recipient).transfer(result.amount), emit Withdrawn(...)
---
