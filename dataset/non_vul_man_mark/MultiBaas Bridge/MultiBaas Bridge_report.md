# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Deposit1, Deposit2
- **rel_chain**: ProposalEvent, ProposalVote
- **det_chain**: TokenWithdraw1, NFTMint2
### src_chain: SourceChain
- **事件**: Deposit1
  - 函数: deposit
  - 关键操作: require(msg.value == _fee, "Incorrect fee supplied"), address handler = _resourceIDToHandlerAddress[resourceID], uint64 depositNonce = ++_depositCounts[destinationChainID]
- **事件**: Deposit2
  - 函数: deposit
  - 关键操作: require(msg.value == _fee, "Incorrect fee supplied"), address handler = _resourceIDToHandlerAddress[resourceID], uint64 depositNonce = ++_depositCounts[destinationChainID]
### rel_chain: RelayChain
- **事件**: ProposalEvent
  - 函数: voteProposal
  - 关键操作: Proposal memory proposal = _proposals[nonceAndID][dataHash], if (proposal._status == ProposalStatus.Inactive) { proposal = Proposal(...) }, if (proposal._yesVotesTotal >= _relayerThreshold) { proposal._status = ProposalStatus.Passed }
- **事件**: ProposalVote
  - 函数: executeProposal
  - 关键操作: Proposal storage proposal = _proposals[nonceAndID][dataHash], require(proposal._status == ProposalStatus.Passed, "Proposal must have Passed status"), proposal._status = ProposalStatus.Executed
### det_chain: DestinationChain
- **事件**: TokenWithdraw1
  - 函数: executeProposal
  - 关键操作: (amount, lenDestinationRecipientAddress) = abi.decode(data, (uint, uint)), address tokenAddress = _resourceIDToTokenContractAddress[resourceID], if (_burnList[tokenAddress]) { mintERC20(...) } else { releaseERC20(...) }
- **事件**: NFTMint2
  - 函数: executeProposal
  - 关键操作: (tokenID, lenDestinationRecipientAddress) = abi.decode(data, (uint, uint)), address tokenAddress = _resourceIDToTokenContractAddress[resourceID], if (_burnList[tokenAddress]) { mintERC721(...) } else { releaseERC721(...) }
---
