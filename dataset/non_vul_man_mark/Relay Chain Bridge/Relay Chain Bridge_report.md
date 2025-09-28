# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Deposit1
- **rel_chain**: ProposalVote, ProposalEvent
- **det_chain**: ProposalEvent1
### src_chain: source_chain
- **事件**: Deposit1
  - 函数: deposit
  - 关键操作: require(msg.value == _fees[destinationChainID], "Incorrect fee supplied"), require(handler != address(0), "resourceID not mapped to handler"), _depositCounts[destinationChainID]++, emit Deposit(destinationChainID, resourceID, depositNonce)
### rel_chain: relay_chain
- **事件**: ProposalVote
  - 函数: voteProposal
  - 关键操作: require(_resourceIDToHandlerAddress[resourceID] != address(0), "no handler for resourceID"), require(uint(proposal._status) <= 1, "proposal already executed"), require(!_hasVotedOnProposal[nonceAndID][dataHash][msg.sender], "relayer already voted"), proposal._yesVotes.push(msg.sender), _hasVotedOnProposal[nonceAndID][dataHash][msg.sender] = true, emit ProposalVote(chainID, depositNonce, proposal._status, resourceID)
- **事件**: ProposalEvent
  - 函数: voteProposal
  - 关键操作: ++_totalProposals, _proposals[nonceAndID][dataHash] = Proposal(...), emit ProposalEvent(chainID, depositNonce, ProposalStatus.Active, resourceID, dataHash), emit ProposalEvent(chainID, depositNonce, proposal._status, proposal._resourceID, proposal._dataHash)
### det_chain: destination_chain
- **事件**: ProposalEvent1
  - 函数: executeProposal
  - 关键操作: bytes memory callData = abi.encodePacked(sig, metaData), (bool success,) = contractAddress.call(callData), require(success, "delegatecall to contractAddress failed")
---
