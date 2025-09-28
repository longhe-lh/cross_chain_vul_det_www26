# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: ExchangeBuy1, ExchangePay2
- **rel_chain**: ProofEvent
- **det_chain**: ExchangeBuyConfirm1, ExchangePayConfirm2, Revoke1, Commit1
### src_chain: source_chain
- **事件**: ExchangeBuy1
  - 函数: exchangeBuy
  - 关键操作: proofRecord.toChain = cctChannel.getChannelCrossChain(channel), proofRecord.pmId = pmId, proofRecord.channel = channel, proofRecord.cctTxHash = cctTxHash, proofRecord.status = ProofStatus.LOCK
- **事件**: ExchangePay2
  - 函数: exchangePay
  - 关键操作: proofRecord.toChain = cctChannel.getChannelCrossChain(channel), proofRecord.pmId = pmId, proofRecord.channel = channel, proofRecord.cctTxHash = cctTxHash, proofRecord.status = ProofStatus.LOCK
### rel_chain: relay_chain
- **事件**: ProofEvent
  - 函数: addCrossData
  - 关键操作: require(fromChain != toChain,"fromChain is the same as the toChain"), require(cctRoot.getChainId() == toChain, "bad chainId"), require(cctRoot.verify(pmId,proofData,crossData),"no authorized pmId")
### det_chain: destination_chain
- **事件**: ExchangeBuyConfirm1
  - 函数: commit
  - 关键操作: require(proofRecord.cctTxHash != 0x0, "proofRecord not exists"), require(proofRecord.status == ProofStatus.CONFIRM,"proofRecord valid")
- **事件**: ExchangePayConfirm2
  - 函数: commit
  - 关键操作: require(proofRecord.cctTxHash != 0x0, "proofRecord not exists"), require(proofRecord.status == ProofStatus.CONFIRM && proofRecord.status == ProofStatus.LOCK, "proofRecord valid")
- **事件**: Revoke1
  - 函数: revoke
  - 关键操作: require(proofRecord.cctTxHash != 0x0, "proofRecord not exists"), require(proofRecord.status != ProofStatus.CONFIRM && proofRecord.status != ProofStatus.LOCK, "invalid status")
- **事件**: Commit1
  - 函数: commit
  - 关键操作: proofRecord.status = ProofStatus.COMMIT
---
