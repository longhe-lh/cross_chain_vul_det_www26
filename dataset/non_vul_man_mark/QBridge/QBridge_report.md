# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Deposit1
- **rel_chain**: ProposalVote, ProposalEvent
- **det_chain**: TokenMint1
### src_chain: source_chain
- **事件**: Deposit1
  - 函数: deposit
  - 关键操作: require(msg.value == fee, "QBridge: invalid fee"), require(handler != address(0), "QBridge: invalid resourceID"), _depositCounts[destinationDomainID]++
### rel_chain: relay_chain
- **事件**: ProposalVote
  - 函数: voteProposal
  - 关键操作: require(handlerAddress != address(0), "QBridge: invalid handler"), require(uint(proposal._status) <= 1, "QBridge: proposal already executed/cancelled"), require(!_hasVoted(proposal, msg.sender), "QBridge: relayer already voted")
- **事件**: ProposalEvent
  - 函数: executeProposal
  - 关键操作: require(proposal._status == ProposalStatus.Passed, "QBridge: Proposal must have Passed status"), proposal._status = ProposalStatus.Executed
### det_chain: destination_chain
- **事件**: TokenMint1
  - 函数: mint
  - 关键操作: _mint(recipientAddress, amount)
---
