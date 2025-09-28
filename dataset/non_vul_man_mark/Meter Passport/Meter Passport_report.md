# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Deposit1, ProposalVote1, ProposalEvent1
- **rel_chain**: RoleGranted, RoleRevoked, ProposalVote, ProposalEvent
- **det_chain**: Deposit1, ProposalEvent1, ProposalVote1
### src_chain: Ethereum
- **事件**: Deposit1
  - 函数: deposit
  - 关键操作: require(msg.value == _fee, "Incorrect fee supplied"), uint64 depositNonce = ++_depositCounts[destinationChainID];
- **事件**: ProposalVote1
  - 函数: voteProposal
  - 关键操作: require(!_hasVotedOnProposal[nonceAndID][dataHash][msg.sender], "relayer already voted"), proposal._yesVotes.push(msg.sender);
- **事件**: ProposalEvent1
  - 函数: executeProposal
  - 关键操作: require(proposal._status == ProposalStatus.Passed, "proposal already transferred"), depositHandler.executeProposal(proposal._resourceID, data);
### rel_chain: RelayChain
- **事件**: RoleGranted
  - 函数: grantRole
  - 关键操作: require(hasRole(_roles[role].adminRole, _msgSender()), "AccessControl: sender must be an admin to grant")
- **事件**: RoleRevoked
  - 函数: revokeRole
  - 关键操作: require(hasRole(_roles[role].adminRole, _msgSender()), "AccessControl: sender must be an admin to revoke")
- **事件**: ProposalVote
  - 函数: voteProposal
  - 关键操作: require(uint256(proposal._status) <= 1, "proposal already executed/cancelled"), proposal._yesVotes = (proposal._yesVotes | _relayerBit(sender)).toUint200();
- **事件**: ProposalEvent
  - 函数: executeProposal
  - 关键操作: require(proposal._status == ProposalStatus.Passed, "Proposal must have Passed status"), depositHandler.executeProposal(resourceID, data);
### det_chain: Ethereum
- **事件**: Deposit1
  - 函数: deposit
  - 关键操作: require(msg.value == _fee, "Incorrect fee supplied"), uint64 depositNonce = ++_depositCounts[destinationChainID];
- **事件**: ProposalEvent1
  - 函数: executeProposal
  - 关键操作: require(proposal._status == ProposalStatus.Passed, "proposal already transferred"), depositHandler.executeProposal(proposal._resourceID, data);
- **事件**: ProposalVote1
  - 函数: voteProposal
  - 关键操作: require(uint256(proposal._status) <= 1, "proposal already executed/cancelled"), proposal._yesVotes = (proposal._yesVotes | _relayerBit(sender)).toUint200();
---
